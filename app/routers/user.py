from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    new_user = models.User(
        username=user.username,
        email=user.email
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database Error while creating user"
        )
    return new_user
@router.get("/", response_model=List[schemas.UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(models.User).offset(skip).limit(limit).all()        
@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(  
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    updated: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated.model_dump().items():
        setattr(user, key, value)  # type: ignore[arg-type]

    db.commit()
    db.refresh(user)
    return user 
@router.delete("/{user_id}", status_code=200)
def delete_user(    
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])


@router.post("/", response_model=schemas.VolunteerResponse)
def create_volunteer(volunteer: schemas.VolunteerCreate, db: Session = Depends(database.get_db)):

    new_volunteer = models.Volunteer(
        fullname=volunteer.fullname,
        age=volunteer.age,
        gender=volunteer.gender,
        mobile=volunteer.mobile,
        email=volunteer.email,
        address=volunteer.address,
        availability=volunteer.availability,
        id_proof_path=getattr(volunteer, "id_proof_path", None)  
    )
    try:
        db.add(new_volunteer)
        db.commit()
        db.refresh(new_volunteer)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {e}")

    return new_volunteer


@router.get("/", response_model=List[schemas.VolunteerResponse])
def read_volunteers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Volunteer).offset(skip).limit(limit).all()


@router.get("/{volunteer_id}", response_model=schemas.VolunteerResponse)
def read_volunteer(volunteer_id: int, db: Session = Depends(database.get_db)):
    volunteer = db.get(models.Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer


@router.put("/{volunteer_id}", response_model=schemas.VolunteerResponse)
def update_volunteer(volunteer_id: int, updated: schemas.VolunteerCreate, db: Session = Depends(database.get_db)):
    volunteer = db.get(models.Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    
    for key, value in updated.dict().items():
        setattr(volunteer, key, value)

    db.commit()
    db.refresh(volunteer)
    return volunteer



@router.delete("/{volunteer_id}")
def delete_volunteer(volunteer_id: int, db: Session = Depends(database.get_db)):
    volunteer = db.get(models.Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    db.delete(volunteer)
    db.commit()
    return {"detail": "Volunteer deleted successfully"}

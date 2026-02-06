from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])


@router.post("/", response_model=schemas.VolunteerResponse)
def create_volunteer(
    volunteer: schemas.VolunteerCreate,
    db: Session = Depends(get_db)
):
    payload = volunteer.model_dump()
    new_volunteer = models.Volunteer(**payload)

    try:
        db.add(new_volunteer)
        db.commit()
        db.refresh(new_volunteer)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database Error while creating volunteer"
        )

    return new_volunteer


@router.get("/", response_model=List[schemas.VolunteerResponse])
def read_volunteers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(models.Volunteer).offset(skip).limit(limit).all()


@router.get("/{volunteer_id}", response_model=schemas.VolunteerResponse)
def read_volunteer(
    volunteer_id: int,
    db: Session = Depends(get_db)
):
    volunteer = db.get(models.Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer


@router.put("/{volunteer_id}", response_model=schemas.VolunteerResponse)
def update_volunteer(
    volunteer_id: int,
    updated: schemas.VolunteerCreate,
    db: Session = Depends(get_db)
):
    volunteer = db.get(models.Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    for key, value in updated.model_dump().items():   
        setattr(volunteer, key, value)

    db.commit()
    db.refresh(volunteer)
    return volunteer



@router.delete("/{volunteer_id}")
def delete_volunteer(
    volunteer_id: int,
    db: Session = Depends(get_db)
):
    volunteer = db.get(models.Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    db.delete(volunteer)
    db.commit()
    return {"detail": "Volunteer deleted successfully"}

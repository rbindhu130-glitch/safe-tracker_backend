from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])


# Create a volunteer
@router.post("/", response_model=schemas.VolunteerResponse)
def create_volunteer(volunteer: schemas.VolunteerCreate, db: Session = Depends(database.get_db)):
    new_volunteer = models.Volunteer(**volunteer.dict())
    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)
    return new_volunteer


# Get all volunteers
@router.get("/", response_model=List[schemas.VolunteerResponse])
def read_volunteers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Volunteer).offset(skip).limit(limit).all()


# Get a single volunteer by ID
@router.get("/{volunteer_id}", response_model=schemas.VolunteerResponse)
def read_volunteer(volunteer_id: int, db: Session = Depends(database.get_db)):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    return volunteer


# Update a volunteer
@router.put("/{volunteer_id}", response_model=schemas.VolunteerResponse)
def update_volunteer(volunteer_id: int, updated: schemas.VolunteerCreate, db: Session = Depends(database.get_db)):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    for key, value in updated.dict().items():
        setattr(volunteer, key, value)
    db.commit()
    db.refresh(volunteer)
    return volunteer


# Delete a volunteer
@router.delete("/{volunteer_id}")
def delete_volunteer(volunteer_id: int, db: Session = Depends(database.get_db)):
    volunteer = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    db.delete(volunteer)
    db.commit()
    return {"detail": "Volunteer deleted successfully"}

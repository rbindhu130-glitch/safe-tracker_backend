from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/incidents", tags=["Incidents"])


# Create an incident
@router.post("/", response_model=schemas.IncidentResponse)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(database.get_db)):
    new_incident = models.Incident(**incident.dict())
    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)
    return new_incident


# Get all incidents
@router.get("/", response_model=List[schemas.IncidentResponse])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.Incident).offset(skip).limit(limit).all()


# Get a single incident by ID
@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def read_incident(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    return incident


# Update an incident
@router.put("/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(incident_id: int, updated: schemas.IncidentCreate, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    for key, value in updated.dict().items():
        setattr(incident, key, value)
    db.commit()
    db.refresh(incident)
    return incident


# Delete an incident
@router.delete("/{incident_id}")
def delete_incident(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    db.delete(incident)
    db.commit()
    return {"detail": "Incident deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/", response_model=schemas.IncidentResponse)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(database.get_db)):
    db_incident = models.Incident(
        location=incident.location,
        category=incident.category,
        description=incident.description,
        contact=incident.contact
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@router.get("/", response_model=List[schemas.IncidentResponse])
def read_incidents(db: Session = Depends(database.get_db)):
    return db.query(models.Incident).all()


@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def read_incident(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident



@router.put("/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(incident_id: int, updated: schemas.IncidentCreate, db: Session = Depends(database.get_db)):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident.location = updated.location
    incident.category = updated.category
    incident.description = updated.description
    incident.contact = updated.contact

    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/{incident_id}", status_code=200)
def delete_incident(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    db.delete(incident)
    db.commit()
    return {"detail": "Incident deleted successfully"}

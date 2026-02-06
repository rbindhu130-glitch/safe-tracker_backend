from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Any, cast
from .. import models, schemas, database
from ..deps import get_current_user

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/", response_model=schemas.IncidentCreateResponse)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    payload = incident.model_dump()
    # ignore any client-supplied status and enforce server-controlled default
    payload.pop("status", None)
    payload["status"] = "pending"
    payload["owner_id"] = current_user.id
    # Create the Incident and attach the owner object so response validation that
    # expects an `owner` object will succeed.
    db_incident = models.Incident(**payload)
    db_incident.owner = current_user
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@router.get("/", response_model=List[schemas.IncidentResponse])
def read_incidents(db: Session = Depends(database.get_db)):
    return db.query(models.Incident).options(joinedload(models.Incident.owner)).all()


@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def read_incident(incident_id: int, db: Session = Depends(database.get_db)):
    incident = db.query(models.Incident).options(joinedload(models.Incident.owner)).filter(models.Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident



@router.put("/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(
    incident_id: int,
    updated: schemas.IncidentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if cast(int, incident.owner_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this incident")
    for key, value in updated.model_dump().items():
        if key in ("owner_id", "status"):
            continue
        setattr(incident, key, value)  # type: ignore[arg-type]

    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/{incident_id}", status_code=200)
def delete_incident(
    incident_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if cast(int, incident.owner_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this incident")

    db.delete(incident)
    db.commit()
    return {"detail": "Incident deleted successfully"}


@router.put("/{incident_id}/status", response_model=schemas.IncidentResponse)
def update_incident_status(
    incident_id: int,
    status_update: schemas.IncidentStatusUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if cast(int, incident.owner_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this incident")

    incident.status = status_update.status  
    db.commit()
    db.refresh(incident)
    return incident

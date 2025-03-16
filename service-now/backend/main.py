from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/incidents", response_model=List[schemas.Incident])
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()
    return incidents


@app.get("/incidents/{incident_id}", response_model=schemas.Incident)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = (
        db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    )
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.post("/incidents", response_model=schemas.Incident, status_code=201)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    db_incident = models.Incident(
        description=incident.description,
        actions_taken=incident.actions_taken,
        status=models.StatusEnum.OPEN,
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@app.put("/incidents/{incident_id}", response_model=schemas.Incident)
def update_incident(
    incident_id: int, incident: schemas.IncidentUpdate, db: Session = Depends(get_db)
):
    db_incident = (
        db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    )
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    for key, value in incident.dict(exclude_unset=True).items():
        setattr(db_incident, key, value)

    db.commit()
    db.refresh(db_incident)
    return db_incident


# fastapi run main.py

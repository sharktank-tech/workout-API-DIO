from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

app = FastAPI()

@app.post("/participants/", response_model=schemas.Participant)
async def create_participant(participant: schemas.ParticipantCreate, db: Session = Depends(database.get_db)):
    db_participant = models.Participant(name=participant.name, age=participant.age, score=participant.score)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

@app.get("/participants/", response_model=List[schemas.Participant])
async def read_participants(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    participants = db.query(models.Participant).offset(skip).limit(limit).all()
    return participants

@app.get("/participants/{participant_id}", response_model=schemas.Participant)
async def read_participant(participant_id: int, db: Session = Depends(database.get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant

@app.put("/participants/{participant_id}", response_model=schemas.Participant)
async def update_participant(participant_id: int, updated_participant: schemas.ParticipantCreate, db: Session = Depends(database.get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    participant.name = updated_participant.name
    participant.age = updated_participant.age
    participant.score = updated_participant.score
    db.commit()
    db.refresh(participant)
    return participant

@app.delete("/participants/{participant_id}", response_model=schemas.Participant)
async def delete_participant(participant_id: int, db: Session = Depends(database.get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    db.delete(participant)
    db.commit()
    return participant

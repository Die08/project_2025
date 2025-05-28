from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from app.data.db import SessionDep
from app.models.event import Event  # creato nel passaggio 1
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    date: datetime
    location: str

    class Config:
        orm_mode = True

@router.get("/events", response_model=List[EventResponse])
def get_events(session: Session = Depends(SessionDep)):
    return session.query(Event).all()

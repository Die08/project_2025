from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session, select
from app.data.db import SessionDep
from app.models.event import Event  # creato nel passaggio 1
from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException
from app.models.registration import Registration
from app.models.user import User

router = APIRouter()

class EventCreate(BaseModel):
    title: str
    description: str
    date: datetime
    location: str

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    date: datetime
    location: str

    class Config:
        orm_mode = True

class RegistrationRequest(BaseModel):
    username: str
    name: str
    email: str


@router.get("/events", response_model=List[EventResponse])
def get_events(session: Session = Depends(SessionDep)):
    return session.exec(select(Event)).all()

@router.post("/events", response_model=EventResponse)
def create_event(event: EventCreate, session: Session = Depends(SessionDep)):
    new_event = Event(**event.dict())
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event


@router.get("/events/{id}", response_model=EventResponse)
def get_event_by_id(id: int, session: Session = Depends(SessionDep)):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{id}", response_model=EventResponse)
def update_event(id: int, updated_event: EventCreate, session: Session = Depends(SessionDep)):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = updated_event.title
    event.description = updated_event.description
    event.date = updated_event.date
    event.location = updated_event.location

    session.add(event)
    session.commit()
    session.refresh(event)
    return event



@router.post("/events/{id}/register")
def register_user_to_event(id: int, reg: RegistrationRequest, session: Session = Depends(SessionDep)):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    user = session.get(User, reg.username)
    if not user:
        user = User(**reg.dict())
        session.add(user)

    # Verifica se già registrato
    existing = session.get(Registration, (reg.username, id))
    if existing:
        raise HTTPException(status_code=400, detail="User already registered")

    registration = Registration(username=reg.username, event_id=id)
    session.add(registration)
    session.commit()

    return {"message": f"User '{reg.username}' registered to event {id}"}

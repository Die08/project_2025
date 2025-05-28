from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.data.db import SessionDep
from app.models.registration import Registration
from pydantic import BaseModel

router = APIRouter()

class RegistrationResponse(BaseModel):
    username: str
    event_id: int

    class Config:
        from_attributes = True  # per compatibilità con Pydantic v2

@router.get("/registrations", response_model=List[RegistrationResponse])
def get_registrations(session: Session = Depends(SessionDep)):
    return session.exec(select(Registration)).all()

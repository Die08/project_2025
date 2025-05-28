from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.models.user import User
from app.data.db import SessionDep
from pydantic import BaseModel
from fastapi import HTTPException
from app.models.user import User

router = APIRouter()

class UserResponse(BaseModel):
    username: str
    name: str
    email: str

    class Config:
        from_attributes = True  # per compatibilità con Pydantic v2

@router.get("/users", response_model=List[UserResponse])
def get_users(session: Session = Depends(SessionDep)):
    return session.exec(select(User)).all()



@router.post("/users", response_model=UserResponse)
def create_user(user: UserResponse, session: Session = Depends(SessionDep)):
    existing_user = session.get(User, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/users/{username}", response_model=UserResponse)
def get_user_by_username(username: str, session: Session = Depends(SessionDep)):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

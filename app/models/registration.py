# app/models/registration.py

from sqlmodel import SQLModel, Field

class Registration(SQLModel, table=True):
    username: str = Field(foreign_key="user.username", primary_key=True)
    event_id: int = Field(foreign_key="event.id", primary_key=True)

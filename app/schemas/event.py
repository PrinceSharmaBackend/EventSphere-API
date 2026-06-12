from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    event_date: datetime


class EventUpdate(BaseModel):
    title: str
    description: str
    location: str
    event_date: datetime
    

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    event_date: datetime
    organizer_id: int

    class Config:
        from_attributes = True



from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    name: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class EventResponse(EventCreate):
    event_id: int
    status: str

    class Config:
        from_attributes = True

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class AttendeeResponse(AttendeeCreate):
    attendee_id: int
    event_id: int
    check_in_status: bool

    class Config:
        from_attributes = True

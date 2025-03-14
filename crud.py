from sqlalchemy.orm import Session
from models import Event, Attendee, EventStatus
from schemas import EventCreate, AttendeeCreate

def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def register_attendee(db: Session, event_id: int, attendee: AttendeeCreate):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event or len(event.attendees) >= event.max_attendees:
        return None  # Event full or not found
    db_attendee = Attendee(**attendee.dict(), event_id=event_id)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee

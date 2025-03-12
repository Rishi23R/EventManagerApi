from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from crud import create_event
from schemas import EventCreate, EventResponse
from typing import Optional, List
from models import Event, EventStatus
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=EventResponse)
def add_event(event: EventCreate, db: Session = Depends(get_db)):
    return create_event(db, event)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/filter/", response_model=List[EventResponse])
def list_events(
        db: Session = Depends(get_db),
        event_id: Optional[int] = Query(None),
        status: Optional[str] = Query(None),
        location: Optional[str] = Query(None)
):
    query = db.query(Event)

    if status:
        query = query.filter(Event.status == status)
    if location:
        query = query.filter(Event.location == location)
    if event_id:
        query = query.filter(Event.event_id == event_id)

    return query.all()


@router.put("/{event_id}")
def update_event(
        event_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        location: Optional[str] = None,
        max_attendees: Optional[int] = None,
        status: Optional[EventStatus] = None,
        db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.event_id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Update only provided fields
    if name: event.name = name
    if description: event.description = description
    if start_time: event.start_time = start_time
    if end_time: event.end_time = end_time
    if location: event.location = location
    if max_attendees: event.max_attendees = max_attendees
    if status: event.status = status

    db.commit()
    db.refresh(event)

    return {"message": "Event updated successfully", "event": event}

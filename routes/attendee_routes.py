from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from database import get_db
from crud import register_attendee
from schemas import AttendeeCreate, AttendeeResponse
from typing import List, Optional
import csv
from models import Attendee
from io import StringIO

router = APIRouter()


@router.post("/{event_id}/register", response_model=AttendeeResponse)
def add_attendee(event_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db)):
    registered = register_attendee(db, event_id, attendee)
    if not registered:
        raise HTTPException(status_code=400, detail="Event full or not found")
    return registered


@router.get("/{event_id}/attendees", response_model=List[AttendeeResponse])
def list_attendees(
        event_id: int,
        db: Session = Depends(get_db),
        checked_in: Optional[bool] = Query(None),
):
    query = db.query(Attendee).filter(Attendee.event_id == event_id)

    if checked_in is not None:
        query = query.filter(Attendee.check_in_status == checked_in)

    return query.all()


@router.post("/{event_id}/bulk_checkin")
def bulk_checkin(event_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))

    updated_count = 0
    for row in reader:
        attendee = db.query(Attendee).filter(Attendee.email == row["email"], Attendee.event_id == event_id).first()
        if attendee:
            attendee.check_in_status = row["check_in_status"].lower() == "true"
            db.commit()
            updated_count += 1

    return {"message": f"{updated_count} attendees checked in successfully"}


@router.put("/check-in/{attendee_id}")
def check_in_attendee(attendee_id: int, db: Session = Depends(get_db)):
    try:
        print(f"Searching for attendee with ID: {attendee_id}")
        attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()

        if not attendee:
            print("Attendee not found")
            raise HTTPException(status_code=404, detail="Attendee not found")

        if attendee.check_in_status:
            print("Attendee already checked in")
            raise HTTPException(status_code=400, detail="Attendee already checked in")

        print("Updating check-in status...")
        attendee.check_in_status = True
        db.commit()
        db.refresh(attendee)

        print(f"Attendee {attendee.first_name} checked in successfully")
        return {"message": f"Attendee {attendee.first_name} checked in successfully"}

    except Exception as e:
        db.rollback()
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error")

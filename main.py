import asyncio
from fastapi import FastAPI
from datetime import datetime
from database import SessionLocal
from routes import event_routes, attendee_routes
from models import Event, EventStatus

app = FastAPI(title="Event Management API")

# Include routes
app.include_router(event_routes.router, prefix="/events", tags=["Events"])
app.include_router(attendee_routes.router, prefix="/attendees", tags=["Attendees"])

# Run server with:
# uvicorn main:app --reload

async def update_event_status():
    while True:
        db = SessionLocal()
        events = db.query(Event).filter(Event.end_time < datetime.utcnow(), Event.status != EventStatus.completed).all()

        for event in events:
            event.status = EventStatus.completed
        db.commit()
        db.close()

        await asyncio.sleep(60)  # Run every 60 seconds


@app.on_event("startup")
async def startup_event(): asyncio.create_task(update_event_status())
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import MemoryCard, Task, Trip
from app.schemas import CardGenerate, CardOut

router = APIRouter(prefix="/api/cards", tags=["cards"])


@router.post("/generate", response_model=CardOut)
def generate_card(payload: CardGenerate, db: Session = Depends(get_db)):
    trip = db.get(Trip, payload.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    tasks = db.scalars(select(Task).where(Task.trip_id == payload.trip_id)).all()
    completed_tasks = [t.title for t in tasks if t.status == "completed"]
    summary = f"Trip to {trip.destination} on {trip.travel_date}. Completed tasks: {', '.join(completed_tasks) if completed_tasks else 'none yet'}."

    card_data = {
        "pilot_city": "Chongqing",
        "destination": trip.destination,
        "travel_date": str(trip.travel_date),
        "completed_tasks": completed_tasks,
    }
    row = MemoryCard(
        trip_id=payload.trip_id,
        title=payload.title,
        summary=summary,
        image_url=payload.image_url,
        card_json=json.dumps(card_data, ensure_ascii=True),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    row = db.get(MemoryCard, card_id)
    if not row:
        raise HTTPException(status_code=404, detail="Card not found")
    return row

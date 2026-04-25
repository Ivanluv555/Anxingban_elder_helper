from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Profile, Trip
from app.schemas import TripCreate, TripOut
from app.services.pass_token import create_dynamic_pass

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.post("", response_model=TripOut)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)):
    profile = db.get(Profile, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    temp_trip = Trip(
        profile_id=payload.profile_id,
        destination=payload.destination,
        travel_date=payload.travel_date,
        pass_token="pending",
        pass_qr_svg="pending",
    )
    db.add(temp_trip)
    db.flush()

    token, qr_svg = create_dynamic_pass(settings.token_secret, payload.profile_id, temp_trip.id)
    temp_trip.pass_token = token
    temp_trip.pass_qr_svg = qr_svg

    db.commit()
    db.refresh(temp_trip)
    return temp_trip


@router.get("/{trip_id}/pass", response_model=TripOut)
def get_trip_pass(trip_id: int, db: Session = Depends(get_db)):
    row = db.get(Trip, trip_id)
    if not row:
        raise HTTPException(status_code=404, detail="Trip not found")
    return row

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.trip.dto.TripDto import TripCreateDto, TripResponseDto
from app.modules.trip.service.TripService import TripService
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/trips", tags=["trips"])


@router.post("", response_model=TripResponseDto)
def create_trip(payload: TripCreateDto, db: Session = Depends(get_db)):
    if not ProfileService.get_profile_by_id(db, payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found")

    trip = TripService.create_trip(db, payload.profile_id, payload.destination, payload.travel_date)
    return trip


@router.get("/{trip_id}", response_model=TripResponseDto)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.get("/{trip_id}/pass", response_model=TripResponseDto)
def get_trip_pass(trip_id: int, db: Session = Depends(get_db)):
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.get("/profile/{profile_id}", response_model=list[TripResponseDto])
def list_trips_by_profile(profile_id: int, db: Session = Depends(get_db)):
    return TripService.list_trips_by_profile(db, profile_id)

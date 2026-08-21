from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.sos.dto.SosDto import SosRequestDto, SosResponseDto
from app.modules.sos.service.SosService import SosService
from app.modules.profile.service.ProfileService import ProfileService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/sos", tags=["sos"])


@router.post("/trigger", response_model=SosResponseDto)
async def trigger_sos(payload: SosRequestDto, db: Session = Depends(get_db)):
    profile = ProfileService.get_profile_by_id(db, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if payload.trip_id is not None and not TripService.get_trip_by_id(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")

    sos_record = await SosService.trigger_sos(
        db,
        payload.profile_id,
        payload.trip_id,
        payload.latitude,
        payload.longitude,
        payload.network_status,
        profile,
    )
    return sos_record


@router.get("/profile/{profile_id}", response_model=list[SosResponseDto])
def list_sos_records(profile_id: int, db: Session = Depends(get_db)):
    return SosService.list_sos_by_profile(db, profile_id)

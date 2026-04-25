from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Profile, SOSRecord, Trip
from app.schemas import SOSOut, SOSRequest
from app.services.notification import send_dual_channel

router = APIRouter(prefix="/api/sos", tags=["sos"])


@router.post("/trigger", response_model=SOSOut)
async def trigger_sos(payload: SOSRequest, db: Session = Depends(get_db)):
    profile = db.get(Profile, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if payload.trip_id is not None and not db.get(Trip, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")

    message = (
        f"Emergency alert for {profile.parent_name} in {settings.pilot_city}. "
        f"Location=({payload.latitude},{payload.longitude}), network={payload.network_status}."
    )

    result = await send_dual_channel(
        child_phone=profile.child_phone,
        wechat_webhook_url=profile.wechat_webhook_url or settings.wechat_webhook_url,
        message=message,
        sms_provider=settings.sms_provider,
    )

    row = SOSRecord(
        profile_id=payload.profile_id,
        trip_id=payload.trip_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        network_status=payload.network_status,
        health_snapshot=profile.health_info,
        sms_status=result.sms_status,
        wechat_status=result.wechat_status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profile
from app.schemas import ProfileCreate, ProfileOut

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.get("", response_model=list[ProfileOut])
def list_profiles(limit: int = 20, db: Session = Depends(get_db)):
    safe_limit = max(1, min(limit, 100))
    rows = db.scalars(select(Profile).order_by(Profile.id.desc()).limit(safe_limit)).all()
    return list(rows)


@router.post("", response_model=ProfileOut)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    health_info = {
        "chronic_diseases": payload.chronic_diseases,
        "allergies": payload.allergies,
        "mobility_limitations": payload.mobility_limitations,
    }
    row = Profile(
        parent_name=payload.parent_name,
        parent_phone=payload.parent_phone,
        child_name=payload.child_name,
        child_phone=payload.child_phone,
        health_info=json.dumps(health_info, ensure_ascii=True),
        interests=payload.interests,
        wechat_webhook_url=payload.wechat_webhook_url,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    row = db.get(Profile, profile_id)
    if not row:
        raise HTTPException(status_code=404, detail="Profile not found")
    return row

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.profile.dto.ProfileDto import (
    ProfileCreateDto,
    ProfileResponseDto,
    ProfileUpdateDto,
)
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.get("", response_model=list[ProfileResponseDto])
def list_profiles(limit: int = 20, db: Session = Depends(get_db)):
    return ProfileService.list_profiles(db, limit)


@router.post("", response_model=ProfileResponseDto)
def create_profile(payload: ProfileCreateDto, db: Session = Depends(get_db)):
    profile = ProfileService.create_profile(
        db,
        payload.parent_name,
        payload.parent_phone,
        payload.child_name,
        payload.child_phone,
        payload.chronic_diseases,
        payload.allergies,
        payload.mobility_limitations,
        payload.interests,
        payload.wechat_webhook_url,
    )
    return profile


@router.get("/{profile_id}", response_model=ProfileResponseDto)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/{profile_id}", response_model=ProfileResponseDto)
def update_profile(profile_id: int, payload: ProfileUpdateDto, db: Session = Depends(get_db)):
    update_data = payload.model_dump(exclude_unset=True)
    profile = ProfileService.update_profile(db, profile_id, **update_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

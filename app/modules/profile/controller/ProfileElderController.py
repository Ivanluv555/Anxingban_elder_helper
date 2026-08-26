from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_elder
from app.modules.profile.dto.ProfileDto import ProfileResponseDto
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/elder/profiles", tags=["老人-档案管理"])


@router.get(
    "/{profile_id}",
    response_model=ProfileResponseDto,
    summary="获取档案详情",
    description="老人用户获取指定档案详情"
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取档案详情"""
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")
    return profile


@router.get(
    "",
    response_model=list[ProfileResponseDto],
    summary="获取档案列表",
    description="老人用户获取档案列表"
)
def list_profiles(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取档案列表"""
    return ProfileService.list_profiles(db, limit)

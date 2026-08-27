from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_elder
from app.modules.profile.dto.ProfileDto import ProfileResponseDto
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/elder/profiles", tags=["老人-档案管理"])

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

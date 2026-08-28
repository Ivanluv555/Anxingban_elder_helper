from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.modules.auth.dependencies import get_current_elder
from app.modules.profile.dto.ProfileDto import ProfileResponseDto
from app.modules.profile.repository.ProfileRepository import ProfileRepository

router = APIRouter(prefix="/api/elder/profiles", tags=["老人-档案管理"])


@router.get(
    "",
    response_model=list[ProfileResponseDto],
    summary="获取档案列表",
    description="老人用户获取自己关联的档案列表"
)
def list_profiles(
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取档案列表 - 老人只能查看自己相关的档案"""
    repo = ProfileRepository(db)
    return repo.find_by_elder(current_elder.id)

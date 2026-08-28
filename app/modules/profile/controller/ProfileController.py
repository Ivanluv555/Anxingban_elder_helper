from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_user
from app.modules.profile.dto.ProfileDto import ProfileCreateDto, ProfileResponseDto
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/user/profiles", tags=["子女-档案管理"])


@router.get(
    "",
    response_model=list[ProfileResponseDto],
    summary="获取档案列表",
    description="查询当前用户的家庭档案列表"
)
def list_profiles(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取档案列表 - 只返回当前子女用户关联的档案"""
    return ProfileService.list_profiles(db, current_user.id, limit)


@router.post(
    "",
    response_model=ProfileResponseDto,
    summary="创建家庭档案",
    description="扫码场景：子女扫描老人二维码后创建关联档案"
)
def create_profile(
    payload: ProfileCreateDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建家庭档案 - 扫码后关联老人和子女"""
    profile = ProfileService.create_profile(
        db,
        elder_id=payload.elder_id,
        user_id=current_user.id,
    )
    return profile


@router.delete(
    "/{profile_id}",
    summary="删除档案"
)
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除档案"""
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="档案不存在")
    if profile.user_id != current_user.id:
        raise BusinessException(ErrorCode.FORBIDDEN, detail="无权删除此档案")
    
    ProfileService.delete_profile(db, profile_id)
    return {"message": "档案删除成功"}

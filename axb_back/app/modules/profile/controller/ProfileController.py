"""档案控制器 - 子女用户端"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_user
from app.modules.profile.dto.ProfileDto import (
    ProfileCreateDto,
    ProfileUpdateDto,
    ProfileResponseDto
)
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/user/profiles", tags=["子女-档案管理"])


@router.post(
    "",
    response_model=ProfileResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="创建档案关联"
)
def create_profile(
    request: ProfileCreateDto,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """创建档案关联"""
    profile = ProfileService.create_profile(db, request)
    return profile


@router.get(
    "",
    response_model=list[ProfileResponseDto],
    summary="获取档案列表"
)
def list_profiles(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """获取当前用户的档案列表"""
    profiles = ProfileService.list_profiles_by_user(db, current_user.id, limit)
    return profiles


@router.get(
    "/{profile_id}",
    response_model=ProfileResponseDto,
    summary="获取档案详情"
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """获取档案详情"""
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="档案不存在")
    return profile


@router.patch(
    "/{profile_id}",
    response_model=ProfileResponseDto,
    summary="更新档案信息（PATCH）"
)
@router.put(
    "/{profile_id}",
    response_model=ProfileResponseDto,
    summary="更新档案信息（PUT）"
)
def update_profile(
    profile_id: int,
    request: ProfileUpdateDto,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """更新档案信息"""
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="档案不存在")

    updated_profile = ProfileService.update_profile(db, profile, request)
    return updated_profile


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除档案"
)
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """删除档案"""
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="档案不存在")

    ProfileService.delete_profile(db, profile)
    return None

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.profile.dto.ProfileDto import (
    ProfileCreateDto,
    ProfileResponseDto,
    ProfileUpdateDto,
)
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/profiles", tags=["档案管理"])


@router.get(
    "",
    response_model=list[ProfileResponseDto],
    summary="获取档案列表",
    description="查询家庭档案列表，支持分页限制",
    response_description="返回档案列表，按创建时间倒序排列"
)
def list_profiles(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取档案列表
    
    - **limit**: 返回数量限制，默认 20，最大 100
    """
    return ProfileService.list_profiles(db, limit)


@router.post(
    "",
    response_model=ProfileResponseDto,
    summary="创建家庭档案",
    description="创建新的家庭协同建档，记录长辈和子女信息、健康状况、兴趣偏好",
    response_description="返回创建成功的档案信息，包含自动生成的档案 ID"
)
def create_profile(payload: ProfileCreateDto, db: Session = Depends(get_db)):
    """创建家庭档案
    
    记录内容：
    - 长辈信息：姓名、联系方式
    - 子女信息：姓名、联系方式
    - 健康档案：慢性病、过敏史、行动能力
    - 兴趣偏好：文化、美食等
    - 通知渠道：企业微信 Webhook（可选）
    """
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


@router.get(
    "/{profile_id}",
    response_model=ProfileResponseDto,
    summary="获取单个档案详情",
    description="根据档案 ID 查询档案完整信息",
    response_description="返回档案详细信息"
)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """获取档案详情
    
    - **profile_id**: 档案 ID
    
    错误：
    - 404: 档案不存在
    """
    profile = ProfileService.get_profile_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")
    return profile


@router.patch(
    "/{profile_id}",
    response_model=ProfileResponseDto,
    summary="更新档案信息",
    description="部分更新档案信息，仅更新提供的字段",
    response_description="返回更新后的档案信息"
)
def update_profile(profile_id: int, payload: ProfileUpdateDto, db: Session = Depends(get_db)):
    """更新档案信息
    
    - **profile_id**: 档案 ID
    - 支持部分更新，未提供的字段保持不变
    - 可更新联系方式、健康信息、兴趣偏好
    
    错误：
    - 404: 档案不存在
    """
    update_data = payload.model_dump(exclude_unset=True)
    profile = ProfileService.update_profile(db, profile_id, **update_data)
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")
    return profile

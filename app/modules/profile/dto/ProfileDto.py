from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreateDto(BaseModel):
    """创建档案DTO - 扫码场景，只需要关联的用户ID"""
    elder_id: int = Field(gt=0, description="老人用户ID")


class ProfileUpdateDto(BaseModel):
    """更新档案DTO - 目前无需更新"""
    pass


class ProfileResponseDto(BaseModel):
    """档案响应DTO"""
    id: int
    elder_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

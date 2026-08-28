from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreateDto(BaseModel):
    profile_id: int
    trip_id: int
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=1000)


class TaskCompleteDto(BaseModel):
    feedback: str = Field(default="", max_length=500, description="完成反馈")


class TaskResponseDto(BaseModel):
    id: int
    profile_id: int
    trip_id: int
    title: str
    description: str
    user_completed: bool
    elder_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskDetailDto(BaseModel):
    """任务详情DTO - 包含反馈和完成时间"""
    id: int
    profile_id: int
    trip_id: int
    title: str
    description: str
    user_completed: bool
    user_feedback: Optional[str]
    elder_completed: bool
    elder_feedback: Optional[str]
    created_at: datetime
    user_completed_at: Optional[datetime]
    elder_completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

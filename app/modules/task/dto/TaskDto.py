from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreateDto(BaseModel):
    profile_id: int
    trip_id: int
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=1000)


class TaskCompleteDto(BaseModel):
    completed_note: str = Field(default="", max_length=500)
    photo_url: str = Field(default="", max_length=400)


class TaskFeedbackDto(BaseModel):
    feedback_text: str = Field(default="", max_length=500)
    hearts_delta: int = Field(default=1, ge=-10, le=10)


class TaskResponseDto(BaseModel):
    id: int
    profile_id: int
    trip_id: int
    title: str
    description: str
    status: str
    completed_note: Optional[str] = None
    photo_url: Optional[str] = None
    feedback_text: Optional[str] = None
    hearts: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

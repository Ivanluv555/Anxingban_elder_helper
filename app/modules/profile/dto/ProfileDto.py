from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreateDto(BaseModel):
    parent_name: str = Field(min_length=1, max_length=80)
    parent_phone: str = Field(min_length=5, max_length=30)
    child_name: str = Field(min_length=1, max_length=80)
    child_phone: str = Field(min_length=5, max_length=30)
    chronic_diseases: str = ""
    allergies: str = ""
    mobility_limitations: str = ""
    interests: str = "culture,food"
    wechat_webhook_url: str = ""


class ProfileUpdateDto(BaseModel):
    parent_name: Optional[str] = Field(None, min_length=1, max_length=80)
    parent_phone: Optional[str] = Field(None, min_length=5, max_length=30)
    child_name: Optional[str] = Field(None, min_length=1, max_length=80)
    child_phone: Optional[str] = Field(None, min_length=5, max_length=30)
    chronic_diseases: Optional[str] = None
    allergies: Optional[str] = None
    mobility_limitations: Optional[str] = None
    interests: Optional[str] = None
    wechat_webhook_url: Optional[str] = None


class ProfileResponseDto(BaseModel):
    id: int
    parent_name: str
    parent_phone: str
    child_name: str
    child_phone: str
    health_info: str
    interests: str
    wechat_webhook_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SosRequestDto(BaseModel):
    profile_id: int
    trip_id: Optional[int] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    network_status: str = Field(default="online", max_length=30)


class SosResponseDto(BaseModel):
    id: int
    profile_id: int
    trip_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    network_status: str
    health_snapshot: str
    sms_status: str
    wechat_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TripCreateDto(BaseModel):
    profile_id: int
    destination: str = Field(min_length=1, max_length=120)
    travel_date: date


class TripResponseDto(BaseModel):
    """行程响应DTO - 列表使用，不包含二维码"""
    id: int
    profile_id: int
    destination: str
    travel_date: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TripDetailDto(BaseModel):
    """行程详情DTO - 包含通行码二维码"""
    id: int
    profile_id: int
    destination: str
    travel_date: date
    pass_token: str
    pass_qr_svg: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

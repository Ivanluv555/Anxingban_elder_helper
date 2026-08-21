from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TripCreateDto(BaseModel):
    profile_id: int
    destination: str = Field(min_length=1, max_length=120)
    travel_date: date


class TripResponseDto(BaseModel):
    id: int
    profile_id: int
    destination: str
    travel_date: date
    pass_token: str
    pass_qr_svg: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

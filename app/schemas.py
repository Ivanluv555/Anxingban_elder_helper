from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    parent_name: str = Field(min_length=1, max_length=80)
    parent_phone: str = Field(min_length=5, max_length=30)
    child_name: str = Field(min_length=1, max_length=80)
    child_phone: str = Field(min_length=5, max_length=30)
    chronic_diseases: str = ""
    allergies: str = ""
    mobility_limitations: str = ""
    interests: str = "culture,food"
    wechat_webhook_url: str = ""


class ProfileOut(BaseModel):
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


class TripCreate(BaseModel):
    profile_id: int
    destination: str
    travel_date: date


class TripOut(BaseModel):
    id: int
    profile_id: int
    destination: str
    travel_date: date
    pass_token: str
    pass_qr_svg: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    profile_id: int
    trip_id: int
    title: str
    description: str


class TaskComplete(BaseModel):
    completed_note: str = ""
    photo_url: str = ""


class TaskFeedback(BaseModel):
    feedback_text: str = ""
    hearts_delta: int = 1


class TaskOut(BaseModel):
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


class SOSRequest(BaseModel):
    profile_id: int
    trip_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    network_status: str = "online"


class SOSOut(BaseModel):
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


class GuideAsk(BaseModel):
    question: str


class GuideAnswer(BaseModel):
    answer: str
    confidence: float
    scope: str


class CardGenerate(BaseModel):
    trip_id: int
    title: str = "Travel Memory Card"
    image_url: str = ""


class CardOut(BaseModel):
    id: int
    trip_id: int
    title: str
    summary: str
    image_url: Optional[str] = None
    card_json: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

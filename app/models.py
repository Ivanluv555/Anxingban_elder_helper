from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    parent_name: Mapped[str] = mapped_column(String(80), nullable=False)
    parent_phone: Mapped[str] = mapped_column(String(30), nullable=False)
    child_name: Mapped[str] = mapped_column(String(80), nullable=False)
    child_phone: Mapped[str] = mapped_column(String(30), nullable=False)
    health_info: Mapped[str] = mapped_column(Text, nullable=False)
    interests: Mapped[str] = mapped_column(Text, nullable=False)
    wechat_webhook_url: Mapped[str] = mapped_column(String(300), nullable=True, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(120), nullable=False)
    travel_date: Mapped[date] = mapped_column(Date, nullable=False)
    pass_token: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    pass_qr_svg: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    completed_note: Mapped[str] = mapped_column(Text, nullable=True)
    photo_url: Mapped[str] = mapped_column(String(400), nullable=True)
    feedback_text: Mapped[str] = mapped_column(Text, nullable=True)
    hearts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class SOSRecord(Base):
    __tablename__ = "sos_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    network_status: Mapped[str] = mapped_column(String(30), nullable=False)
    health_snapshot: Mapped[str] = mapped_column(Text, nullable=False)
    sms_status: Mapped[str] = mapped_column(String(30), nullable=False)
    wechat_status: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class MemoryCard(Base):
    __tablename__ = "memory_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(400), nullable=True)
    card_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

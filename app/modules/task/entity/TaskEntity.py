from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.utils.database import Base


class TaskEntity(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"), nullable=False, index=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    user_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    elder_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    elder_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    elder_completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

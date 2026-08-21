from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProfileEntity(Base):
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

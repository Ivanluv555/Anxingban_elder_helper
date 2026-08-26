from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ElderEntity(Base):
    __tablename__ = "elders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    health_info: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    interests: Mapped[str] = mapped_column(Text, nullable=False, default="")
    wechat_webhook_url: Mapped[str] = mapped_column(String(300), nullable=True, default="")
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

"""档案实体"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProfileEntity(Base):
    """家庭档案表"""

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment="关联的子女用户ID")
    elder_id: Mapped[int] = mapped_column(Integer, ForeignKey("elders.id"), nullable=False, comment="关联的老人ID")
    relationship: Mapped[str] = mapped_column(String(50), nullable=False, comment="关系（如：父亲、母亲）")
    emergency_contact: Mapped[str | None] = mapped_column(String(20), nullable=True, comment="紧急联系人电话")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True, comment="备注信息")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    def __repr__(self):
        return f"<ProfileEntity(id={self.id}, user_id={self.user_id}, elder_id={self.elder_id})>"

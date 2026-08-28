from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.profile.entity.ProfileEntity import ProfileEntity


class ProfileRepository:
    """Profile 数据访问层"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, profile_id: int) -> ProfileEntity | None:
        """根据ID查询档案"""
        return self.db.get(ProfileEntity, profile_id)
    
    def find_all(self, limit: int = 20) -> list[ProfileEntity]:
        """查询所有档案"""
        safe_limit = max(1, min(limit, 100))
        return list(self.db.scalars(
            select(ProfileEntity)
            .order_by(ProfileEntity.id.desc())
            .limit(safe_limit)
        ).all())
    
    def create(self, profile: ProfileEntity) -> ProfileEntity:
        """创建档案"""
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    def update(self, profile: ProfileEntity) -> ProfileEntity:
        """更新档案"""
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    def delete(self, profile: ProfileEntity) -> None:
        """删除档案"""
        self.db.delete(profile)
        self.db.commit()

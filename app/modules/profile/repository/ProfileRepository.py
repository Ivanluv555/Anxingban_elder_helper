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
    
    def find_by_user(self, user_id: int, limit: int = 20) -> list[ProfileEntity]:
        """根据子女用户ID查询档案列表"""
        safe_limit = max(1, min(limit, 100))
        return list(self.db.scalars(
            select(ProfileEntity)
            .where(ProfileEntity.user_id == user_id)
            .order_by(ProfileEntity.id.desc())
            .limit(safe_limit)
        ).all())
    
    def find_by_elder(self, elder_id: int) -> list[ProfileEntity]:
        """根据老人用户ID查询档案列表"""
        return list(self.db.scalars(
            select(ProfileEntity)
            .where(ProfileEntity.elder_id == elder_id)
            .order_by(ProfileEntity.id.desc())
        ).all())
    
    def create(self, profile: ProfileEntity) -> ProfileEntity:
        """创建档案"""
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    def delete(self, profile: ProfileEntity) -> None:
        """删除档案"""
        self.db.delete(profile)
        self.db.commit()

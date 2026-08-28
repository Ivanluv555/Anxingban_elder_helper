from sqlalchemy.orm import Session

from app.modules.profile.entity.ProfileEntity import ProfileEntity
from app.modules.profile.repository.ProfileRepository import ProfileRepository


class ProfileService:
    @staticmethod
    def list_profiles(db: Session, user_id: int, limit: int = 20) -> list[ProfileEntity]:
        """获取指定用户的档案列表"""
        repo = ProfileRepository(db)
        return repo.find_by_user(user_id, limit)

    @staticmethod
    def get_profile_by_id(db: Session, profile_id: int) -> ProfileEntity | None:
        repo = ProfileRepository(db)
        return repo.find_by_id(profile_id)

    @staticmethod
    def create_profile(db: Session, elder_id: int, user_id: int) -> ProfileEntity:
        """创建档案 - 扫码场景，关联老人和子女"""
        repo = ProfileRepository(db)
        profile = ProfileEntity(
            elder_id=elder_id,
            user_id=user_id,
        )
        return repo.create(profile)

    @staticmethod
    def delete_profile(db: Session, profile_id: int) -> None:
        repo = ProfileRepository(db)
        profile = repo.find_by_id(profile_id)
        if profile:
            repo.delete(profile)

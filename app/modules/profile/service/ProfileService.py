import json

from sqlalchemy.orm import Session

from app.modules.profile.entity.ProfileEntity import ProfileEntity
from app.modules.profile.repository.ProfileRepository import ProfileRepository


class ProfileService:
    @staticmethod
    def list_profiles(db: Session, limit: int = 20) -> list[ProfileEntity]:
        repo = ProfileRepository(db)
        return repo.find_all(limit)

    @staticmethod
    def get_profile_by_id(db: Session, profile_id: int) -> ProfileEntity | None:
        repo = ProfileRepository(db)
        return repo.find_by_id(profile_id)

    @staticmethod
    def create_profile(
        db: Session,
        parent_name: str,
        parent_phone: str,
        child_name: str,
        child_phone: str,
        chronic_diseases: str,
        allergies: str,
        mobility_limitations: str,
        interests: str,
        wechat_webhook_url: str,
    ) -> ProfileEntity:
        repo = ProfileRepository(db)
        health_info = {
            "chronic_diseases": chronic_diseases,
            "allergies": allergies,
            "mobility_limitations": mobility_limitations,
        }
        profile = ProfileEntity(
            parent_name=parent_name,
            parent_phone=parent_phone,
            child_name=child_name,
            child_phone=child_phone,
            health_info=json.dumps(health_info, ensure_ascii=True),
            interests=interests,
            wechat_webhook_url=wechat_webhook_url,
        )
        return repo.create(profile)

    @staticmethod
    def update_profile(db: Session, profile_id: int, **kwargs) -> ProfileEntity | None:
        repo = ProfileRepository(db)
        profile = repo.find_by_id(profile_id)
        if not profile:
            return None

        if any(k in kwargs for k in ["chronic_diseases", "allergies", "mobility_limitations"]):
            current_health = json.loads(profile.health_info) if profile.health_info else {}
            if "chronic_diseases" in kwargs:
                current_health["chronic_diseases"] = kwargs.pop("chronic_diseases")
            if "allergies" in kwargs:
                current_health["allergies"] = kwargs.pop("allergies")
            if "mobility_limitations" in kwargs:
                current_health["mobility_limitations"] = kwargs.pop("mobility_limitations")
            profile.health_info = json.dumps(current_health, ensure_ascii=True)

        for key, value in kwargs.items():
            if value is not None and hasattr(profile, key):
                setattr(profile, key, value)

        return repo.update(profile)

    @staticmethod
    def delete_profile(db: Session, profile_id: int) -> None:
        repo = ProfileRepository(db)
        profile = repo.find_by_id(profile_id)
        if profile:
            repo.delete(profile)

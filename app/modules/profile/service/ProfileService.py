import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.profile.entity.ProfileEntity import ProfileEntity


class ProfileService:
    @staticmethod
    def list_profiles(db: Session, limit: int = 20) -> list[ProfileEntity]:
        safe_limit = max(1, min(limit, 100))
        return list(db.scalars(select(ProfileEntity).order_by(ProfileEntity.id.desc()).limit(safe_limit)).all())

    @staticmethod
    def get_profile_by_id(db: Session, profile_id: int) -> ProfileEntity | None:
        return db.get(ProfileEntity, profile_id)

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
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update_profile(db: Session, profile_id: int, **kwargs) -> ProfileEntity | None:
        profile = db.get(ProfileEntity, profile_id)
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

        db.commit()
        db.refresh(profile)
        return profile

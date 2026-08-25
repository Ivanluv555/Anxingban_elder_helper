from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.modules.sos.entity.SosRecordEntity import SosRecordEntity
from app.services.notification import send_dual_channel


class SosService:
    @staticmethod
    async def trigger_sos(
        db: Session,
        profile_id: int,
        trip_id: int | None,
        latitude: float | None,
        longitude: float | None,
        network_status: str,
        profile_entity,
    ) -> SosRecordEntity:
        message = (
            f"Emergency alert for {profile_entity.parent_name} in {settings.pilot_city}. "
            f"Location=({latitude},{longitude}), network={network_status}."
        )

        result = await send_dual_channel(
            child_phone=profile_entity.child_phone,
            wechat_webhook_url=profile_entity.wechat_webhook_url or settings.wechat_webhook_url,
            message=message,
            sms_provider=settings.sms_provider,
        )

        sos_record = SosRecordEntity(
            profile_id=profile_id,
            trip_id=trip_id,
            latitude=latitude,
            longitude=longitude,
            network_status=network_status,
            health_snapshot=profile_entity.health_info,
            sms_status=result.sms_status,
            wechat_status=result.wechat_status,
        )
        db.add(sos_record)
        db.commit()
        db.refresh(sos_record)
        return sos_record

    @staticmethod
    def list_sos_by_profile(db: Session, profile_id: int) -> list[SosRecordEntity]:
        return list(db.scalars(select(SosRecordEntity).where(SosRecordEntity.profile_id == profile_id).order_by(SosRecordEntity.id.desc())).all())

    @staticmethod
    def list_all_sos(db: Session, limit: int = 100) -> list[SosRecordEntity]:
        return list(db.scalars(select(SosRecordEntity).order_by(SosRecordEntity.id.desc()).limit(limit)).all())

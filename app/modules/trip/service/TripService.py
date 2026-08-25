from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.modules.trip.entity.TripEntity import TripEntity
from app.services.pass_token import create_dynamic_pass


class TripService:
    @staticmethod
    def create_trip(db: Session, profile_id: int, destination: str, travel_date) -> TripEntity:
        temp_trip = TripEntity(
            profile_id=profile_id,
            destination=destination,
            travel_date=travel_date,
            pass_token="pending",
            pass_qr_svg="pending",
        )
        db.add(temp_trip)
        db.flush()

        token, qr_svg = create_dynamic_pass(settings.token_secret, profile_id, temp_trip.id)
        temp_trip.pass_token = token
        temp_trip.pass_qr_svg = qr_svg

        db.commit()
        db.refresh(temp_trip)
        return temp_trip

    @staticmethod
    def get_trip_by_id(db: Session, trip_id: int) -> TripEntity | None:
        return db.get(TripEntity, trip_id)

    @staticmethod
    def list_trips_by_profile(db: Session, profile_id: int) -> list[TripEntity]:
        return list(db.scalars(select(TripEntity).where(TripEntity.profile_id == profile_id).order_by(TripEntity.id.desc())).all())

    @staticmethod
    def list_all_trips(db: Session, limit: int = 100) -> list[TripEntity]:
        return list(db.scalars(select(TripEntity).order_by(TripEntity.id.desc()).limit(limit)).all())

    @staticmethod
    def delete_trip(db: Session, trip_id: int) -> None:
        trip = db.get(TripEntity, trip_id)
        if trip:
            db.delete(trip)
            db.commit()

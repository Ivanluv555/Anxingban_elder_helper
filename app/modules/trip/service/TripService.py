from sqlalchemy.orm import Session

from app.config import settings
from app.modules.trip.entity.TripEntity import TripEntity
from app.modules.trip.repository.TripRepository import TripRepository
from app.services.pass_token import create_dynamic_pass


class TripService:
    @staticmethod
    def create_trip(db: Session, profile_id: int, destination: str, travel_date) -> TripEntity:
        repo = TripRepository(db)
        temp_trip = TripEntity(
            profile_id=profile_id,
            destination=destination,
            travel_date=travel_date,
            pass_token="pending",
            pass_qr_svg="pending",
        )
        temp_trip = repo.create(temp_trip)

        token, qr_svg = create_dynamic_pass(settings.token_secret, profile_id, temp_trip.id)
        temp_trip.pass_token = token
        temp_trip.pass_qr_svg = qr_svg

        return repo.update(temp_trip)

    @staticmethod
    def get_trip_by_id(db: Session, trip_id: int) -> TripEntity | None:
        repo = TripRepository(db)
        return repo.find_by_id(trip_id)

    @staticmethod
    def list_trips_by_profile(db: Session, profile_id: int) -> list[TripEntity]:
        repo = TripRepository(db)
        return repo.find_by_profile(profile_id)

    @staticmethod
    def list_all_trips(db: Session, limit: int = 100) -> list[TripEntity]:
        repo = TripRepository(db)
        return repo.find_all(limit)

    @staticmethod
    def delete_trip(db: Session, trip_id: int) -> None:
        repo = TripRepository(db)
        trip = repo.find_by_id(trip_id)
        if trip:
            repo.delete(trip)

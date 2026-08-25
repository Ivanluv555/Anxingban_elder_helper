import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.card.entity.MemoryCardEntity import MemoryCardEntity
from app.modules.task.entity.TaskEntity import TaskEntity


class CardService:
    @staticmethod
    def generate_card(db: Session, trip_id: int, title: str, image_url: str, trip_entity) -> MemoryCardEntity:
        tasks = db.scalars(select(TaskEntity).where(TaskEntity.trip_id == trip_id)).all()
        completed_tasks = [t.title for t in tasks if t.status == "completed"]
        summary = f"Trip to {trip_entity.destination} on {trip_entity.travel_date}. Completed tasks: {', '.join(completed_tasks) if completed_tasks else 'none yet'}."

        card_data = {
            "pilot_city": "Chongqing",
            "destination": trip_entity.destination,
            "travel_date": str(trip_entity.travel_date),
            "completed_tasks": completed_tasks,
        }
        card = MemoryCardEntity(
            trip_id=trip_id,
            title=title,
            summary=summary,
            image_url=image_url,
            card_json=json.dumps(card_data, ensure_ascii=True),
        )
        db.add(card)
        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def get_card_by_id(db: Session, card_id: int) -> MemoryCardEntity | None:
        return db.get(MemoryCardEntity, card_id)

    @staticmethod
    def list_cards_by_trip(db: Session, trip_id: int) -> list[MemoryCardEntity]:
        return list(db.scalars(select(MemoryCardEntity).where(MemoryCardEntity.trip_id == trip_id).order_by(MemoryCardEntity.id.desc())).all())

    @staticmethod
    def list_cards_by_profile(db: Session, profile_id: int) -> list[MemoryCardEntity]:
        # 通过trip_id关联查询
        from app.modules.trip.entity.TripEntity import TripEntity
        stmt = select(MemoryCardEntity).join(TripEntity).where(TripEntity.profile_id == profile_id).order_by(MemoryCardEntity.id.desc())
        return list(db.scalars(stmt).all())

    @staticmethod
    def list_all_cards(db: Session, limit: int = 100) -> list[MemoryCardEntity]:
        return list(db.scalars(select(MemoryCardEntity).order_by(MemoryCardEntity.id.desc()).limit(limit)).all())

    @staticmethod
    def delete_card(db: Session, card_id: int) -> None:
        card = db.get(MemoryCardEntity, card_id)
        if card:
            db.delete(card)
            db.commit()

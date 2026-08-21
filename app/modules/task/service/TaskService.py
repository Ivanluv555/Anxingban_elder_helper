from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.task.entity.TaskEntity import TaskEntity


class TaskService:
    @staticmethod
    def create_task(db: Session, profile_id: int, trip_id: int, title: str, description: str) -> TaskEntity:
        task = TaskEntity(
            profile_id=profile_id,
            trip_id=trip_id,
            title=title,
            description=description,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> TaskEntity | None:
        return db.get(TaskEntity, task_id)

    @staticmethod
    def complete_task(db: Session, task_id: int, completed_note: str, photo_url: str) -> TaskEntity | None:
        task = db.get(TaskEntity, task_id)
        if not task:
            return None
        task.status = "completed"
        task.completed_note = completed_note
        task.photo_url = photo_url
        task.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def feedback_task(db: Session, task_id: int, feedback_text: str, hearts_delta: int) -> TaskEntity | None:
        task = db.get(TaskEntity, task_id)
        if not task:
            return None
        task.feedback_text = feedback_text
        task.hearts = max(0, task.hearts + hearts_delta)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def list_tasks_by_profile(db: Session, profile_id: int) -> list[TaskEntity]:
        return list(db.scalars(select(TaskEntity).where(TaskEntity.profile_id == profile_id).order_by(TaskEntity.id.desc())).all())

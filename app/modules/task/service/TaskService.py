from datetime import datetime

from sqlalchemy.orm import Session

from app.modules.task.entity.TaskEntity import TaskEntity
from app.modules.task.repository.TaskRepository import TaskRepository


class TaskService:
    @staticmethod
    def create_task(db: Session, profile_id: int, trip_id: int, title: str, description: str) -> TaskEntity:
        repo = TaskRepository(db)
        task = TaskEntity(
            profile_id=profile_id,
            trip_id=trip_id,
            title=title,
            description=description,
        )
        return repo.create(task)

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> TaskEntity | None:
        repo = TaskRepository(db)
        return repo.find_by_id(task_id)

    @staticmethod
    def complete_task(db: Session, task_id: int, completed_note: str, photo_url: str) -> TaskEntity | None:
        repo = TaskRepository(db)
        task = repo.find_by_id(task_id)
        if not task:
            return None
        task.status = "completed"
        task.completed_note = completed_note
        task.photo_url = photo_url
        task.completed_at = datetime.utcnow()
        return repo.update(task)

    @staticmethod
    def feedback_task(db: Session, task_id: int, feedback_text: str, hearts_delta: int) -> TaskEntity | None:
        repo = TaskRepository(db)
        task = repo.find_by_id(task_id)
        if not task:
            return None
        task.feedback_text = feedback_text
        task.hearts = max(0, task.hearts + hearts_delta)
        return repo.update(task)

    @staticmethod
    def list_tasks_by_profile(db: Session, profile_id: int) -> list[TaskEntity]:
        repo = TaskRepository(db)
        return repo.find_by_profile(profile_id)

    @staticmethod
    def list_all_tasks(db: Session, limit: int = 100) -> list[TaskEntity]:
        repo = TaskRepository(db)
        return repo.find_all(limit)

    @staticmethod
    def delete_task(db: Session, task_id: int) -> None:
        repo = TaskRepository(db)
        task = repo.find_by_id(task_id)
        if task:
            repo.delete(task)

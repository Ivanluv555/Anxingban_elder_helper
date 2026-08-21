from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.task.dto.TaskDto import (
    TaskCompleteDto,
    TaskCreateDto,
    TaskFeedbackDto,
    TaskResponseDto,
)
from app.modules.task.service.TaskService import TaskService
from app.modules.profile.service.ProfileService import ProfileService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponseDto)
def create_task(payload: TaskCreateDto, db: Session = Depends(get_db)):
    if not ProfileService.get_profile_by_id(db, payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    if not TripService.get_trip_by_id(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")

    task = TaskService.create_task(db, payload.profile_id, payload.trip_id, payload.title, payload.description)
    return task


@router.post("/{task_id}/complete", response_model=TaskResponseDto)
def complete_task(task_id: int, payload: TaskCompleteDto, db: Session = Depends(get_db)):
    task = TaskService.complete_task(db, task_id, payload.completed_note, payload.photo_url)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/{task_id}/feedback", response_model=TaskResponseDto)
def feedback_task(task_id: int, payload: TaskFeedbackDto, db: Session = Depends(get_db)):
    task = TaskService.feedback_task(db, task_id, payload.feedback_text, payload.hearts_delta)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/profile/{profile_id}", response_model=list[TaskResponseDto])
def list_tasks(profile_id: int, db: Session = Depends(get_db)):
    return TaskService.list_tasks_by_profile(db, profile_id)

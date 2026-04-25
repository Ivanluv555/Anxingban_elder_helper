from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Profile, Task, Trip
from app.schemas import TaskComplete, TaskCreate, TaskFeedback, TaskOut

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(Profile, payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found")
    if not db.get(Trip, payload.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")

    row = Task(
        profile_id=payload.profile_id,
        trip_id=payload.trip_id,
        title=payload.title,
        description=payload.description,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.post("/{task_id}/complete", response_model=TaskOut)
def complete_task(task_id: int, payload: TaskComplete, db: Session = Depends(get_db)):
    row = db.get(Task, task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    row.status = "completed"
    row.completed_note = payload.completed_note
    row.photo_url = payload.photo_url
    row.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return row


@router.post("/{task_id}/feedback", response_model=TaskOut)
def feedback_task(task_id: int, payload: TaskFeedback, db: Session = Depends(get_db)):
    row = db.get(Task, task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    row.feedback_text = payload.feedback_text
    row.hearts = max(0, row.hearts + payload.hearts_delta)
    db.commit()
    db.refresh(row)
    return row


@router.get("/profile/{profile_id}", response_model=list[TaskOut])
def list_tasks(profile_id: int, db: Session = Depends(get_db)):
    rows = db.scalars(select(Task).where(Task.profile_id == profile_id).order_by(Task.id.desc())).all()
    return list(rows)

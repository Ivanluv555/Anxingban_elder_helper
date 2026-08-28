from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_user
from app.modules.task.dto.TaskDto import TaskCompleteDto, TaskCreateDto, TaskResponseDto, TaskDetailDto
from app.modules.task.service.TaskService import TaskService
from app.modules.profile.service.ProfileService import ProfileService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/user/tasks", tags=["子女-亲子任务"])


@router.post(
    "",
    response_model=TaskDetailDto,
    summary="创建任务"
)
def create_task(
    payload: TaskCreateDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建亲子任务"""
    if not ProfileService.get_profile_by_id(db, payload.profile_id):
        raise BusinessException(ErrorCode.NOT_FOUND, detail="档案不存在")
    if not TripService.get_trip_by_id(db, payload.trip_id):
        raise BusinessException(ErrorCode.NOT_FOUND, detail="行程不存在")

    task = TaskService.create_task(db, payload.profile_id, payload.trip_id, payload.title, payload.description)
    return task


@router.post(
    "/{task_id}/complete",
    response_model=TaskDetailDto,
    summary="完成任务"
)
def complete_task(
    task_id: int,
    payload: TaskCompleteDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """子女完成任务"""
    task = TaskService.complete_task_by_user(db, task_id, payload.feedback)
    if not task:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="任务不存在")
    return task


@router.get(
    "",
    response_model=list[TaskResponseDto],
    summary="获取任务列表"
)
def list_all_tasks(
    profile_id: int = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务列表"""
    if profile_id:
        return TaskService.list_tasks_by_profile(db, profile_id)
    return TaskService.list_all_tasks(db, limit)


@router.get(
    "/{task_id}",
    response_model=TaskDetailDto,
    summary="获取任务详情"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务详情"""
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="任务不存在")
    return task


@router.delete(
    "/{task_id}",
    summary="删除任务"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除任务"""
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="任务不存在")
    
    TaskService.delete_task(db, task_id)
    return {"message": "任务删除成功"}

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_elder
from app.modules.task.dto.TaskDto import TaskResponseDto
from app.modules.task.service.TaskService import TaskService

router = APIRouter(prefix="/api/elder/tasks", tags=["老人-亲子任务"])


@router.get(
    "/{task_id}",
    response_model=TaskResponseDto,
    summary="获取任务详情",
    description="老人用户获取指定任务详情"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取任务详情"""
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise BusinessException(ErrorCode.TASK_NOT_FOUND)
    return task


@router.get(
    "",
    response_model=list[TaskResponseDto],
    summary="获取任务列表",
    description="老人用户获取任务列表"
)
def list_tasks(
    profile_id: int = Query(None, description="档案ID筛选"),
    limit: int = Query(20, ge=1, le=100, description="返回数量限制"),
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取任务列表"""
    if profile_id:
        return TaskService.list_tasks_by_profile(db, profile_id)
    else:
        return TaskService.list_all_tasks(db, limit)

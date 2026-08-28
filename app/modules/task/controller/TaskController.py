from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_user
from app.modules.task.dto.TaskDto import (
    TaskCompleteDto,
    TaskCreateDto,
    TaskFeedbackDto,
    TaskResponseDto,
)
from app.modules.task.service.TaskService import TaskService
from app.modules.profile.service.ProfileService import ProfileService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/user/tasks", tags=["子女-亲子任务"])


@router.post(
    "",
    response_model=TaskResponseDto,
    summary="创建任务",
    description="为指定行程创建亲子互动任务",
    response_description="返回创建的任务信息"
)
def create_task(
    payload: TaskCreateDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建亲子任务
    
    功能：
    - 绑定家庭档案和行程
    - 设置任务标题和描述
    - 初始状态为待完成（pending）
    
    错误：
    - 404: 档案或行程不存在
    """
    if not ProfileService.get_profile_by_id(db, payload.profile_id):
        raise BusinessException(ErrorCode.PROFILE_NOT_FOUND)
    if not TripService.get_trip_by_id(db, payload.trip_id):
        raise BusinessException(ErrorCode.TRIP_NOT_FOUND)

    task = TaskService.create_task(db, payload.profile_id, payload.trip_id, payload.title, payload.description)
    return task


@router.post(
    "/{task_id}/complete",
    response_model=TaskResponseDto,
    summary="完成任务",
    description="标记任务为已完成，可上传完成备注和照片",
    response_description="返回更新后的任务信息"
)
def complete_task(
    task_id: int,
    payload: TaskCompleteDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """完成任务
    
    - **task_id**: 任务 ID
    - **completed_note**: 完成备注（可选）
    - **photo_url**: 完成照片 URL（可选）
    - 自动记录完成时间
    
    错误：
    - 404: 任务不存在
    """
    task = TaskService.complete_task(db, task_id, payload.completed_note, payload.photo_url)
    if not task:
        raise BusinessException(ErrorCode.TASK_NOT_FOUND)
    return task


@router.post(
    "/{task_id}/feedback",
    response_model=TaskResponseDto,
    summary="任务反馈",
    description="家长对任务完成情况进行反馈，可给予爱心奖励",
    response_description="返回更新后的任务信息"
)
def feedback_task(
    task_id: int,
    payload: TaskFeedbackDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """任务反馈
    
    - **task_id**: 任务 ID
    - **feedback_text**: 反馈文字（可选）
    - **hearts_delta**: 爱心增减值（-10 到 +10）
    - 爱心值不会低于 0
    
    错误：
    - 404: 任务不存在
    """
    task = TaskService.feedback_task(db, task_id, payload.feedback_text, payload.hearts_delta)
    if not task:
        raise BusinessException(ErrorCode.TASK_NOT_FOUND)
    return task


@router.get(
    "",
    response_model=list[TaskResponseDto],
    summary="获取任务列表",
    description="查询任务列表，支持按档案ID筛选",
    response_description="返回任务列表，按创建时间倒序"
)
def list_all_tasks(
    profile_id: int = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务列表
    
    - **profile_id**: 可选，档案ID筛选
    - **limit**: 返回数量限制，默认100
    """
    if profile_id:
        return TaskService.list_tasks_by_profile(db, profile_id)
    return TaskService.list_all_tasks(db, limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponseDto,
    summary="获取任务详情",
    description="查询单个任务的详细信息",
    response_description="返回任务详情"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务详情
    
    - **task_id**: 任务ID
    
    错误：
    - 404: 任务不存在
    """
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise BusinessException(ErrorCode.TASK_NOT_FOUND)
    return task


@router.get(
    "/profile/{profile_id}",
    response_model=list[TaskResponseDto],
    summary="获取档案任务列表",
    description="查询指定档案的所有任务，按创建时间倒序",
    response_description="返回任务列表"
)
def list_tasks(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取任务列表
    
    - **profile_id**: 档案 ID
    - 返回该档案下所有任务
    - 包含任务状态、完成情况、爱心值
    """
    return TaskService.list_tasks_by_profile(db, profile_id)


@router.delete(
    "/{task_id}",
    summary="删除任务",
    description="删除指定的任务记录",
    response_description="删除成功返回成功消息"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除任务
    
    - **task_id**: 任务ID
    
    错误：
    - 404: 任务不存在
    """
    task = TaskService.get_task_by_id(db, task_id)
    if not task:
        raise BusinessException(ErrorCode.TASK_NOT_FOUND)
    
    TaskService.delete_task(db, task_id)
    return {"message": "任务删除成功"}

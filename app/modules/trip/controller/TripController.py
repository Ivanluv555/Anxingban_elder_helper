from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.trip.dto.TripDto import TripCreateDto, TripResponseDto
from app.modules.trip.service.TripService import TripService
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/user/trips", tags=["子女-行程管理"])


@router.post(
    "",
    response_model=TripResponseDto,
    summary="创建行程",
    description="为指定档案创建新行程，自动生成动态通行码和二维码",
    response_description="返回创建的行程信息，包含通行令牌和 SVG 格式二维码"
)
def create_trip(
    payload: TripCreateDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建行程"""
    if not ProfileService.get_profile_by_id(db, payload.profile_id):
        raise HTTPException(status_code=404, detail="档案不存在")

    trip = TripService.create_trip(db, payload.profile_id, payload.destination, payload.travel_date)
    return trip


@router.get(
    "/{trip_id}",
    response_model=TripResponseDto,
    summary="获取行程详情",
    description="根据行程 ID 查询行程完整信息，包含通行码",
    response_description="返回行程详细信息"
)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取行程详情"""
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    return trip


@router.get(
    "/{trip_id}/pass",
    response_model=TripResponseDto,
    summary="获取行程通行码",
    description="获取行程的动态通行码和二维码，用于核验身份",
    response_description="返回完整行程信息，包含通行令牌和 SVG 二维码"
)
def get_trip_pass(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取通行码"""
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    return trip


@router.get(
    "",
    response_model=list[TripResponseDto],
    summary="获取行程列表",
    description="查询行程列表，支持按档案ID筛选",
    response_description="返回行程列表，按创建时间倒序"
)
def list_trips(
    profile_id: int = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取行程列表"""
    if profile_id:
        return TripService.list_trips_by_profile(db, profile_id)
    return TripService.list_all_trips(db, limit)


@router.get(
    "/profile/{profile_id}",
    response_model=list[TripResponseDto],
    summary="获取档案行程列表",
    description="查询指定档案的所有行程，按创建时间倒序",
    response_description="返回行程列表"
)
def list_trips_by_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取档案行程列表"""
    return TripService.list_trips_by_profile(db, profile_id)


@router.delete(
    "/{trip_id}",
    summary="删除行程",
    description="删除指定的行程记录",
    response_description="删除成功返回成功消息"
)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除行程"""
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    TripService.delete_trip(db, trip_id)
    return {"message": "行程删除成功"}

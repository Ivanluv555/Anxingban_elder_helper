from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_elder
from app.modules.trip.dto.TripDto import TripResponseDto
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/elder/trips", tags=["老人-行程管理"])


@router.get(
    "/{trip_id}",
    response_model=TripResponseDto,
    summary="获取行程详情",
    description="老人用户获取指定行程详情"
)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取行程详情"""
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    return trip


@router.get(
    "",
    response_model=list[TripResponseDto],
    summary="获取行程列表",
    description="老人用户获取行程列表"
)
def list_trips(
    profile_id: int = Query(None, description="档案ID筛选"),
    limit: int = Query(20, ge=1, le=100, description="返回数量限制"),
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取行程列表"""
    if profile_id:
        return TripService.list_trips_by_profile(db, profile_id)
    else:
        return TripService.list_all_trips(db, limit)


@router.get(
    "/{trip_id}/pass",
    response_model=TripResponseDto,
    summary="获取行程通行码",
    description="老人用户获取行程通行码"
)
def get_trip_pass(
    trip_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取行程通行码"""
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    return trip

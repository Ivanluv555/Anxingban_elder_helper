from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_elder
from app.modules.trip.dto.TripDto import TripResponseDto, TripDetailDto
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/elder/trips", tags=["老人-行程管理"])


@router.get(
    "/{trip_id}",
    response_model=TripDetailDto,
    summary="获取行程详情",
    description="老人用户获取指定行程详情（包含通行码）"
)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取行程详情"""
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise BusinessException(ErrorCode.NOT_FOUND, detail="行程不存在")
    return trip


@router.get(
    "",
    response_model=list[TripResponseDto],
    summary="获取行程列表",
    description="老人用户获取行程列表（列表不返回二维码）"
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
    return TripService.list_all_trips(db, limit)

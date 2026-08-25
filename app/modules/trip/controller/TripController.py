from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.trip.dto.TripDto import TripCreateDto, TripResponseDto
from app.modules.trip.service.TripService import TripService
from app.modules.profile.service.ProfileService import ProfileService

router = APIRouter(prefix="/api/trips", tags=["行程管理"])


@router.post(
    "",
    response_model=TripResponseDto,
    summary="创建行程",
    description="为指定档案创建新行程，自动生成动态通行码和二维码",
    response_description="返回创建的行程信息，包含通行令牌和 SVG 格式二维码"
)
def create_trip(payload: TripCreateDto, db: Session = Depends(get_db)):
    """创建行程
    
    功能：
    - 绑定家庭档案
    - 记录目的地和出行日期
    - 自动生成 HMAC-SHA256 签名的动态通行码
    - 生成 SVG 格式二维码供展示和打印
    
    错误：
    - 404: 档案不存在
    """
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
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    """获取行程详情
    
    - **trip_id**: 行程 ID
    
    错误：
    - 404: 行程不存在
    """
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
def get_trip_pass(trip_id: int, db: Session = Depends(get_db)):
    """获取通行码
    
    - **trip_id**: 行程 ID
    - 返回 HMAC 签名的通行令牌和 SVG 二维码
    - 建议配合核验端使用
    
    错误：
    - 404: 行程不存在
    """
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
def list_trips(profile_id: int = None, limit: int = 100, db: Session = Depends(get_db)):
    """获取行程列表
    
    - **profile_id**: 可选，档案ID筛选
    - **limit**: 返回数量限制，默认100
    """
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
def list_trips_by_profile(profile_id: int, db: Session = Depends(get_db)):
    """获取档案行程列表
    
    - **profile_id**: 档案 ID
    - 返回该档案下所有行程
    - 按创建时间倒序排列
    """
    return TripService.list_trips_by_profile(db, profile_id)


@router.delete(
    "/{trip_id}",
    summary="删除行程",
    description="删除指定的行程记录",
    response_description="删除成功返回成功消息"
)
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    """删除行程
    
    - **trip_id**: 行程ID
    
    错误：
    - 404: 行程不存在
    """
    trip = TripService.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")
    
    TripService.delete_trip(db, trip_id)
    return {"message": "行程删除成功"}

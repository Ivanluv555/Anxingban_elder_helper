from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.sos.dto.SosDto import SosRequestDto, SosResponseDto
from app.modules.sos.service.SosService import SosService
from app.modules.profile.service.ProfileService import ProfileService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/sos", tags=["紧急求助"])


@router.post(
    "/trigger",
    response_model=SosResponseDto,
    summary="触发紧急求助",
    description="触发 SOS 求助信号，双通道通知（短信 + 企业微信），支持离线队列",
    response_description="返回 SOS 记录，包含通知发送状态"
)
async def trigger_sos(payload: SosRequestDto, db: Session = Depends(get_db)):
    """触发紧急求助
    
    功能：
    - 记录求助位置（经纬度）
    - 记录网络状态（在线/离线）
    - 双通道通知：
      1. 短信发送到子女手机
      2. 企业微信通知到 Webhook
    - 离线时自动排队，恢复后重试
    - 包含健康快照（从档案获取）
    
    参数：
    - **profile_id**: 档案 ID
    - **trip_id**: 行程 ID（可选）
    - **latitude**: 纬度（-90 到 90）
    - **longitude**: 经度（-180 到 180）
    - **network_status**: 网络状态（online/offline）
    
    错误：
    - 404: 档案或行程不存在
    """
    profile = ProfileService.get_profile_by_id(db, payload.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")
    if payload.trip_id is not None and not TripService.get_trip_by_id(db, payload.trip_id):
        raise HTTPException(status_code=404, detail="行程不存在")

    sos_record = await SosService.trigger_sos(
        db,
        payload.profile_id,
        payload.trip_id,
        payload.latitude,
        payload.longitude,
        payload.network_status,
        profile,
    )
    return sos_record


@router.get(
    "/profile/{profile_id}",
    response_model=list[SosResponseDto],
    summary="获取 SOS 历史记录",
    description="查询指定档案的所有 SOS 求助记录，按时间倒序",
    response_description="返回 SOS 记录列表"
)
def list_sos_records(profile_id: int, db: Session = Depends(get_db)):
    """获取 SOS 历史
    
    - **profile_id**: 档案 ID
    - 返回该档案的所有求助记录
    - 包含位置、时间、通知状态
    """
    return SosService.list_sos_by_profile(db, profile_id)

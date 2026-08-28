from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.utils.error_codes import BusinessException, ErrorCode
from app.modules.auth.dependencies import get_current_elder
from app.modules.sos.dto.SosDto import SosResponseDto, SosRequestDto
from app.modules.sos.service.SosService import SosService

router = APIRouter(prefix="/api/elder/sos", tags=["老人-紧急求助"])


@router.post(
    "/trigger",
    response_model=SosResponseDto,
    summary="触发SOS紧急求助",
    description="老人用户触发紧急求助"
)
async def trigger_sos(
    payload: SosRequestDto,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """触发SOS"""
    # 这里需要从profile获取elder信息，暂时简化处理
    from app.modules.profile.service.ProfileService import ProfileService
    profile = ProfileService.get_profile_by_id(db, payload.profile_id)
    if not profile:
        raise BusinessException(ErrorCode.PROFILE_NOT_BOUND)
    
    # 获取elder信息作为profile_entity传递
    from app.modules.auth.service.AuthService import AuthService
    elder = AuthService.get_elder_by_id(db, profile.elder_id)
    
    sos_record = await SosService.trigger_sos(
        db,
        payload.profile_id,
        payload.trip_id,
        payload.latitude,
        payload.longitude,
        payload.network_status,
        elder
    )
    return sos_record


@router.get(
    "",
    response_model=list[SosResponseDto],
    summary="获取SOS记录列表",
    description="老人用户获取紧急求助记录"
)
def list_sos(
    profile_id: int = Query(None, description="档案ID筛选"),
    limit: int = Query(100, ge=1, le=500, description="返回数量限制"),
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取SOS记录列表"""
    if profile_id:
        return SosService.list_sos_by_profile(db, profile_id)
    else:
        return SosService.list_all_sos(db, limit)

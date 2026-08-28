from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.sos.dto.SosDto import SosResponseDto
from app.modules.sos.service.SosService import SosService

router = APIRouter(prefix="/api/user/sos", tags=["子女-紧急求助"])


@router.get(
    "",
    response_model=list[SosResponseDto],
    summary="获取SOS记录列表",
    description="查询SOS记录列表，支持按档案ID筛选",
    response_description="返回SOS记录列表，按时间倒序"
)
def list_all_sos(
    profile_id: int = None, # type: ignore
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取SOS记录列表"""
    if profile_id:
        return SosService.list_sos_by_profile(db, profile_id)
    return SosService.list_all_sos(db, limit)


@router.get(
    "/profile/{profile_id}",
    response_model=list[SosResponseDto],
    summary="获取 SOS 历史记录",
    description="查询指定档案的所有 SOS 求助记录，按时间倒序",
    response_description="返回 SOS 记录列表"
)
def list_sos_records(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取 SOS 历史"""
    return SosService.list_sos_by_profile(db, profile_id)

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_elder
from app.modules.card.dto.CardDto import CardGenerateDto, CardResponseDto
from app.modules.card.service.CardService import CardService

router = APIRouter(prefix="/api/elder/cards", tags=["老人-回忆卡片"])


@router.post(
    "/generate",
    response_model=CardResponseDto,
    summary="生成回忆卡片",
    description="老人用户为行程生成回忆卡片"
)
def generate_card(
    payload: CardGenerateDto,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """生成回忆卡片"""
    card = CardService.generate_card(db, payload.trip_id)
    if not card:
        raise HTTPException(status_code=404, detail="行程不存在或卡片生成失败")
    return card


@router.get(
    "/{card_id}",
    response_model=CardResponseDto,
    summary="获取卡片详情",
    description="老人用户获取指定回忆卡片"
)
def get_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取卡片详情"""
    card = CardService.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    return card


@router.get(
    "",
    response_model=list[CardResponseDto],
    summary="获取卡片列表",
    description="老人用户获取回忆卡片列表"
)
def list_cards(
    profile_id: int = Query(None, description="档案ID筛选"),
    trip_id: int = Query(None, description="行程ID筛选"),
    limit: int = Query(20, ge=1, le=100, description="返回数量限制"),
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """获取卡片列表"""
    if profile_id:
        return CardService.list_cards_by_profile(db, profile_id)
    elif trip_id:
        return CardService.list_cards_by_trip(db, trip_id)
    else:
        return CardService.list_all_cards(db, limit)


@router.delete(
    "/{card_id}",
    summary="删除卡片",
    description="老人用户删除指定回忆卡片"
)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """删除卡片"""
    card = CardService.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    CardService.delete_card(db, card_id)
    return {"message": "卡片删除成功"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.card.dto.CardDto import CardGenerateDto, CardResponseDto
from app.modules.card.service.CardService import CardService
from app.modules.trip.service.TripService import TripService

router = APIRouter(prefix="/api/user/cards", tags=["子女-回忆卡片"])


@router.post(
    "/generate",
    response_model=CardResponseDto,
    summary="生成回忆卡片",
    description="为指定行程生成回忆卡片，汇总行程信息和已完成任务",
    response_description="返回生成的卡片信息，包含 JSON 格式数据"
)
def generate_card(
    payload: CardGenerateDto,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """生成回忆卡片
    
    功能：
    - 绑定行程
    - 自动汇总目的地、日期
    - 统计已完成任务
    - 生成 JSON 格式卡片数据
    - 支持自定义标题和配图
    
    参数：
    - **trip_id**: 行程 ID
    - **title**: 卡片标题（可选，默认 "Travel Memory Card"）
    - **image_url**: 卡片配图 URL（可选）
    
    错误：
    - 404: 行程不存在
    """
    trip = TripService.get_trip_by_id(db, payload.trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="行程不存在")

    card = CardService.generate_card(db, payload.trip_id, payload.title, payload.image_url, trip)
    return card


@router.get(
    "/{card_id}",
    response_model=CardResponseDto,
    summary="获取卡片详情",
    description="根据卡片 ID 查询卡片完整信息",
    response_description="返回卡片详细信息"
)
def get_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取卡片详情
    
    - **card_id**: 卡片 ID
    
    错误：
    - 404: 卡片不存在
    """
    card = CardService.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    return card


@router.get(
    "",
    response_model=list[CardResponseDto],
    summary="获取卡片列表",
    description="查询卡片列表，支持按档案ID或行程ID筛选",
    response_description="返回卡片列表，按创建时间倒序"
)
def list_cards(
    profile_id: int = None,
    trip_id: int = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取卡片列表
    
    - **profile_id**: 可选，档案ID筛选
    - **trip_id**: 可选，行程ID筛选
    - **limit**: 返回数量限制，默认100
    """
    if trip_id:
        return CardService.list_cards_by_trip(db, trip_id)
    elif profile_id:
        return CardService.list_cards_by_profile(db, profile_id)
    return CardService.list_all_cards(db, limit)


@router.get(
    "/trip/{trip_id}",
    response_model=list[CardResponseDto],
    summary="获取行程卡片列表",
    description="查询指定行程的所有回忆卡片，按创建时间倒序",
    response_description="返回卡片列表"
)
def list_cards_by_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取行程卡片列表
    
    - **trip_id**: 行程 ID
    - 返回该行程的所有回忆卡片
    - 按创建时间倒序排列
    """
    return CardService.list_cards_by_trip(db, trip_id)


@router.delete(
    "/{card_id}",
    summary="删除卡片",
    description="删除指定的回忆卡片",
    response_description="删除成功返回成功消息"
)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除卡片
    
    - **card_id**: 卡片ID
    
    错误：
    - 404: 卡片不存在
    """
    card = CardService.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="卡片不存在")
    
    CardService.delete_card(db, card_id)
    return {"message": "卡片删除成功"}

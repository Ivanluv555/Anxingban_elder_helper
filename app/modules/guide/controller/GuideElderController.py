from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.modules.auth.dependencies import get_current_elder
from app.modules.guide.dto.GuideDto import GuideAskDto, GuideAnswerDto
from app.modules.guide.service.GuideService import GuideService

router = APIRouter(prefix="/api/elder/guide", tags=["老人-景点讲解"])


@router.post(
    "/ask",
    response_model=GuideAnswerDto,
    summary="询问景点导游",
    description="老人用户询问景点相关问题"
)
async def ask_guide(
    payload: GuideAskDto,
    db: Session = Depends(get_db),
    current_elder = Depends(get_current_elder)
):
    """询问景点导游"""
    answer, confidence = GuideService.ask_question(payload.question)
    return GuideAnswerDto(
        answer=answer,
        confidence=confidence,
        scope="重庆试点城市"
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.modules.guide.dto.GuideDto import GuideAnswerDto, GuideAskDto
from app.modules.guide.service.GuideService import GuideService

router = APIRouter(prefix="/api/guide", tags=["guide"])


@router.post("/ask", response_model=GuideAnswerDto)
def ask_guide(payload: GuideAskDto):
    answer, confidence = GuideService.ask_question(payload.question)
    return GuideAnswerDto(answer=answer, confidence=confidence, scope=settings.guide_scope)

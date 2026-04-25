from fastapi import APIRouter

from app.config import settings
from app.schemas import GuideAnswer, GuideAsk
from app.services.ai_guide import answer_question

router = APIRouter(prefix="/api/guide", tags=["guide"])


@router.post("/ask", response_model=GuideAnswer)
def ask_guide(payload: GuideAsk):
    answer, confidence = answer_question(payload.question)
    return GuideAnswer(answer=answer, confidence=confidence, scope=settings.guide_scope)

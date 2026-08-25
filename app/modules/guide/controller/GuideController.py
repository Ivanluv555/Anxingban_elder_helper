from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.modules.guide.dto.GuideDto import GuideAnswerDto, GuideAskDto
from app.modules.guide.service.GuideService import GuideService

router = APIRouter(prefix="/api/guide", tags=["景点讲解"])


@router.post(
    "/ask",
    response_model=GuideAnswerDto,
    summary="景点智能问答",
    description="基于 AI 的景点讲解问答系统，提供重庆试点城市景点信息",
    response_description="返回 AI 生成的回答、置信度和服务范围"
)
def ask_guide(payload: GuideAskDto):
    """景点智能讲解
    
    功能：
    - 基于 AI 模型的景点问答
    - 支持景点介绍、历史文化、游玩攻略
    - 返回置信度评分
    - 当前服务范围：重庆试点城市
    
    参数：
    - **question**: 用户提问（1-500 字）
    
    返回：
    - **answer**: AI 生成的回答
    - **confidence**: 置信度（0-1）
    - **scope**: 服务范围（当前为重庆）
    
    示例问题：
    - "洪崖洞有什么特色？"
    - "磁器口古镇的历史"
    - "武隆天生三桥怎么去？"
    """
    answer, confidence = GuideService.ask_question(payload.question)
    return GuideAnswerDto(answer=answer, confidence=confidence, scope=settings.guide_scope)

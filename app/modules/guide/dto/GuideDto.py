from pydantic import BaseModel, Field


class GuideAskDto(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class GuideAnswerDto(BaseModel):
    answer: str
    confidence: float
    scope: str

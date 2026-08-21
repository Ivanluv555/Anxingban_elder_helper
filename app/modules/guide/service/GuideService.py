from app.services.ai_guide import answer_question


class GuideService:
    @staticmethod
    def ask_question(question: str) -> tuple[str, float]:
        return answer_question(question)

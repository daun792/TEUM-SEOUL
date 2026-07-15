from datetime import date

from sqlalchemy.orm import Session

from app.repositories.place_repository import PlaceRepository
from app.services.openai_service import OpenAIService, OpenAIUnavailable
from app.services.question_classifier import classify_question


NO_RESULT_MESSAGE = """죄송합니다. 관련 정보를 찾지 못했습니다.

예시 질문
- 한강 관광지 추천해줘
- 강남 숙박 추천해줘
- 서울 불꽃축제 일정 알려줘
- 경복궁 위치 알려줘
- 서울 여행코스 추천해줘"""


class ChatService:
    def __init__(self, db: Session, openai_service: OpenAIService | None = None):
        self.repository = PlaceRepository(db)
        self.openai_service = openai_service or OpenAIService()

    def chat(self, message: str) -> str:
        classification = classify_question(message)
        question_type = classification["question_type"]
        category = classification["category"]
        keyword = classification["keyword"] or ""

        if question_type == "community":
            return "커뮤니티 글은 상단의 커뮤니티 메뉴에서 검색해 주세요. 관광지·축제·숙박·쇼핑 정보는 여기서 안내할 수 있습니다."

        places = self.repository.search_places(keyword=keyword, category=category)
        if not places and category is not None:
            places = self.repository.search_places(keyword=keyword, category=None)
        if not places:
            return NO_RESULT_MESSAGE

        grounded_result = self._build_grounded_result(places)
        try:
            return self.openai_service.generate_answer(message, grounded_result)
        except OpenAIUnavailable:
            return self._build_fallback_answer(places)

    @staticmethod
    def _format_period(start: date | None, end: date | None) -> str | None:
        if start and end:
            return start.isoformat() if start == end else f"{start.isoformat()} ~ {end.isoformat()}"
        if start:
            return start.isoformat()
        return None

    def _build_grounded_result(self, places) -> str:
        sections = []
        for place in places:
            lines = [f"장소명: {place.title}", f"분류: {place.category or '미분류'}"]
            address = " ".join(part for part in [place.addr1, place.addr2] if part)
            if address:
                lines.append(f"주소: {address}")
            if place.tel:
                lines.append(f"전화번호: {place.tel}")
            period = self._format_period(place.event_start_date, place.event_end_date)
            if period:
                lines.append(f"기간: {period}")
            sections.append("\n".join(lines))
        return "\n\n".join(sections)

    def _build_fallback_answer(self, places) -> str:
        lines = ["검색 결과를 정리했어요."]
        for index, place in enumerate(places, start=1):
            lines.append(f"\n{index}. {place.title}")
            address = " ".join(part for part in [place.addr1, place.addr2] if part)
            if address:
                lines.append(f"- 주소: {address}")
            if place.category:
                lines.append(f"- 분류: {place.category}")
            period = self._format_period(place.event_start_date, place.event_end_date)
            if period:
                lines.append(f"- 기간: {period}")
        return "\n".join(lines)

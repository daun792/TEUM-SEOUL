from app.database.database import SessionLocal
from app.repositories.place_repository import PlaceRepository
from app.services.question_classifier import classify_question
from app.services.openai_service import OpenAIService


class ChatService:

    def __init__(self):
        self.openai_service = OpenAIService()


    def chat(self, message: str) -> str:

        classification = classify_question(message)

        question_type = classification["question_type"]
        category = classification["category"]
        keyword = classification["keyword"]


        db = SessionLocal()

        try:

            repository = PlaceRepository(db)


            if keyword == "":
                return """
죄송합니다. 관련 정보를 찾지 못했습니다.

틈서울은 서울 관광 정보를 안내해드립니다.

예시 질문
- 한강 관광지 추천해줘
- 강남 숙박 추천해줘
- 서울 불꽃축제 일정 알려줘
- 경복궁 위치 알려줘
- 명동 쇼핑 추천해줘
"""


            places = repository.search_places(
                keyword=keyword,
                category=category
            )


            if not places:
                return """
죄송합니다. 관련 정보를 찾지 못했습니다.

틈서울은 서울 관광 정보를 안내해드립니다.

예시 질문
- 한강 관광지 추천해줘
- 강남 숙박 추천해줘
- 서울 불꽃축제 일정 알려줘
- 경복궁 위치 알려줘
- 명동 쇼핑 추천해줘
"""


            search_result = ""


            for place in places:
                search_result += f"관광지명: {place.title}\n"
                search_result += f"주소: {place.addr1}\n"
                search_result += f"분류: {place.category}\n"

                if place.tel:
                    search_result += f"전화번호: {place.tel}\n"

                search_result += "\n"



            answer = self.openai_service.generate_answer(
                question=message,
                search_result=search_result
            )


            return answer


        finally:
            db.close()
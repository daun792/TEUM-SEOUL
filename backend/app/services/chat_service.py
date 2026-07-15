from app.database.database import SessionLocal
from app.repositories.place_repository import PlaceRepository
from app.services.question_classifier import classify_question


class ChatService:

    def chat(self, message: str) -> str:

        question_type = classify_question(message)

        db = SessionLocal()

        try:

            repository = PlaceRepository(db)

            keyword = ""

            if "한강" in message:
                keyword = "한강"

            elif "경복궁" in message:
                keyword = "경복궁"

            elif "서울" in message:
                keyword = "서울"

            places = repository.search_places(keyword=keyword)

            if not places:
                return "검색 결과가 없습니다."

            answer = ""

            for place in places:
                answer += f"• {place.title}\n"
                answer += f"  주소 : {place.addr1}\n\n"

            return answer

        finally:
            db.close()
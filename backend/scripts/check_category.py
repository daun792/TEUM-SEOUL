from app.database.database import SessionLocal
from app.database.models import Place
from app.repositories.place_repository import PlaceRepository


db = SessionLocal()

places = (
    db.query(Place)
    .filter(Place.title.like("%경복궁%"))
    .all()
)



for p in places:
    print(
        p.title,
        "|",
        p.category,
        "|",
        p.addr1
    )


print('\n=== 여행코스 category 검색 (keyword="서울") ===')
repo = PlaceRepository(db)
travel_courses = repo.search_places(
    keyword="서울",
    category="여행코스"
)
for p in travel_courses:
    print(
        p.title,
        "|",
        p.category,
        "|",
        p.addr1
    )


db.close()
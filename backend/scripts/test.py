import os
import sys


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.database.database import SessionLocal
from app.repositories.place_repository import PlaceRepository



db = SessionLocal()


repository = PlaceRepository(db)



results = repository.search_places(
    keyword="한강",
    category="관광지"
)



for place in results:

    print("================")

    print(place.title)

    print(place.addr1)



db.close()
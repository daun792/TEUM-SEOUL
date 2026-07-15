from app.database.database import SessionLocal
from app.database.models import Place


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


db.close()
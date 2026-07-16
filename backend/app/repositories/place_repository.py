from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database.models import Place


class PlaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_places(
        self,
        keyword: str,
        category: str | None = None,
        limit: int = 5,
    ) -> list[Place]:
        statement = select(Place)

        for word in keyword.split():
            pattern = f"%{word}%"
            statement = statement.where(
                or_(
                    Place.title.ilike(pattern),
                    Place.addr1.ilike(pattern),
                    Place.addr2.ilike(pattern),
                )
            )

        if category:
            statement = statement.where(Place.category == category)

        statement = statement.order_by(Place.title.asc()).limit(limit)
        return list(self.db.scalars(statement).all())

    def get_by_title(self, title: str) -> Place | None:
        return self.db.scalar(select(Place).where(Place.title == title))

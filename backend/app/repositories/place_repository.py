from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.models import Place


class PlaceRepository:

    def __init__(self, db: Session):
        self.db = db


    def search_places(
        self,
        keyword: str,
        category: str = None,
        limit: int = 5
    ):

        query = self.db.query(Place)

        if keyword:

            keywords = keyword.split()

            for word in keywords:

                query = query.filter(
                    or_(
                        Place.title.like(f"%{word}%"),
                        Place.addr1.like(f"%{word}%")
                    )
                )

        if category:
            query = query.filter(
                Place.category == category
            )

        return query.limit(limit).all()



    def search_festivals(
        self,
        keyword: str,
        limit: int = 5
    ):

        query = self.db.query(Place)

        # 축제 데이터만 조회
        query = query.filter(
            Place.category == "축제"
        )


        if keyword:

            keywords = keyword.split()

            for word in keywords:

                query = query.filter(
                    or_(
                        Place.title.like(f"%{word}%"),
                        Place.addr1.like(f"%{word}%")
                    )
                )


        return query.limit(limit).all()



    def get_by_title(self, title: str):

        return (
            self.db.query(Place)
            .filter(Place.title == title)
            .first()
        )
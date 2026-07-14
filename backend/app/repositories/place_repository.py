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

            query = query.filter(
                Place.title.like(
                    f"%{keyword}%"
                )
            )


        if category:

            query = query.filter(
                Place.category == category
            )


        return (
            query
            .limit(limit)
            .all()
        )



    def get_by_title(
        self,
        title: str
    ):

        return (
            self.db.query(Place)
            .filter(
                Place.title == title
            )
            .first()
        )
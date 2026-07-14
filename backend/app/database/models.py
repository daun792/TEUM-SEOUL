from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class Place(Base):

    __tablename__ = "places"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    contentid = Column(
        String,
        unique=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    category = Column(
        String
    )


    contenttypeid = Column(
        String
    )


    addr1 = Column(
        String
    )


    addr2 = Column(
        String
    )


    mapx = Column(
        Float
    )


    mapy = Column(
        Float
    )


    tel = Column(
        String
    )


    firstimage = Column(
        String
    )


    firstimage2 = Column(
        String
    )


    createdtime = Column(
        String
    )


    modifiedtime = Column(
        String
    )
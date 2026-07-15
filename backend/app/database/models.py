from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Place(Base):
    __tablename__ = "places"
    __table_args__ = (
        Index("ix_places_type_title", "contenttypeid", "title"),
        Index("ix_places_coordinates", "mapy", "mapx"),
        Index("ix_places_event_dates", "event_start_date", "event_end_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contentid: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(300), index=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(50), index=True)
    contenttypeid: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    addr1: Mapped[str | None] = mapped_column(String(500))
    addr2: Mapped[str | None] = mapped_column(String(500))
    zipcode: Mapped[str | None] = mapped_column(String(20))
    mapx: Mapped[float | None] = mapped_column(Float)
    mapy: Mapped[float | None] = mapped_column(Float)
    tel: Mapped[str | None] = mapped_column(String(200))
    firstimage: Mapped[str | None] = mapped_column(Text)
    firstimage2: Mapped[str | None] = mapped_column(Text)
    createdtime: Mapped[str | None] = mapped_column(String(14))
    modifiedtime: Mapped[str | None] = mapped_column(String(14))
    event_start_date: Mapped[date | None] = mapped_column(Date)
    event_end_date: Mapped[date | None] = mapped_column(Date)
    source_region: Mapped[str | None] = mapped_column(String(100), index=True)
    source_license: Mapped[str | None] = mapped_column(String(100))


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(50), default="익명", nullable=False)
    password_hash: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

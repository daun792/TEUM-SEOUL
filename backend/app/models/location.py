from __future__ import annotations

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    address: Mapped[str] = mapped_column(Text, default="", nullable=False)
    address_detail: Mapped[str] = mapped_column(Text, default="", nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[str] = mapped_column(String(32), default="서울", nullable=False)
    district_code: Mapped[str] = mapped_column(String(16), default="", nullable=False)
    image_url: Mapped[str] = mapped_column(Text, default="", nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(Text, default="", nullable=False)
    telephone: Mapped[str] = mapped_column(String(128), default="", nullable=False)
    source: Mapped[str] = mapped_column(String(255), default="한국관광공사 TourAPI 4.0", nullable=False)

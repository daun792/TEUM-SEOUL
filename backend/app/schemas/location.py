from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content_id: str
    name: str
    category: str
    address: str
    address_detail: str = ""
    latitude: float
    longitude: float
    region: str
    image_url: str = ""
    thumbnail_url: str = ""
    telephone: str = ""
    source: str


class LocationList(BaseModel):
    total: int
    items: list[LocationRead]

import json
from datetime import date, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Place


class ImportValidationError(ValueError):
    pass


def _blank_to_none(value):
    return None if value in (None, "") else value


def _parse_datetime(value: str | None) -> datetime | None:
    value = _blank_to_none(value)
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d%H%M%S")
    except ValueError as exc:
        raise ValueError("must use YYYYMMDDHHmmss format") from exc


def _parse_date(value: str | None) -> date | None:
    value = _blank_to_none(value)
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d").date()
    except ValueError as exc:
        raise ValueError("must use YYYYMMDD format") from exc


class TourItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content_id: str = Field(alias="contentid")
    content_type_id: str = Field(alias="contenttypeid")
    title: str
    address1: str | None = Field(default=None, alias="addr1")
    address2: str | None = Field(default=None, alias="addr2")
    zipcode: str | None = None
    telephone: str | None = Field(default=None, alias="tel")
    longitude: float | None = Field(default=None, alias="mapx")
    latitude: float | None = Field(default=None, alias="mapy")
    image_url: str | None = Field(default=None, alias="firstimage")
    thumbnail_url: str | None = Field(default=None, alias="firstimage2")
    created_at: datetime | None = Field(default=None, alias="createdtime")
    modified_at: datetime | None = Field(default=None, alias="modifiedtime")
    event_start_date: date | None = Field(default=None, alias="eventstartdate")
    event_end_date: date | None = Field(default=None, alias="eventenddate")

    @field_validator(
        "address1", "address2", "zipcode", "telephone", "image_url", "thumbnail_url",
        mode="before",
    )
    @classmethod
    def normalize_blank_strings(cls, value):
        return _blank_to_none(value)

    @field_validator("longitude", mode="before")
    @classmethod
    def validate_longitude(cls, value):
        value = _blank_to_none(value)
        if value is None:
            return None
        parsed = float(value)
        if not -180 <= parsed <= 180:
            raise ValueError("longitude must be between -180 and 180")
        return parsed

    @field_validator("latitude", mode="before")
    @classmethod
    def validate_latitude(cls, value):
        value = _blank_to_none(value)
        if value is None:
            return None
        parsed = float(value)
        if not -90 <= parsed <= 90:
            raise ValueError("latitude must be between -90 and 90")
        return parsed

    @field_validator("created_at", "modified_at", mode="before")
    @classmethod
    def validate_datetime(cls, value):
        return _parse_datetime(value)

    @field_validator("event_start_date", "event_end_date", mode="before")
    @classmethod
    def validate_event_date(cls, value):
        return _parse_date(value)

    @model_validator(mode="after")
    def validate_event_period(self):
        if (
            self.event_start_date
            and self.event_end_date
            and self.event_start_date > self.event_end_date
        ):
            raise ValueError("eventstartdate must not be after eventenddate")
        return self


class TourApiFile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    region: str
    content_type: str = Field(alias="contentType")
    content_type_id: int = Field(alias="contentTypeId")
    total: int
    items: list[TourItem]

    @model_validator(mode="after")
    def validate_item_count(self):
        if self.total != len(self.items):
            raise ValueError(f"total={self.total} does not match items={len(self.items)}")
        return self


def load_tourapi_file(path: Path) -> TourApiFile:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return TourApiFile.model_validate(raw)
    except (OSError, json.JSONDecodeError, ValidationError, ValueError) as exc:
        raise ImportValidationError(f"{path.name}: {exc}") from exc


def discover_tourapi_files(data_dir: Path, region: str = "서울") -> list[tuple[Path, TourApiFile]]:
    discovered: list[tuple[Path, TourApiFile]] = []
    errors: list[str] = []
    for path in sorted(data_dir.rglob("*.json")):
        try:
            payload = load_tourapi_file(path)
        except ImportValidationError as exc:
            errors.append(str(exc))
            continue
        if payload.region == region:
            discovered.append((path, payload))
    if not discovered:
        detail = f"; validation errors: {' | '.join(errors[:3])}" if errors else ""
        raise ImportValidationError(f"No TourAPI files found for region={region}{detail}")
    return discovered


def import_directory(db: Session, data_dir: Path, region: str = "서울") -> dict[str, int]:
    files = discover_tourapi_files(data_dir, region=region)
    inserted = 0
    updated = 0
    seen_content_ids: set[str] = set()

    for _path, payload in files:
        for item in payload.items:
            if item.content_id in seen_content_ids:
                continue
            seen_content_ids.add(item.content_id)
            existing = db.scalar(select(Place).where(Place.contentid == item.content_id))
            values = {
                "title": item.title,
                "category": payload.content_type,
                "contenttypeid": item.content_type_id,
                "addr1": item.address1,
                "addr2": item.address2,
                "zipcode": item.zipcode,
                "mapx": item.longitude,
                "mapy": item.latitude,
                "tel": item.telephone,
                "firstimage": item.image_url,
                "firstimage2": item.thumbnail_url,
                "createdtime": item.created_at.strftime("%Y%m%d%H%M%S") if item.created_at else None,
                "modifiedtime": item.modified_at.strftime("%Y%m%d%H%M%S") if item.modified_at else None,
                "event_start_date": item.event_start_date,
                "event_end_date": item.event_end_date,
                "source_region": payload.region,
                "source_license": "한국관광공사 TourAPI 4.0",
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                db.add(Place(contentid=item.content_id, **values))
                inserted += 1
    db.commit()
    return {"files": len(files), "inserted": inserted, "updated": updated, "total": len(seen_content_ids)}

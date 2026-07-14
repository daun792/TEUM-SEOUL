from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.location import Location


@dataclass(frozen=True)
class LoadResult:
    inserted: int
    updated: int
    skipped: int


def _safe_float(value: object) -> float | None:
    try:
        text = str(value or "").strip()
        return float(text) if text else None
    except (TypeError, ValueError):
        return None


def load_locations(directory: Path, session: Session) -> LoadResult:
    inserted = 0
    updated = 0
    skipped = 0

    for path in sorted(directory.glob("서울_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        category = str(payload.get("contentType", "")).strip()
        region = str(payload.get("region", "서울")).strip() or "서울"
        for item in payload.get("items", []):
            longitude = _safe_float(item.get("mapx"))
            latitude = _safe_float(item.get("mapy"))
            content_id = str(item.get("contentid", "")).strip()
            title = str(item.get("title", "")).strip()
            if longitude is None or latitude is None or not content_id or not title:
                skipped += 1
                continue

            existing = session.scalar(select(Location).where(Location.content_id == content_id))
            values = {
                "name": title,
                "category": category,
                "address": str(item.get("addr1", "") or ""),
                "address_detail": str(item.get("addr2", "") or ""),
                "longitude": longitude,
                "latitude": latitude,
                "region": region,
                "district_code": str(item.get("lDongSignguCd", "") or ""),
                "image_url": str(item.get("firstimage", "") or ""),
                "thumbnail_url": str(item.get("firstimage2", "") or ""),
                "telephone": str(item.get("tel", "") or ""),
                "source": "한국관광공사 TourAPI 4.0",
            }
            if existing:
                for key, value in values.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                session.add(Location(content_id=content_id, **values))
                inserted += 1

    session.commit()
    return LoadResult(inserted=inserted, updated=updated, skipped=skipped)

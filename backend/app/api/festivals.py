from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Place
from app.services.distance import haversine_km

router = APIRouter(prefix="/api/festivals", tags=["festivals"])


def _period(place: Place) -> str | None:
    if place.event_start_date and place.event_end_date:
        if place.event_start_date == place.event_end_date:
            return place.event_start_date.isoformat()
        return f"{place.event_start_date.isoformat()} ~ {place.event_end_date.isoformat()}"
    if place.event_start_date:
        return place.event_start_date.isoformat()
    return None


def _serialize_place(place: Place) -> dict:
    return {
        "id": place.contentid,
        "content_id": place.contentid,
        "title": place.title,
        "name": place.title,
        "category": place.category,
        "content_type_id": place.contenttypeid,
        "address": " ".join(part for part in [place.addr1, place.addr2] if part),
        "addr1": place.addr1,
        "addr2": place.addr2,
        "telephone": place.tel,
        "longitude": place.mapx,
        "latitude": place.mapy,
        "lng": place.mapx,
        "lat": place.mapy,
        "image_url": place.firstimage,
        "thumbnail_url": place.firstimage2,
        "event_start_date": place.event_start_date,
        "event_end_date": place.event_end_date,
        "period": _period(place),
    }


@router.get("")
def list_festivals(
    q: str | None = Query(default=None, max_length=100),
    start_date: date | None = None,
    end_date: date | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=422, detail="start_date must not be after end_date")

    filters = [Place.contenttypeid == "15"]
    if q:
        keyword = f"%{q.strip()}%"
        filters.append(or_(Place.title.ilike(keyword), Place.addr1.ilike(keyword)))
    if start_date or end_date:
        window_start = start_date or date.min
        window_end = end_date or date.max
        filters.append(
            and_(
                Place.event_start_date.is_not(None),
                Place.event_end_date.is_not(None),
                Place.event_start_date <= window_end,
                Place.event_end_date >= window_start,
            )
        )

    total = db.scalar(select(func.count()).select_from(Place).where(*filters)) or 0
    rows = db.scalars(
        select(Place)
        .where(*filters)
        .order_by(Place.event_start_date.asc().nullslast(), Place.title.asc())
        .offset((page - 1) * size)
        .limit(size)
    ).all()
    return {
        "items": [_serialize_place(row) for row in rows],
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size,
    }


@router.get("/{content_id}")
def get_festival(content_id: str, db: Session = Depends(get_db)):
    festival = db.scalar(
        select(Place).where(Place.contentid == content_id, Place.contenttypeid == "15")
    )
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")
    return _serialize_place(festival)


@router.get("/{content_id}/nearby")
def get_nearby_places(
    content_id: str,
    radius_km: float = Query(default=2.0, gt=0, le=20),
    categories: str | None = Query(default=None, description="Comma-separated category names"),
    limit: int = Query(default=30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    festival = db.scalar(
        select(Place).where(Place.contentid == content_id, Place.contenttypeid == "15")
    )
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")
    if festival.mapx is None or festival.mapy is None:
        raise HTTPException(status_code=422, detail="Festival coordinates are unavailable")

    filters = [
        Place.contentid != content_id,
        Place.mapx.is_not(None),
        Place.mapy.is_not(None),
    ]
    category_values = [item.strip() for item in categories.split(",") if item.strip()] if categories else []
    if category_values:
        filters.append(Place.category.in_(category_values))

    # Bounding box reduces DB candidates before exact Haversine calculation.
    latitude_delta = radius_km / 111.0
    longitude_delta = radius_km / max(111.0 * 0.7, 1)
    filters.extend(
        [
            Place.mapy.between(festival.mapy - latitude_delta, festival.mapy + latitude_delta),
            Place.mapx.between(festival.mapx - longitude_delta, festival.mapx + longitude_delta),
        ]
    )
    candidates = db.scalars(select(Place).where(*filters)).all()

    nearby = []
    for place in candidates:
        distance = haversine_km(festival.mapy, festival.mapx, place.mapy, place.mapx)
        if distance <= radius_km:
            serialized = _serialize_place(place)
            serialized["distance_km"] = round(distance, 3)
            nearby.append(serialized)
    nearby.sort(key=lambda item: (item["distance_km"], item["title"]))
    return {
        "festival_id": festival.contentid,
        "radius_km": radius_km,
        "items": nearby[:limit],
        "total": min(len(nearby), limit),
    }

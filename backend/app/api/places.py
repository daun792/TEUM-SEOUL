from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Place
from app.services.distance import haversine_km

router = APIRouter(prefix="/api/places", tags=["places"])


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
    }


def _category_filters(category: str | None):
    if not category:
        return []

    normalized = category.strip()
    if not normalized:
        return []

    aliases = {
        "축제": ["축제", "축제공연행사"],
        "체험": ["체험", "레포츠"],
    }
    values = aliases.get(normalized, [normalized])
    return [or_(*[Place.category == value for value in values])]


@router.get("")
def list_places(
    q: str | None = Query(default=None, max_length=100),
    category: str | None = Query(default=None, max_length=50),
    content_type_id: str | None = Query(default=None, max_length=10),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=200),
    lat: float | None = Query(default=None),
    lng: float | None = Query(default=None),
    radius_km: float | None = Query(default=None, gt=0, le=20),
    db: Session = Depends(get_db),
):
    if radius_km is not None and (lat is None or lng is None):
        raise HTTPException(status_code=422, detail="lat and lng are required when radius_km is provided")

    filters = []
    # Map screens require valid coordinates, so keep only mappable rows.
    filters.extend([Place.mapy.is_not(None), Place.mapx.is_not(None)])

    if q:
        keyword = f"%{q.strip()}%"
        filters.append(or_(Place.title.ilike(keyword), Place.addr1.ilike(keyword), Place.addr2.ilike(keyword)))

    filters.extend(_category_filters(category))

    if content_type_id:
        filters.append(Place.contenttypeid == content_type_id.strip())

    if radius_km is not None and lat is not None and lng is not None:
        latitude_delta = radius_km / 111.0
        longitude_delta = radius_km / max(111.0 * 0.7, 1)
        filters.extend(
            [
                Place.mapy.between(lat - latitude_delta, lat + latitude_delta),
                Place.mapx.between(lng - longitude_delta, lng + longitude_delta),
            ]
        )

    total = db.scalar(select(func.count()).select_from(Place).where(*filters)) or 0
    rows = db.scalars(
        select(Place)
        .where(*filters)
        .order_by(Place.title.asc())
        .offset((page - 1) * size)
        .limit(size)
    ).all()

    serialized_rows = [_serialize_place(row) for row in rows]

    if radius_km is not None and lat is not None and lng is not None:
        within_radius = []
        for row in serialized_rows:
            if row["lat"] is None or row["lng"] is None:
                continue
            distance_km = haversine_km(lat, lng, row["lat"], row["lng"])
            if distance_km <= radius_km:
                row["distance_km"] = round(distance_km, 3)
                within_radius.append(row)

        within_radius.sort(key=lambda item: (item["distance_km"], item["title"]))
        serialized_rows = within_radius
        total = len(within_radius)

    return {
        "items": serialized_rows,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size if total else 0,
    }


@router.get("/{content_id}")
def get_place(content_id: str, db: Session = Depends(get_db)):
    place = db.scalar(select(Place).where(Place.contentid == content_id))
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return _serialize_place(place)

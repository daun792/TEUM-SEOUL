from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.location import Location
from app.schemas.location import LocationList, LocationRead

router = APIRouter(tags=["places"])


@router.get("/places", response_model=LocationList)
def list_places(
    category: str = Query(default=""),
    q: str = Query(default="", max_length=100),
    limit: int = Query(default=30, ge=1, le=100),
    db: Session = Depends(get_db),
) -> LocationList:
    query = select(Location)
    count_query = select(func.count()).select_from(Location)
    if category:
        query = query.where(Location.category == category)
        count_query = count_query.where(Location.category == category)
    if q.strip():
        pattern = f"%{q.strip()}%"
        condition = or_(Location.name.ilike(pattern), Location.address.ilike(pattern))
        query = query.where(condition)
        count_query = count_query.where(condition)
    items = db.scalars(query.order_by(Location.name).limit(limit)).all()
    total = db.scalar(count_query) or 0
    return LocationList(total=total, items=[LocationRead.model_validate(item) for item in items])

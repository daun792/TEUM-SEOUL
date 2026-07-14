from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.location import Location
from app.schemas.course import CourseRequest, CourseResult
from app.services.course_recommender import recommend_course, rebuild_shared_course

router = APIRouter(tags=["courses"])


def _get_performance(db: Session, performance_id: int) -> Location:
    performance = db.get(Location, performance_id)
    if not performance or performance.category != "축제공연행사":
        raise HTTPException(status_code=404, detail="공연을 찾을 수 없습니다.")
    return performance


@router.post("/courses/recommend", response_model=CourseResult)
def create_course(payload: CourseRequest, db: Session = Depends(get_db)) -> CourseResult:
    performance = _get_performance(db, payload.performance_id)
    candidates = list(
        db.scalars(
            select(Location).where(Location.category.in_(["문화시설", "관광지", "쇼핑", "레포츠"]))
        ).all()
    )
    try:
        return recommend_course(payload, performance, candidates)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/courses/shared", response_model=CourseResult)
def shared_course(
    performance_id: int,
    phase: str,
    category: str,
    place_ids: str,
    minutes: int = Query(ge=30, le=180),
    db: Session = Depends(get_db),
) -> CourseResult:
    try:
        request = CourseRequest(
            performance_id=performance_id,
            phase=phase,
            available_minutes=minutes,
            preferred_category=category,
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail="공유 링크 조건이 올바르지 않습니다.") from exc
    performance = _get_performance(db, performance_id)
    try:
        ids = [int(value) for value in place_ids.split(",") if value]
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="장소 ID 형식이 올바르지 않습니다.") from exc
    candidates = list(db.scalars(select(Location).where(Location.id.in_(ids))).all()) if ids else []
    try:
        return rebuild_shared_course(request, performance, candidates, ids)
    except ValueError as exc:
        status = 404 if "찾을 수" in str(exc) else 422
        raise HTTPException(status_code=status, detail=str(exc)) from exc

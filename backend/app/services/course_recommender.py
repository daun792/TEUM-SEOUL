from __future__ import annotations

from itertools import permutations

from app.models.location import Location
from app.schemas.course import (
    CoursePlace,
    CourseRequest,
    CourseResult,
    PerformanceSummary,
)
from app.services.distance import estimated_walk_minutes, haversine_km


STAY_MINUTES = {
    "쇼핑": 30,
    "관광지": 40,
    "문화시설": 50,
    "레포츠": 60,
}
ALLOWED_CATEGORIES = set(STAY_MINUTES)


def _stay_minutes(request: CourseRequest, category: str) -> int:
    base = STAY_MINUTES[category]
    if request.available_minutes <= 45:
        return min(base, 10)
    if request.available_minutes <= 60:
        return min(base, 20)
    if request.available_minutes <= 90:
        return min(base, 35)
    return base


def _distance(a: Location, b: Location) -> float:
    return haversine_km(a.latitude, a.longitude, b.latitude, b.longitude)


def _route_metrics(
    request: CourseRequest, performance: Location, places: list[Location]
) -> tuple[int, int, int, int, list[tuple[float, int]]]:
    previous = performance
    walking = 0
    stay = 0
    segments: list[tuple[float, int]] = []
    for place in places:
        distance = _distance(previous, place)
        walk = estimated_walk_minutes(distance)
        segments.append((distance, walk))
        walking += walk
        stay += _stay_minutes(request, place.category)
        previous = place

    return_walk = 0
    if request.phase == "before" and places:
        return_walk = estimated_walk_minutes(_distance(previous, performance))
        walking += return_walk

    return walking + stay, walking, stay, return_walk, segments


def _build_result(
    request: CourseRequest,
    performance: Location,
    places: list[Location],
    relaxed: bool,
) -> CourseResult:
    total, walk_total, stay_total, return_walk, segments = _route_metrics(
        request, performance, places
    )
    course_places = []
    for place, (distance, walk) in zip(places, segments, strict=True):
        category_match = (
            request.preferred_category == "상관없음"
            or place.category == request.preferred_category
        )
        reason = (
            f"선호한 {place.category}이며 공연장에서 가까워 짧은 시간에 방문하기 좋습니다."
            if category_match
            else f"입력 시간 안에 방문 가능한 가까운 {place.category} 장소입니다."
        )
        course_places.append(
            CoursePlace(
                id=place.id,
                name=place.name,
                category=place.category,
                address=place.address,
                latitude=place.latitude,
                longitude=place.longitude,
                image_url=place.image_url,
                distance_from_previous_km=round(distance, 2),
                walk_minutes=walk,
                stay_minutes=_stay_minutes(request, place.category),
                recommendation_reason=reason,
            )
        )

    return CourseResult(
        performance=PerformanceSummary(
            id=performance.id,
            name=performance.name,
            address=performance.address,
            latitude=performance.latitude,
            longitude=performance.longitude,
            image_url=performance.image_url,
        ),
        phase=request.phase,
        available_minutes=request.available_minutes,
        preferred_category=request.preferred_category,
        places=course_places,
        total_minutes=total,
        total_walk_minutes=walk_total,
        total_stay_minutes=stay_total,
        return_walk_minutes=return_walk,
        buffer_minutes=15 if request.phase == "before" else 0,
        relaxed=relaxed,
    )


def _fits(request: CourseRequest, total_minutes: int) -> bool:
    buffer = 15 if request.phase == "before" else 0
    return total_minutes + buffer <= request.available_minutes


def _find_course(
    request: CourseRequest, performance: Location, candidates: list[Location]
) -> list[Location] | None:
    sorted_candidates = sorted(candidates, key=lambda place: _distance(performance, place))[:20]
    desired_counts = [2, 1] if request.available_minutes > 90 else [1]

    for count in desired_counts:
        if count == 1:
            variants = ([place] for place in sorted_candidates)
        else:
            variants = (list(pair) for pair in permutations(sorted_candidates, 2))

        best: tuple[float, list[Location]] | None = None
        for places in variants:
            total, _walk, _stay, _return, _segments = _route_metrics(
                request, performance, places
            )
            if not _fits(request, total):
                continue
            unused = request.available_minutes - total
            total_distance = _distance(performance, places[0])
            if len(places) == 2:
                total_distance += _distance(places[0], places[1])
            score = unused * 0.1 + total_distance
            if best is None or score < best[0]:
                best = (score, places)
        if best:
            return best[1]
    return None


def recommend_course(
    request: CourseRequest,
    performance: Location,
    candidates: list[Location],
) -> CourseResult:
    usable = [
        place
        for place in candidates
        if place.category in ALLOWED_CATEGORIES
        and place.id != performance.id
        and place.latitude is not None
        and place.longitude is not None
    ]
    preferred = (
        usable
        if request.preferred_category == "상관없음"
        else [place for place in usable if place.category == request.preferred_category]
    )

    selected = _find_course(request, performance, preferred)
    relaxed = False
    if not selected and request.preferred_category != "상관없음":
        selected = _find_course(request, performance, usable)
        relaxed = bool(selected)
    if not selected:
        raise ValueError("입력한 시간 안에 방문 가능한 장소가 없습니다.")
    return _build_result(request, performance, selected, relaxed)


def rebuild_shared_course(
    request: CourseRequest,
    performance: Location,
    candidates: list[Location],
    place_ids: list[int],
) -> CourseResult:
    by_id = {place.id: place for place in candidates}
    if not place_ids or any(identifier not in by_id for identifier in place_ids):
        raise ValueError("공유된 추천 장소를 찾을 수 없습니다.")
    if len(place_ids) > 2:
        raise ValueError("추천 장소는 최대 2개입니다.")
    selected = [by_id[identifier] for identifier in place_ids]
    total, *_ = _route_metrics(request, performance, selected)
    if not _fits(request, total):
        raise ValueError("공유된 코스가 입력 시간 범위를 초과합니다.")
    relaxed = any(
        request.preferred_category not in ("상관없음", place.category)
        for place in selected
    )
    return _build_result(request, performance, selected, relaxed)

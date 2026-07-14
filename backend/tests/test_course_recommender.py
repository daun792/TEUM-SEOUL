from __future__ import annotations

import pytest

from app.models.location import Location
from app.schemas.course import CourseRequest
from app.services.course_recommender import recommend_course, rebuild_shared_course


def loc(identifier, name, category, lat, lon):
    return Location(
        id=identifier,
        content_id=str(identifier),
        name=name,
        category=category,
        latitude=lat,
        longitude=lon,
        address="서울특별시 종로구",
        region="서울",
        image_url="",
        source="한국관광공사 TourAPI 4.0",
    )


def test_before_course_fits_time_and_keeps_buffer():
    performance = loc(1, "테스트 공연", "축제공연행사", 37.5805, 127.0023)
    candidates = [
        loc(2, "가까운 문화시설", "문화시설", 37.5810, 127.0030),
        loc(3, "가까운 관광지", "관광지", 37.5820, 127.0040),
    ]
    request = CourseRequest(
        performance_id=1,
        phase="before",
        available_minutes=90,
        preferred_category="문화시설",
    )

    result = recommend_course(request, performance, candidates)

    assert 1 <= len(result.places) <= 2
    assert result.total_minutes + result.buffer_minutes <= request.available_minutes
    assert result.buffer_minutes == 15
    assert result.places[0].name == "가까운 문화시설"


def test_after_course_prefers_two_places_when_180_minutes_available():
    performance = loc(1, "테스트 공연", "축제공연행사", 37.5805, 127.0023)
    candidates = [
        loc(2, "문화시설 A", "문화시설", 37.5810, 127.0030),
        loc(3, "문화시설 B", "문화시설", 37.5820, 127.0040),
    ]
    request = CourseRequest(
        performance_id=1,
        phase="after",
        available_minutes=180,
        preferred_category="문화시설",
    )

    result = recommend_course(request, performance, candidates)

    assert len(result.places) == 2
    assert result.total_minutes <= 180


def test_recommendation_relaxes_category_when_no_match():
    performance = loc(1, "테스트 공연", "축제공연행사", 37.5805, 127.0023)
    candidates = [loc(3, "관광지 A", "관광지", 37.5810, 127.0030)]
    request = CourseRequest(
        performance_id=1,
        phase="after",
        available_minutes=90,
        preferred_category="문화시설",
    )

    result = recommend_course(request, performance, candidates)

    assert result.relaxed is True
    assert result.places[0].category == "관광지"


def test_shared_course_rejects_unknown_place():
    performance = loc(1, "테스트 공연", "축제공연행사", 37.5805, 127.0023)
    request = CourseRequest(
        performance_id=1,
        phase="after",
        available_minutes=120,
        preferred_category="문화시설",
    )

    with pytest.raises(ValueError, match="추천 장소"):
        rebuild_shared_course(request, performance, [], [999])


def test_thirty_minute_course_uses_quick_stay_window():
    performance = loc(1, "테스트 공연", "축제공연행사", 37.5805, 127.0023)
    candidates = [loc(2, "바로 옆 관광지", "관광지", 37.5806, 127.0024)]
    request = CourseRequest(
        performance_id=1,
        phase="before",
        available_minutes=30,
        preferred_category="관광지",
    )

    result = recommend_course(request, performance, candidates)

    assert len(result.places) == 1
    assert result.places[0].stay_minutes == 10
    assert result.total_minutes + result.buffer_minutes <= 30

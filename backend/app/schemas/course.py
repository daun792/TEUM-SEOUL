from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


AllowedPhase = Literal["before", "after"]
AllowedCategory = Literal["문화시설", "관광지", "쇼핑", "레포츠", "상관없음"]


class CourseRequest(BaseModel):
    performance_id: int
    phase: AllowedPhase
    available_minutes: int = Field(ge=30, le=180)
    preferred_category: AllowedCategory = "상관없음"


class CoursePlace(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    address: str
    latitude: float
    longitude: float
    image_url: str = ""
    distance_from_previous_km: float
    walk_minutes: int
    stay_minutes: int
    recommendation_reason: str


class PerformanceSummary(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    image_url: str = ""


class CourseResult(BaseModel):
    performance: PerformanceSummary
    phase: AllowedPhase
    available_minutes: int
    preferred_category: str
    places: list[CoursePlace]
    total_minutes: int
    total_walk_minutes: int
    total_stay_minutes: int
    return_walk_minutes: int = 0
    buffer_minutes: int = 0
    relaxed: bool = False
    notice: str = "직선거리 기반 예상값이며 실제 이동 경로와 운영시간은 별도 확인이 필요합니다."

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    category: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=1, max_length=100)
    performance_name: str = Field(default="", max_length=255)
    available_minutes: int | None = Field(default=None, ge=30, le=180)


class PostUpdate(PostCreate):
    pass


class PasswordPayload(BaseModel):
    password: str = Field(min_length=1, max_length=100)


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    category: str
    performance_name: str
    available_minutes: int | None
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime


class PostList(BaseModel):
    total: int
    page: int
    size: int
    items: list[PostRead]


class LikeToggleResult(BaseModel):
    liked: bool
    like_count: int

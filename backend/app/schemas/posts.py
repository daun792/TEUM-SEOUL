from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


PostCategory = Literal["축제후기", "주변장소", "자유"]


class PostCreate(BaseModel):
    category: PostCategory = "자유"
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)
    author: str = Field(default="익명", min_length=1, max_length=50)
    festival_id: str | None = Field(default=None, max_length=40)
    password: str = Field(min_length=4, max_length=100)


class PostUpdate(BaseModel):
    category: PostCategory | None = None
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)
    festival_id: str | None = Field(default=None, max_length=40)
    password: str = Field(min_length=4, max_length=100)


class PasswordConfirm(BaseModel):
    password: str = Field(min_length=4, max_length=100)


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: PostCategory
    title: str
    content: str
    author: str
    festival_id: str | None
    created_at: datetime
    updated_at: datetime


class PostPage(BaseModel):
    items: list[PostRead]
    total: int
    page: int
    size: int
    pages: int

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)
    author: str = Field(default="익명", min_length=1, max_length=50)
    password: str = Field(min_length=4, max_length=100)


class PostUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=20_000)
    password: str = Field(min_length=4, max_length=100)


class PasswordConfirm(BaseModel):
    password: str = Field(min_length=4, max_length=100)


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime


class PostPage(BaseModel):
    items: list[PostRead]
    total: int
    page: int
    size: int
    pages: int

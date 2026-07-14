from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.location import LocationRead
from app.schemas.post import PostRead


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
    answer: str
    source: Literal["openai", "fallback"]
    places: list[LocationRead] = Field(default_factory=list)
    posts: list[PostRead] = Field(default_factory=list)

from __future__ import annotations

import re

import httpx
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.post import Post
from app.schemas.chat import ChatMessage, ChatResponse
from app.schemas.location import LocationRead
from app.schemas.post import PostRead


STOPWORDS = {
    "추천", "알려줘", "찾아줘", "공연", "공연전", "공연후", "전", "후", "시간",
    "갈", "곳", "장소", "서울", "남는", "데이트", "코스", "하고", "에서", "근처",
}


class ChatService:
    def __init__(
        self,
        session: Session,
        api_key: str = "",
        model: str = "gpt-4.1-mini",
    ) -> None:
        self.session = session
        self.api_key = api_key
        self.model = model

    def _keywords(self, message: str) -> list[str]:
        tokens = re.findall(r"[가-힣A-Za-z0-9]+", message)
        return [token for token in tokens if len(token) >= 2 and token not in STOPWORDS][:6]

    def _retrieve(self, message: str) -> tuple[list[Location], list[Post]]:
        keywords = self._keywords(message)
        location_query = select(Location)
        post_query = select(Post)
        if keywords:
            location_conditions = []
            post_conditions = []
            for keyword in keywords:
                pattern = f"%{keyword}%"
                location_conditions.extend([
                    Location.name.ilike(pattern),
                    Location.address.ilike(pattern),
                    Location.category.ilike(pattern),
                ])
                post_conditions.extend([
                    Post.title.ilike(pattern),
                    Post.content.ilike(pattern),
                    Post.performance_name.ilike(pattern),
                ])
            location_query = location_query.where(or_(*location_conditions))
            post_query = post_query.where(or_(*post_conditions))
        else:
            location_query = location_query.where(Location.category != "숙박")
        locations = list(self.session.scalars(location_query.limit(5)).all())
        posts = list(self.session.scalars(post_query.order_by(Post.view_count.desc()).limit(3)).all())
        return locations, posts

    def _call_openai(
        self,
        message: str,
        locations: list[Location],
        posts: list[Post],
        history: list[ChatMessage],
    ) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        context_lines = [
            f"장소: {item.name} | 유형: {item.category} | 주소: {item.address}"
            for item in locations
        ] + [
            f"게시글: {item.title} | 카테고리: {item.category} | 내용: {item.content[:200]}"
            for item in posts
        ]
        prompt = "\n".join(context_lines) or "검색 결과 없음"
        messages = [
            {
                "role": "system",
                "content": (
                    "제공된 서울 장소와 게시글만 사용한다. 목록에 없는 장소, 운영시간, "
                    "행사 일정을 만들지 않는다. 직선거리 기반 추천 서비스임을 필요할 때 알린다."
                ),
            }
        ]
        messages.extend(
            {"role": item.role, "content": item.content}
            for item in history[-10:]
        )
        messages.append({"role": "user", "content": f"질문: {message}\n\n근거:\n{prompt}"})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def _fallback(self, locations: list[Location], posts: list[Post]) -> str:
        if not locations and not posts:
            return "조건에 맞는 실제 등록 장소나 후기를 찾지 못했습니다. 공연명이나 지역명을 더 구체적으로 입력해 주세요."
        parts = ["실제 등록된 데이터에서 다음 정보를 찾았습니다."]
        if locations:
            parts.append("장소: " + ", ".join(item.name for item in locations[:5]))
        if posts:
            parts.append("후기: " + ", ".join(item.title for item in posts[:3]))
        parts.append("운영시간과 실제 이동 경로는 방문 전에 별도로 확인해 주세요.")
        return "\n".join(parts)

    def answer(self, message: str, history: list[ChatMessage] | None = None) -> ChatResponse:
        locations, posts = self._retrieve(message)
        try:
            answer = self._call_openai(message, locations, posts, history or [])
            source = "openai"
        except Exception:
            answer = self._fallback(locations, posts)
            source = "fallback"
        return ChatResponse(
            answer=answer,
            source=source,
            places=[LocationRead.model_validate(item) for item in locations],
            posts=[PostRead.model_validate(item) for item in posts],
        )

from __future__ import annotations

from app.models.location import Location
from app.services.chat_service import ChatService


def test_chat_fallback_returns_grounded_places(db_session, monkeypatch):
    db_session.add_all([
        Location(
            content_id="p1",
            name="대학로 공연",
            category="축제공연행사",
            address="서울 종로구 대학로",
            latitude=37.58,
            longitude=127.00,
            region="서울",
            image_url="",
            source="한국관광공사 TourAPI 4.0",
        ),
        Location(
            content_id="c1",
            name="대학로 문화공간",
            category="문화시설",
            address="서울 종로구 대학로",
            latitude=37.581,
            longitude=127.001,
            region="서울",
            image_url="",
            source="한국관광공사 TourAPI 4.0",
        ),
    ])
    db_session.commit()
    service = ChatService(db_session, api_key="test")
    monkeypatch.setattr(service, "_call_openai", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("fail")))

    result = service.answer("대학로 공연 후 문화시설 추천")

    assert result.source == "fallback"
    assert result.places
    assert all(place.name in {"대학로 공연", "대학로 문화공간"} for place in result.places)
    assert "실제 등록된" in result.answer


def test_chat_passes_recent_history_to_openai(db_session, monkeypatch):
    from app.schemas.chat import ChatMessage

    service = ChatService(db_session, api_key="test")
    captured = {}

    def fake_call(message, locations, posts, history):
        captured["message"] = message
        captured["history"] = history
        return "기록을 반영한 답변"

    monkeypatch.setattr(service, "_call_openai", fake_call)
    history = [ChatMessage(role="user", content="대학로 공연을 볼 거야")]

    result = service.answer("공연 후 어디 갈까?", history)

    assert result.source == "openai"
    assert captured["history"] == history

from app.database.models import Place


def test_chat_returns_grounded_place_result_without_openai_key(client, db_session, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    db_session.add(
        Place(
            contentid="place-1",
            title="경복궁",
            category="관광지",
            contenttypeid="12",
            addr1="서울 종로구 사직로 161",
        )
    )
    db_session.commit()

    response = client.post("/api/chat", json={"message": "경복궁 위치 알려줘"})

    assert response.status_code == 200
    assert "경복궁" in response.json()["answer"]
    assert "서울 종로구 사직로 161" in response.json()["answer"]


def test_chat_rejects_blank_message(client):
    response = client.post("/api/chat", json={"message": "   "})

    assert response.status_code == 422

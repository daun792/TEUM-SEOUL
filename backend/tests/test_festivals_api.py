from datetime import date

from app.database.models import Place


def seed_places(db_session):
    festival = Place(
        contentid="festival-1",
        title="서울 여름 음악축제",
        category="축제공연행사",
        contenttypeid="15",
        addr1="서울특별시 중구 세종대로 110",
        mapx=126.9779,
        mapy=37.5663,
        event_start_date=date(2026, 7, 20),
        event_end_date=date(2026, 7, 22),
        firstimage="https://example.com/festival.jpg",
    )
    nearby = Place(
        contentid="place-1",
        title="덕수궁",
        category="관광지",
        contenttypeid="12",
        addr1="서울특별시 중구 세종대로 99",
        mapx=126.9751,
        mapy=37.5658,
    )
    far = Place(
        contentid="place-2",
        title="멀리 있는 장소",
        category="관광지",
        contenttypeid="12",
        mapx=127.2,
        mapy=37.7,
    )
    db_session.add_all([festival, nearby, far])
    db_session.commit()


def test_list_festivals_supports_keyword_and_date_filters(client, db_session):
    seed_places(db_session)

    response = client.get(
        "/api/festivals",
        params={"q": "음악", "start_date": "2026-07-21", "end_date": "2026-07-21"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["title"] == "서울 여름 음악축제"
    assert body["items"][0]["period"] == "2026-07-20 ~ 2026-07-22"


def test_get_festival_detail_and_nearby_places_sorted_by_distance(client, db_session):
    seed_places(db_session)

    detail = client.get("/api/festivals/festival-1")
    nearby = client.get(
        "/api/festivals/festival-1/nearby",
        params={"radius_km": 2, "categories": "관광지"},
    )

    assert detail.status_code == 200
    assert detail.json()["latitude"] == 37.5663
    assert nearby.status_code == 200
    items = nearby.json()["items"]
    assert [item["title"] for item in items] == ["덕수궁"]
    assert 0 < items[0]["distance_km"] < 1


def test_get_missing_festival_returns_404(client):
    response = client.get("/api/festivals/not-found")
    assert response.status_code == 404

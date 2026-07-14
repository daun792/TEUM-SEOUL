from __future__ import annotations

import json

from app.models.location import Location
from app.services.data_loader import load_locations


def test_load_locations_imports_items_and_skips_missing_coordinates(db_session, tmp_path):
    payload = {
        "region": "서울",
        "contentType": "축제공연행사",
        "contentTypeId": 15,
        "total": 2,
        "items": [
            {
                "contentid": "100",
                "title": "테스트 공연",
                "addr1": "서울 종로구",
                "addr2": "",
                "mapx": "127.0",
                "mapy": "37.5",
                "firstimage": "https://example.com/a.jpg",
                "tel": "02-000-0000",
                "lDongSignguCd": "110",
            },
            {
                "contentid": "101",
                "title": "좌표 없는 공연",
                "addr1": "서울 중구",
                "mapx": "",
                "mapy": "",
            },
        ],
    }
    (tmp_path / "서울_축제공연행사.json").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )

    result = load_locations(tmp_path, db_session)

    assert result.inserted == 1
    assert result.skipped == 1
    location = db_session.query(Location).one()
    assert location.name == "테스트 공연"
    assert location.category == "축제공연행사"
    assert location.longitude == 127.0


def test_load_locations_is_idempotent(db_session, tmp_path):
    payload = {
        "region": "서울",
        "contentType": "문화시설",
        "contentTypeId": 14,
        "total": 1,
        "items": [{
            "contentid": "200",
            "title": "테스트 문화시설",
            "addr1": "서울 강남구",
            "mapx": "127.1",
            "mapy": "37.6",
        }],
    }
    path = tmp_path / "서울_문화시설.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    load_locations(tmp_path, db_session)
    load_locations(tmp_path, db_session)

    assert db_session.query(Location).count() == 1

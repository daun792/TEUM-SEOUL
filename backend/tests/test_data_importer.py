import json
from pathlib import Path

import pytest

from app.services.data_importer import ImportValidationError, load_tourapi_file


def test_load_tourapi_file_normalizes_coordinates_and_dates(tmp_path: Path):
    path = tmp_path / "서울_축제공연행사.json"
    path.write_text(
        json.dumps(
            {
                "region": "서울",
                "contentType": "축제공연행사",
                "contentTypeId": 15,
                "total": 1,
                "items": [
                    {
                        "contentid": "100",
                        "contenttypeid": "15",
                        "title": "테스트 축제",
                        "mapx": "126.9780",
                        "mapy": "37.5665",
                        "createdtime": "20260701090000",
                        "modifiedtime": "20260702103000",
                        "eventstartdate": "20260720",
                        "eventenddate": "20260722",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    payload = load_tourapi_file(path)

    assert payload.region == "서울"
    assert payload.items[0].longitude == 126.978
    assert payload.items[0].latitude == 37.5665
    assert payload.items[0].created_at.year == 2026
    assert payload.items[0].event_start_date.isoformat() == "2026-07-20"


def test_load_tourapi_file_rejects_out_of_range_coordinates(tmp_path: Path):
    path = tmp_path / "invalid.json"
    path.write_text(
        json.dumps(
            {
                "region": "서울",
                "contentType": "관광지",
                "contentTypeId": 12,
                "total": 1,
                "items": [
                    {
                        "contentid": "100",
                        "contenttypeid": "12",
                        "title": "잘못된 장소",
                        "mapx": "220.0",
                        "mapy": "37.5",
                        "createdtime": "20260701090000",
                        "modifiedtime": "20260702103000",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    with pytest.raises(ImportValidationError, match="longitude"):
        load_tourapi_file(path)

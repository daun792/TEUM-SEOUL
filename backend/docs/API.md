# 틈서울 백엔드 API 계약

기본 URL은 로컬 실행 기준 `http://localhost:8000`이다. Swagger UI는 `/docs`, OpenAPI JSON은 `/openapi.json`에서 확인한다.

## 축제 목록

`GET /api/festivals?q=&start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&page=1&size=20`

```json
{
  "items": [
    {
      "id": "2556687",
      "content_id": "2556687",
      "title": "문학주간 2026",
      "name": "문학주간 2026",
      "category": "축제공연행사",
      "content_type_id": "15",
      "address": "서울특별시 종로구 대학로 104 (동숭동)",
      "longitude": 127.0023742293,
      "latitude": 37.580512461,
      "lng": 127.0023742293,
      "lat": 37.580512461,
      "event_start_date": null,
      "event_end_date": null,
      "period": null
    }
  ],
  "total": 201,
  "page": 1,
  "size": 20,
  "pages": 11
}
```

원본 파일에 `eventstartdate`, `eventenddate`가 없으면 날짜와 `period`는 `null`이다. 날짜 필터를 사용하면 날짜가 없는 항목은 제외된다.

## 축제 상세

`GET /api/festivals/{content_id}`

목록 항목과 동일한 구조의 단일 객체를 반환한다. 존재하지 않거나 축제 유형이 아니면 `404`다.

## 주변 장소

`GET /api/festivals/{content_id}/nearby?radius_km=2&categories=관광지,문화시설&limit=30`

```json
{
  "festival_id": "2556687",
  "radius_km": 2.0,
  "items": [
    {
      "id": "126508",
      "title": "대학로",
      "category": "관광지",
      "latitude": 37.581,
      "longitude": 127.002,
      "distance_km": 0.082
    }
  ],
  "total": 1
}
```

SQLite에서 위·경도 bounding box로 후보를 제한하고 Haversine 공식으로 실제 거리를 계산한다.

## 익명 게시판

### 목록

`GET /api/posts?q=&page=1&size=20`

제목과 본문을 검색하고 최신순으로 페이지네이션한다.

### 작성

`POST /api/posts`

```json
{
  "title": "한강 축제 후기",
  "content": "공연이 좋았습니다.",
  "author": "익명",
  "password": "1234"
}
```

### 비밀번호 확인

`POST /api/posts/{id}/verify-password`

```json
{ "password": "1234" }
```

일치하면 `204`, 불일치하면 `403`이다.

### 수정·삭제

- `PUT /api/posts/{id}`: 제목, 본문, 비밀번호 전송
- `DELETE /api/posts/{id}`: JSON 본문으로 비밀번호 전송

비밀번호는 PBKDF2-SHA256으로 해시 저장하며 API 응답에 포함하지 않는다.

## 데이터 적재

```bash
cd backend
python scripts/load_data.py --data-dir data --region 서울
```

입력 JSON의 경도·위도, 등록·수정 시각, 선택적 행사 날짜를 검증한다. 같은 `contentid`는 업데이트 처리하여 재실행해도 중복 행이 생기지 않는다.

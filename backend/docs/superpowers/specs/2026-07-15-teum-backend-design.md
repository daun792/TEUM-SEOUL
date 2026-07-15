# 틈서울 백엔드 설계

## 범위

WBS 중 백엔드 담당 범위만 구현한다. TourAPI JSON 검증·적재, 축제 목록/상세/주변 장소 조회, 익명 게시판 CRUD·비밀번호 검증·검색·페이지네이션, CORS·환경변수·Render 설정을 포함한다. 프론트엔드와 OpenAI 챗봇은 제외한다.

## 구조

FastAPI 라우터가 HTTP 계약을 담당하고 SQLAlchemy 모델이 SQLite 저장소를 담당한다. TourAPI 적재기는 원본 파일을 Pydantic으로 검증한 후 `contentid` 기준으로 upsert한다. 주변 장소는 SQLite bounding box로 후보를 줄인 뒤 Haversine 공식으로 정확한 거리를 계산한다.

## 데이터 제약

- `mapx`: -180~180 경도
- `mapy`: -90~90 위도
- `createdtime`, `modifiedtime`: YYYYMMDDHHmmss
- 선택적 `eventstartdate`, `eventenddate`: YYYYMMDD
- 게시글 비밀번호: PBKDF2-SHA256 해시 저장

## API

- `GET /api/festivals`
- `GET /api/festivals/{content_id}`
- `GET /api/festivals/{content_id}/nearby`
- `GET/POST /api/posts`
- `GET/PUT/DELETE /api/posts/{id}`
- `POST /api/posts/{id}/verify-password`

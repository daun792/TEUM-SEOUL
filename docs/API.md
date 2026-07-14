# API 요약

| Method | Endpoint | 설명 |
|---|---|---|
| GET | `/api/health` | 서버 상태 |
| GET | `/api/performances?q=&limit=` | 공연·축제 검색 |
| GET | `/api/places?category=&q=&limit=` | 장소 조회 |
| POST | `/api/courses/recommend` | 조건 기반 코스 추천 |
| GET | `/api/courses/shared` | 공유 결과 검증·재구성 |
| GET | `/api/posts?q=&category=&ids=&page=&size=` | 게시글 검색·북마크 조회 |
| GET | `/api/posts/{id}` | 상세 및 조회수 증가 |
| POST | `/api/posts` | 작성 |
| PUT | `/api/posts/{id}` | 비밀번호 검증 후 수정 |
| DELETE | `/api/posts/{id}` | 비밀번호 검증 후 삭제 |
| POST | `/api/posts/{id}/likes/toggle` | 익명 좋아요 toggle |
| POST | `/api/chat` | 공공데이터·게시글 기반 챗봇 |

## 추천 요청 예시

```json
{
  "performance_id": 6318,
  "phase": "before",
  "available_minutes": 90,
  "preferred_category": "문화시설"
}
```

## 좋아요 요청

```http
POST /api/posts/1/likes/toggle
X-Client-ID: 0d0433e7-62a4-4ce9-a8cd-b987d46ef123
```

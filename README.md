# 틈서울

**공연 전후 남는 시간을 채워주는 초단기 서울 코스 커뮤니티**

서울의 축제·공연을 선택하고 공연 전·후 30~180분과 선호 카테고리를 입력하면, 한국관광공사 공공데이터의 실제 장소 1~2개로 짧은 일정을 구성합니다. 지도·날씨·길찾기 API 없이 위경도 직선거리와 예상 도보시간을 계산합니다.

## 구현 기능

- 서울 축제·공연 201건 검색
- 공연 전·후 30~180분 초단기 코스 추천
- 문화시설·관광지·쇼핑·레포츠 5,843건 후보 활용
- 공연 전 코스의 15분 복귀 버퍼
- 직선거리 × 1.25와 도보속도 4.5km/h를 이용한 예상 도보시간
- 익명 게시판 CRUD와 비밀번호 기반 수정·삭제
- 게시글 검색·카테고리 필터·조회수
- 브라우저별 익명 좋아요 toggle
- localStorage 기반 북마크와 내 북마크 목록
- 추천 결과 공유 URL, Web Share API, 클립보드 fallback
- 실제 장소·게시글 검색에 근거한 챗봇과 OpenAI 장애 fallback
- 모바일 반응형 UI

## 기술 스택

| 영역 | 기술 |
|---|---|
| Frontend | Vue.js 3, Vite, Vue Router, Axios |
| Backend | FastAPI, SQLAlchemy 2, Pydantic 2 |
| Database | SQLite |
| AI | OpenAI Chat Completions API, 검색 결과 grounding |
| Test | Pytest, Vitest, Vue Test Utils |
| Deploy | Netlify, Render |

## 프로젝트 구조

```text
teum-seoul/
├─ frontend/                 # Vue.js 3 SPA
│  ├─ src/components/
│  ├─ src/views/
│  ├─ src/composables/
│  └─ tests/
├─ backend/                  # FastAPI + SQLite
│  ├─ app/api/routes/
│  ├─ app/models/
│  ├─ app/services/
│  ├─ tests/
│  └─ teum_seoul.db          # 초기 데이터 포함 제출용 DB
├─ data/raw/seoul/           # 제공받은 서울 JSON 원본
├─ docs/
├─ run_local.bat
├─ run_backend.bat
├─ run_frontend.bat
├─ netlify.toml
└─ render.yaml
```

## 로컬 실행

### 한 번에 실행

Windows:

```bat
run_local.bat
```

`run_local.bat`은 API와 웹 개발 서버를 별도 창으로 실행합니다. 배치 파일은 Windows 기본 코드페이지에서도 깨지지 않도록 ASCII와 CRLF 형식으로 제공되며, 필요한 Python·npm 패키지가 없으면 각 실행 창에서 자동 설치합니다.

macOS/Linux:

```bash
./run_local.sh
```

### 직접 실행

백엔드:

```bash
cd backend
pip install -r requirements.txt
python scripts/init_db.py --reset
uvicorn app.main:app --reload --port 8000
```

프론트엔드:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

- 웹: `http://localhost:5173`
- API 문서: `http://localhost:8000/docs`
- 상태 확인: `http://localhost:8000/api/health`

## 환경변수

백엔드 `.env` 또는 배포 환경변수:

```env
DATABASE_URL=sqlite:///./teum_seoul.db
FRONTEND_ORIGIN=http://localhost:5173
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
DATA_DIR=../data/raw/seoul
```

프론트엔드 `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

`OPENAI_API_KEY`가 없거나 호출에 실패해도 장소·게시글 검색 결과를 이용한 기본 응답이 동작합니다.

## 테스트

```bash
cd backend
pytest -q

cd ../frontend
npm test
npm run build
```

## 배포

### Render

저장소의 `render.yaml`을 이용합니다. `FRONTEND_ORIGIN`에는 최종 Netlify URL을 입력하고, 필요한 경우 `OPENAI_API_KEY`를 등록합니다.

SQLite는 Render 인스턴스 재시작·재배포 시 작성 데이터가 초기화될 수 있습니다. 교육용 시연에서는 초기 DB를 저장소와 제출 산출물로 함께 관리하며, 영속성이 필요하면 Render Persistent Disk 또는 외부 DB로 전환해야 합니다.

### Netlify

저장소의 `netlify.toml`을 사용합니다. Netlify 환경변수 `VITE_API_BASE_URL`에 Render API URL을 등록합니다.

## 데이터 출처

이 서비스는 한국관광공사 TourAPI 4.0의 데이터를 활용했습니다.

- 제공 기관: 한국관광공사
- 라이선스: 공공누리 제3유형, 출처 표시 + 변경 금지
- 실제 ZIP 포함 서울 데이터: 7종 6,518건
- `SOURCE.md`에 기재된 음식점 1,632건 파일은 실제 ZIP에 포함되지 않아 사용하지 않았습니다.

자세한 내용은 [`docs/데이터출처_라이선스.md`](docs/데이터출처_라이선스.md)를 확인하세요.

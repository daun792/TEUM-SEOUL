# 틈서울 통합 프로젝트

Vue 3 프론트엔드, FastAPI 백엔드, OpenAI 기반 관광 챗봇을 하나의 저장소로 통합한 배포용 구성입니다.

## 디렉터리

- `frontend/`: Netlify 배포 대상 Vue/Vite 앱
- `backend/`: Render 배포 대상 FastAPI 앱과 TourAPI 데이터
- `netlify.toml`: Netlify 빌드 및 SPA 라우팅 설정
- `render.yaml`: Render Blueprint 설정

## 로컬 실행

### 백엔드

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python scripts/load_data.py --data-dir data --region 서울
uvicorn app.main:app --reload
```

`backend/.env`의 `OPENAI_API_KEY`가 비어 있으면 챗봇은 DB 검색 결과를 그대로 정리해 반환합니다. 키가 있으면 OpenAI가 검색 결과를 기반으로 답변합니다.

### 프론트엔드

```bash
cd frontend
npm ci
cp .env.example .env
npm run dev
```

로컬 기본 백엔드 주소는 `http://localhost:8000`입니다.

## Render 배포

1. 저장소 루트의 `render.yaml`을 사용하는 Blueprint로 Web Service를 생성합니다.
2. Render 환경 변수에 `OPENAI_API_KEY`를 등록합니다.
3. `CORS_ORIGINS`에 최종 Netlify 주소를 입력합니다.

예시:

```text
CORS_ORIGINS=https://your-site.netlify.app
```

## Netlify 배포

저장소 루트를 연결하면 `netlify.toml`이 다음 설정을 적용합니다.

- Base directory: `frontend`
- Build command: `npm run build`
- Publish directory: `frontend/dist`

Netlify 환경 변수에 Render 백엔드 URL을 등록합니다.

```text
VITE_API_BASE_URL=https://your-render-service.onrender.com
```

환경 변수를 변경한 뒤에는 프론트엔드를 다시 배포해야 합니다.

## 검증

```bash
cd backend && pytest -q
cd frontend && npm test && npm run build
```

## 보안

`OPENAI_API_KEY`는 프론트엔드 또는 Git 저장소에 넣지 않습니다. Render의 서버 환경 변수로만 설정합니다.

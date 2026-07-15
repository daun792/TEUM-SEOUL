# TEUM SEOUL Backend

FastAPI, SQLAlchemy, SQLite 기반 틈서울 백엔드다.

## 실행

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

## 테스트

```bash
pytest -q
```

## 데이터 출처

한국관광공사 TourAPI 4.0 원본 JSON을 사용한다. 세부 출처와 이용 조건은 `data/**/SOURCE.md`를 따른다.

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.festivals import router as festivals_router
from app.api.posts import router as posts_router
from app.core.config import get_settings
from app.database.database import Base, engine

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(festivals_router)
app.include_router(posts_router)


@app.get("/")
def root():
    return {"message": "틈서울 백엔드 서버 실행중", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.app_env}

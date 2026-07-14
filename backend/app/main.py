from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, courses, health, performances, places, posts
from app.core.config import settings
from app.db.session import Base, engine
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="틈서울 API",
    version="1.0.0",
    description="공연 전후 30~180분 초단기 서울 코스 커뮤니티 API",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.frontend_origin.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [health.router, performances.router, places.router, courses.router, posts.router, chat.router]:
    app.include_router(router, prefix="/api")

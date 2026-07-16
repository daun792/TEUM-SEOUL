from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def ensure_sqlite_schema() -> None:
    if not settings.database_url.startswith("sqlite"):
        return

    with engine.begin() as connection:
        table_exists = connection.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='posts'"
        ).fetchone()
        if not table_exists:
            return

        columns = {
            row[1]
            for row in connection.exec_driver_sql("PRAGMA table_info(posts)").fetchall()
        }

        if "category" not in columns:
            connection.exec_driver_sql(
                "ALTER TABLE posts ADD COLUMN category VARCHAR(30) NOT NULL DEFAULT '자유'"
            )
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS ix_posts_category ON posts (category)"
            )

        if "festival_id" not in columns:
            connection.exec_driver_sql("ALTER TABLE posts ADD COLUMN festival_id VARCHAR(40)")
            connection.exec_driver_sql(
                "CREATE INDEX IF NOT EXISTS ix_posts_festival_id ON posts (festival_id)"
            )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

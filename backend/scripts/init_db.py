from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func, select

from app.core.config import settings
from app.db.session import Base, SessionLocal, engine
from app.models.location import Location
from app.models.post import Post
from app.services.data_loader import load_locations


DEMO_POSTS = [
    {
        "title": "대학로 공연 전 90분, 문화공간 한 곳",
        "content": "공연장과 가까운 문화시설을 들렀다가 15분 전에 돌아왔습니다. 이동시간이 짧아서 마음이 급하지 않았어요.",
        "category": "공연 전 코스",
        "password": "1234",
        "performance_name": "문학주간 2026",
        "available_minutes": 90,
    },
    {
        "title": "공연 후 2시간 쇼핑 코스 후기",
        "content": "공연이 끝난 뒤 가까운 쇼핑 장소 두 곳을 이어서 방문했습니다. 실제 운영시간은 미리 확인하는 게 좋습니다.",
        "category": "공연 후 코스",
        "password": "1234",
        "performance_name": "서울 축제·공연",
        "available_minutes": 120,
    },
    {
        "title": "짧은 틈에는 한 곳만 가도 충분해요",
        "content": "30분에서 1시간 정도라면 여러 곳보다 가까운 장소 하나를 여유 있게 보는 편이 좋았습니다.",
        "category": "장소 후기",
        "password": "1234",
        "performance_name": "",
        "available_minutes": 60,
    },
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--data-dir", type=Path, default=settings.data_dir)
    parser.add_argument("--no-demo-posts", action="store_true")
    args = parser.parse_args()

    if args.reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        result = load_locations(args.data_dir, session)
        if not args.no_demo_posts and (session.scalar(select(func.count()).select_from(Post)) or 0) == 0:
            session.add_all([Post(**post) for post in DEMO_POSTS])
            session.commit()
        counts = dict(
            session.execute(
                select(Location.category, func.count()).group_by(Location.category)
            ).all()
        )
        print(f"inserted={result.inserted} updated={result.updated} skipped={result.skipped}")
        print(f"category_counts={counts}")


if __name__ == "__main__":
    main()

import argparse
from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database.database import Base, SessionLocal, engine  # noqa: E402
from app.services.data_importer import import_directory  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Import TourAPI JSON data into SQLite")
    parser.add_argument("--data-dir", type=Path, default=BACKEND_DIR / "data")
    parser.add_argument("--region", default="서울")
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        result = import_directory(db, args.data_dir, region=args.region)
    print(
        "Import complete: "
        f"files={result['files']} inserted={result['inserted']} "
        f"updated={result['updated']} total={result['total']}"
    )


if __name__ == "__main__":
    main()

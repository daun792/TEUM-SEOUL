import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.database.database import engine
from app.database.models import Base


Base.metadata.create_all(bind=engine)

print("DB 생성 완료")
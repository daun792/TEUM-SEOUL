import json
import os
import sys


# backend 경로를 import path에 추가
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from app.database.database import SessionLocal
from app.database.models import Place


DATA_DIR = "./data"


FILES = [
    ("서울_관광지.json", "관광지"),
    ("서울_문화시설.json", "문화시설"),
    ("서울_숙박.json", "숙박"),
    ("서울_쇼핑.json", "쇼핑"),
    ("서울_레포츠.json", "레포츠"),
    ("서울_여행코스.json", "여행코스"),
    ("서울_축제공연행사.json", "축제"),
]


def load_json_file(filepath):
    """
    JSON 파일에서 items 배열만 반환
    """

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    return data["items"]


def insert_places(filepath, category):
    """
    JSON 데이터를 SQLite places 테이블에 저장
    """

    db = SessionLocal()

    items = load_json_file(filepath)

    count = 0

    for item in items:

        place = Place(

            contentid=item.get("contentid"),

            title=item.get("title"),

            category=category,

            contenttypeid=item.get("contenttypeid"),

            addr1=item.get("addr1"),

            addr2=item.get("addr2"),

            mapx=float(item["mapx"])
            if item.get("mapx")
            else None,

            mapy=float(item["mapy"])
            if item.get("mapy")
            else None,

            tel=item.get("tel"),

            firstimage=item.get("firstimage"),

            firstimage2=item.get("firstimage2"),

            createdtime=item.get("createdtime"),

            modifiedtime=item.get("modifiedtime")
        )


        db.add(place)

        count += 1


    db.commit()

    db.close()


    print(
        f"{category} 데이터 저장 완료 : {count}개"
    )


if __name__ == "__main__":

    for filename, category in FILES:

        filepath = os.path.join(
            DATA_DIR,
            filename
        )

        if os.path.exists(filepath):

            insert_places(
                filepath,
                category
            )

        else:

            print(
                f"파일 없음 : {filepath}"
            )
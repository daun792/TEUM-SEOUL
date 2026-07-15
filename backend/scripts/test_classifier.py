from app.services.question_classifier import classify_question


questions = [

    "서울 축제 알려줘",

    "한강 관광지 추천해줘",

    "경복궁 위치 알려줘",

    "명동 숙박 추천해줘",

    "강남 쇼핑 추천해줘",

    "박물관 추천해줘",

    "후기 찾아줘"

]


for q in questions:

    print(
        q,
        "=>",
        classify_question(q)
    )
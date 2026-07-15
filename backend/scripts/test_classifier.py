from app.services.question_classifier import classify_question


questions = [

    "서울 축제 알려줘",

    "한강 근처 관광지 추천해줘",

    "경복궁 위치 알려줘",

    "후기 찾아줘"

]


for q in questions:

    print(
        q,
        "=>",
        classify_question(q)
    )
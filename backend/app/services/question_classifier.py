def extract_keyword(message: str):

    remove_words = [
        "추천해줘",
        "추천",
        "알려줘",
        "알려",
        "찾아줘",
        "찾아",
        "정보",
        "위치",
        "어디",
        "일정",
        "기간",
        "관광지",
        "관광",
        "축제",
        "행사",
        "공연",
        "후기",
        "리뷰",
        "게시글",
        "근처",
        "주변",
        "가볼만한",
        "가볼",
        "숙박",
        "쇼핑",
        "호텔",
        "문화시설",
        "레포츠"
    ]

    keyword = message

    for word in remove_words:
        keyword = keyword.replace(word, "")

    return keyword.strip()



def classify_question(message: str):

    message = message.lower()

    keyword = extract_keyword(message)


    # 커뮤니티
    if any(
        word in message
        for word in [
            "후기",
            "리뷰",
            "게시글"
        ]
    ):

        return {
            "question_type": "community",
            "category": None,
            "keyword": keyword
        }


    # 축제
    if any(
        word in message
        for word in [
            "축제",
            "행사",
            "공연"
        ]
    ):

        return {
            "question_type": "festival",
            "category": "축제",
            "keyword": keyword
        }


    # 위치 검색
    if any(
        word in message
        for word in [
            "주소",
            "위치",
            "어디"
        ]
    ):

        if "숙박" in message or "호텔" in message:
            category = "숙박"
        elif "쇼핑" in message:
            category = "쇼핑"
        elif any(
            word in message
            for word in [
                "문화시설",
                "박물관",
                "전시"
            ]
        ):
            category = "문화시설"
        else:
            category = "관광지"

        return {
            "question_type": "place",
            "category": category,
            "keyword": keyword
        }


    # 숙박
    if "숙박" in message or "호텔" in message:

        return {
            "question_type": "recommend",
            "category": "숙박",
            "keyword": keyword
        }


    # 여행코스
    if "여행코스" in message or "코스" in message:

        return {
            "question_type": "recommend",
            "category": "여행코스",
            "keyword": keyword
        }


    # 쇼핑
    if "쇼핑" in message:

        return {
            "question_type": "recommend",
            "category": "쇼핑",
            "keyword": keyword
        }


    # 문화시설
    if any(
        word in message
        for word in [
            "문화시설",
            "박물관",
            "전시"
        ]
    ):

        return {
            "question_type": "recommend",
            "category": "문화시설",
            "keyword": keyword
        }


    # 레포츠
    if any(
        word in message
        for word in [
            "레포츠",
            "운동",
            "자전거"
        ]
    ):

        return {
            "question_type": "recommend",
            "category": "레포츠",
            "keyword": keyword
        }


    # 관광지 기본
    if any(
        word in message
        for word in [
            "추천",
            "가볼",
            "관광"
        ]
    ):

        return {
            "question_type": "recommend",
            "category": "관광지",
            "keyword": keyword
        }


    return {
        "question_type": "unknown",
        "category": None,
        "keyword": keyword
    }
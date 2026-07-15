REMOVE_WORDS = [
    "추천해줘", "추천", "알려줘", "알려", "찾아줘", "찾아", "정보",
    "주소", "위치", "어디", "일정", "기간", "관광지", "관광",
    "축제", "행사", "공연", "후기", "리뷰", "게시글", "근처", "주변",
    "가볼만한", "가볼 만한", "가볼", "숙박", "쇼핑", "호텔", "문화시설",
    "여행코스", "여행 코스", "레포츠", "이번", "주말", "오늘", "무료",
    "아이와", "갈 만한 곳", "곳",
]


def extract_keyword(message: str) -> str:
    keyword = message
    for word in REMOVE_WORDS:
        keyword = keyword.replace(word, " ")
    return " ".join(keyword.split())


def classify_question(message: str) -> dict[str, str | None]:
    normalized = message.lower()
    keyword = extract_keyword(normalized)

    if any(word in normalized for word in ["후기", "리뷰", "게시글"]):
        return {"question_type": "community", "category": None, "keyword": keyword}

    if any(word in normalized for word in ["축제", "행사", "공연"]):
        return {
            "question_type": "festival",
            "category": "축제공연행사",
            "keyword": keyword,
        }

    if any(word in normalized for word in ["주소", "위치", "어디"]):
        if "숙박" in normalized or "호텔" in normalized:
            category = "숙박"
        elif "쇼핑" in normalized:
            category = "쇼핑"
        elif any(word in normalized for word in ["문화시설", "박물관", "전시"]):
            category = "문화시설"
        else:
            category = "관광지"
        return {"question_type": "place", "category": category, "keyword": keyword}

    category_rules = [
        (["숙박", "호텔"], "숙박"),
        (["여행코스", "여행 코스"], "여행코스"),
        (["쇼핑"], "쇼핑"),
        (["문화시설", "박물관", "전시"], "문화시설"),
        (["레포츠", "운동", "자전거"], "레포츠"),
    ]
    for words, category in category_rules:
        if any(word in normalized for word in words):
            return {"question_type": "recommend", "category": category, "keyword": keyword}

    if any(word in normalized for word in ["추천", "가볼", "관광"]):
        return {"question_type": "recommend", "category": "관광지", "keyword": keyword}

    return {"question_type": "unknown", "category": None, "keyword": keyword}

def classify_question(message: str):

    message = message.lower()



    if any(
        word in message
        for word in [
            "축제",
            "행사",
            "공연"
        ]
    ):

        return "festival"



    if any(
        word in message
        for word in [
            "추천",
            "가볼",
            "관광"
        ]
    ):

        return "recommend"



    if any(
        word in message
        for word in [
            "주소",
            "위치",
            "어디"
        ]
    ):

        return "place"



    if any(
        word in message
        for word in [
            "후기",
            "리뷰",
            "게시글"
        ]
    ):

        return "community"



    return "unknown"
from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 로드
load_dotenv()


class OpenAIService:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

        self.client = OpenAI(api_key=api_key)

    def generate_answer(
        self,
        question: str,
        search_result: str
    ) -> str:

        system_prompt = """
당신은 서울 관광 정보 챗봇 '틈서울'입니다.

[역할]
사용자가 서울 관광지, 축제, 장소 정보를 질문하면
제공된 검색 결과를 바탕으로 자연스럽게 답변합니다.

[중요 규칙]
1. 반드시 검색 결과에 포함된 정보만 사용합니다.
2. 검색 결과에 없는 내용은 절대 추측하지 않습니다.
3. 운영시간, 입장료, 후기, 추천코스 등은 검색 결과에 있을 때만 언급합니다.
4. 관광지명과 주소를 중심으로 정리합니다.
5. 답변은 친절하고 간결하게 작성합니다.
6. 마크다운 표는 사용하지 않습니다.
7. 답변 길이는 5~10줄 정도로 작성합니다.

[검색 결과가 없는 경우]
아래 문구를 그대로 출력합니다.

죄송합니다. 관련 정보를 찾지 못했습니다.

예시 질문
- 한강 관광지 추천해줘
- 강남 관광지 추천해줘
- 서울불꽃축제 일정 알려줘
- 경복궁 정보 알려줘
- 불꽃축제 후기 찾아줘
"""

        user_prompt = f"""
사용자 질문:
{question}

검색 결과:
{search_result}
"""

        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.choices[0].message.content
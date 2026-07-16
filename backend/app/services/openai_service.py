from app.core.config import get_settings


class OpenAIUnavailable(RuntimeError):
    """Raised when the optional OpenAI response generator cannot be used."""


class OpenAIService:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model

    def generate_answer(self, question: str, search_result: str) -> str:
        if not self.api_key:
            raise OpenAIUnavailable("OPENAI_API_KEY is not configured")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise OpenAIUnavailable("openai package is not installed") from exc

        system_prompt = """
당신은 서울 관광 정보 챗봇 '틈서울'입니다.
제공된 검색 결과만 사용해 한국어로 친절하고 간결하게 답변합니다.
검색 결과에 없는 운영시간, 입장료, 특징, 후기, 이동 순서 등은 추측하지 않습니다.
마크다운 표는 사용하지 않습니다.
축제는 축제명, 장소, 기간을 우선 정리하고, 기간이 없으면 데이터에 일정 정보가 없다고 안내합니다.
""".strip()

        try:
            response = OpenAI(api_key=self.api_key).chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"사용자 질문:\n{question}\n\n검색 결과:\n{search_result}",
                    },
                ],
            )
        except Exception as exc:  # API/network failures fall back to deterministic output.
            raise OpenAIUnavailable(str(exc)) from exc

        content = response.choices[0].message.content
        if not content:
            raise OpenAIUnavailable("OpenAI returned an empty response")
        return content.strip()

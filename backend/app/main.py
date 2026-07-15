from fastapi import FastAPI

from app.routers.chat import router as chat_router


app = FastAPI(
    title="틈서울 AI Chatbot API"
)


app.include_router(chat_router)


@app.get("/")
def root():

    return {
        "message": "틈서울 챗봇 서버 실행중"
    }
from fastapi import FastAPI


app = FastAPI(
    title="틈서울 AI Chatbot API"
)


@app.get("/")
def root():

    return {
        "message": "틈서울 챗봇 서버 실행중"
    }
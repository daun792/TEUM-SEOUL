# 통합 내역

- 프론트엔드는 `TEUM-SEOUL-feature-frontend.zip`을 기준으로 채택했습니다.
- 백엔드는 `TEUM-SEOUL-feature-backend.zip`의 축제·커뮤니티 API, 데이터 importer, 테스트 구조를 기준으로 채택했습니다.
- AI 챗봇은 `TEUM-SEOUL-main (1).zip`의 분류기·DB 검색·OpenAI 응답 생성 로직을 새 백엔드 구조에 맞춰 이식했습니다.
- 프론트엔드 챗봇 UI를 `POST /api/chat`에 연결하고 중복 전송 방지, 로딩 상태, 오류 표시, 자유 입력을 추가했습니다.
- OpenAI 키가 없거나 API 호출이 실패할 경우 서버가 중단되지 않고 DB 기반 응답으로 대체됩니다.
- 루트에 Netlify 및 Render 배포 설정을 배치했습니다.

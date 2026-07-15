<script setup>
import { ref } from 'vue'
import mascotImage from '../../assets/chatbot-mascot.webp'

const isOpen = ref(false)
const suggestions = ['이번 주말 축제', '무료 축제', '아이와 갈 만한 곳', '축제 주변 관광지']
const messages = ref([{ role: 'bot', text: '안녕하세요. 서울 축제 도우미예요.' }])

const askSuggestion = (question) => {
  messages.value.push({ role: 'user', text: question })
  messages.value.push({ role: 'bot', text: '현재는 UI 미리보기 상태입니다.' })
}
</script>

<template>
  <div class="chatbot-wrap">
    <section v-if="isOpen" class="chat-panel section-card" aria-label="서울 축제 도우미">
      <header>
        <img :src="mascotImage" alt="서울 축제 도우미" class="bot-avatar" />
        <div>
          <strong>서울 축제 도우미</strong>
          <span>무엇을 찾고 있나요?</span>
        </div>
        <button type="button" aria-label="챗봇 닫기" @click="isOpen = false">×</button>
      </header>

      <div class="messages">
        <p v-for="(message, index) in messages" :key="index" :class="message.role">
          {{ message.text }}
        </p>
      </div>

      <div class="suggestions">
        <button v-for="item in suggestions" :key="item" type="button" @click="askSuggestion(item)">
          {{ item }}
        </button>
      </div>
    </section>

    <button v-else type="button" class="chat-fab" aria-label="챗봇 열기" @click="isOpen = true">
      <img :src="mascotImage" alt="서울 축제 도우미" class="fab-avatar" aria-hidden="true" />
      <span class="fab-copy">
        <strong>서울 축제 도우미</strong>
        <small>어디로 떠나볼까요?</small>
      </span>
      <span class="fab-arrow" aria-hidden="true">⌃</span>
    </button>
  </div>
</template>

<style scoped>
.chatbot-wrap {
  position: fixed;
  right: 24px;
  bottom: 22px;
  z-index: 1500;
}

.chat-fab {
  min-width: 310px;
  min-height: 74px;
  display: grid;
  grid-template-columns: 56px 1fr 32px;
  align-items: center;
  gap: 10px;
  padding: 8px 11px;
  border: 1px solid #9dcc83;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: var(--shadow-float);
  cursor: pointer;
}

.fab-avatar,
.bot-avatar {
  border-radius: 50%;
}

.fab-avatar {
  width: 54px;
  height: 54px;
}

.fab-avatar::after,
.bot-avatar::after {
  content: '캐릭터';
  padding: 3px 5px;
  font-size: 7px;
}

.fab-copy {
  display: grid;
  gap: 2px;
  text-align: left;
}

.fab-copy strong {
  color: var(--color-primary-dark);
  font-size: 15px;
}

.fab-copy small {
  color: #6c7a72;
  font-size: 11px;
}

.fab-arrow {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #a5cf8e;
  color: #fff;
}

.chat-panel {
  width: min(360px, calc(100vw - 28px));
  padding: 14px;
  border-radius: 20px;
}

.chat-panel header {
  display: grid;
  grid-template-columns: 44px 1fr 32px;
  align-items: center;
  gap: 9px;
}

.bot-avatar {
  width: 42px;
  height: 42px;
}

.chat-panel header div:nth-child(2) {
  display: grid;
}

.chat-panel header strong {
  color: var(--color-primary-dark);
  font-size: 14px;
}

.chat-panel header span {
  color: #728078;
  font-size: 11px;
}

.chat-panel header button {
  width: 30px;
  height: 30px;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
}

.messages {
  min-height: 130px;
  display: grid;
  align-content: start;
  gap: 8px;
  margin-top: 12px;
  padding: 10px;
  border-radius: 14px;
  background: #f7faf3;
}

.messages p {
  width: fit-content;
  max-width: 85%;
  margin: 0;
  padding: 8px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.messages .bot {
  background: #eaf5e1;
}

.messages .user {
  justify-self: end;
  background: #e8f2fb;
}

.suggestions {
  display: grid;
  gap: 7px;
  margin-top: 10px;
}

.suggestions button {
  padding: 9px 11px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  background: #fff;
  color: #3d5648;
  font-size: 12px;
  font-weight: 750;
  text-align: left;
  cursor: pointer;
}

@media (max-width: 720px) {
  .chatbot-wrap {
    right: 12px;
    bottom: 12px;
  }

  .chat-fab {
    min-width: 62px;
    min-height: 62px;
    grid-template-columns: 1fr;
    padding: 4px;
    border-radius: 50%;
  }

  .fab-copy,
  .fab-arrow {
    display: none;
  }
}
</style>

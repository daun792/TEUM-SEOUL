<script setup>
import { ref } from 'vue'

const isOpen = ref(false)

const suggestions = [
  '이번 주말 축제',
  '무료 축제',
  '아이와 갈 만한 곳',
  '축제 주변 관광지',
]

const messages = ref([
  {
    role: 'bot',
    text: '서울 축제 도우미입니다. 찾고 싶은 주제를 눌러보세요.',
  },
])

const toggleChat = () => {
  isOpen.value = !isOpen.value
}

const askSuggestion = (q) => {
  messages.value.push({ role: 'user', text: q })
  messages.value.push({
    role: 'bot',
    text: '지금은 UI 미리보기 상태예요. 실제 답변은 API 연결 후 제공됩니다.',
  })
}
</script>

<template>
  <div class="chatbot-wrap">
    <section v-if="isOpen" class="chat-panel section-card" aria-label="서울 축제 도우미">
      <header class="panel-head">
        <div class="bot-meta">
          <div class="bot-avatar" aria-hidden="true">🙂</div>
          <div>
            <p class="name">서울 축제 도우미</p>
            <p class="sub">무엇을 찾고 있나요?</p>
          </div>
        </div>
        <button type="button" class="close-btn" @click="toggleChat">닫기</button>
      </header>

      <div class="messages">
        <p
          v-for="(msg, index) in messages"
          :key="index"
          class="msg"
          :class="msg.role"
        >
          {{ msg.text }}
        </p>
      </div>

      <div class="quick-qs">
        <button
          v-for="item in suggestions"
          :key="item"
          type="button"
          class="q-chip"
          @click="askSuggestion(item)"
        >
          {{ item }}
        </button>
      </div>
    </section>

    <button
      v-if="!isOpen"
      type="button"
      class="chat-fab"
      aria-label="서울 축제 도우미 열기"
      @click="toggleChat"
    >
      <span class="fab-emoji" aria-hidden="true">🙂</span>
      <span class="fab-text">
        <strong>서울 축제 도우미</strong>
        <small>무엇을 찾고 있나요?</small>
      </span>
    </button>
  </div>
</template>

<style scoped>
.chatbot-wrap {
  position: fixed;
  right: 20px;
  bottom: 18px;
  z-index: 1200;
}

.chat-fab {
  border: 1px solid #dce8d5;
  background: #ffffff;
  border-radius: 999px;
  padding: 8px 12px;
  min-height: 58px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 24px rgba(31, 61, 50, 0.12);
  cursor: pointer;
}

.fab-emoji {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #e9f8e5;
  font-size: 22px;
}

.fab-text {
  display: grid;
  text-align: left;
  color: #284b3e;
  line-height: 1.2;
}

.fab-text strong {
  font-size: 14px;
}

.fab-text small {
  font-size: 12px;
  color: #5d786d;
}

.chat-panel {
  width: 340px;
  max-height: 520px;
  padding: 14px;
  display: grid;
  gap: 12px;
  border-radius: 18px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bot-meta {
  display: flex;
  gap: 10px;
  align-items: center;
}

.bot-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #e9f8e5;
}

.name {
  margin: 0;
  font-weight: 800;
  color: #1f3d32;
}

.sub {
  margin: 2px 0 0;
  color: #648176;
  font-size: 12px;
}

.close-btn {
  border: 1px solid var(--color-border);
  border-radius: 999px;
  background: #fff;
  padding: 6px 10px;
  cursor: pointer;
}

.messages {
  min-height: 120px;
  max-height: 220px;
  overflow: auto;
  border: 1px solid #e7eee2;
  border-radius: 14px;
  background: #fbfef8;
  padding: 10px;
  display: grid;
  gap: 8px;
}

.msg {
  margin: 0;
  max-width: 90%;
  padding: 8px 10px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.35;
}

.msg.bot {
  background: #eef9e7;
  color: #28503f;
}

.msg.user {
  margin-left: auto;
  background: #eaf3ff;
  color: #24425f;
}

.quick-qs {
  display: grid;
  gap: 8px;
}

.q-chip {
  border: 1px solid var(--color-border);
  background: #fff;
  border-radius: 999px;
  padding: 8px 12px;
  text-align: left;
  font-weight: 700;
  color: #2f5447;
  cursor: pointer;
}

.q-chip:hover {
  border-color: #b8d8af;
  background: #f7fdf3;
}

@media (max-width: 768px) {
  .chatbot-wrap {
    right: 12px;
    bottom: 12px;
  }

  .chat-panel {
    width: min(92vw, 340px);
  }

  .chat-fab {
    width: 56px;
    height: 56px;
    padding: 0;
    justify-content: center;
    border-radius: 50%;
  }

  .fab-text {
    display: none;
  }

  .fab-emoji {
    width: 42px;
    height: 42px;
  }
}
</style>
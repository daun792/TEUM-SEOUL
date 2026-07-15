<script setup>
import { nextTick, ref } from 'vue'
import mascotImage from '../../assets/chatbot-mascot.webp'
import { sendChatMessage } from '../../services/chatApi'

const isOpen = ref(false)
const isLoading = ref(false)
const inputMessage = ref('')
const messagesContainer = ref(null)
const suggestions = ['이번 주말 축제', '무료 축제', '아이와 갈 만한 곳', '축제 주변 관광지']
const messages = ref([{ role: 'bot', text: '안녕하세요. 서울 축제 도우미예요.' }])

const scrollToLatest = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const submitMessage = async (presetMessage) => {
  const question = (presetMessage || inputMessage.value).trim()
  if (!question || isLoading.value) return

  messages.value.push({ role: 'user', text: question })
  inputMessage.value = ''
  isLoading.value = true
  await scrollToLatest()

  try {
    const answer = await sendChatMessage(question)
    messages.value.push({ role: 'bot', text: answer })
  } catch (error) {
    messages.value.push({
      role: 'bot',
      text: error instanceof Error ? error.message : '챗봇 서버에 연결하지 못했습니다.',
    })
  } finally {
    isLoading.value = false
    await scrollToLatest()
  }
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

      <div ref="messagesContainer" class="messages" aria-live="polite">
        <p v-for="(message, index) in messages" :key="index" :class="message.role">
          {{ message.text }}
        </p>
        <p v-if="isLoading" class="bot loading-message">답변을 찾고 있어요…</p>
      </div>

      <div class="suggestions">
        <button
          v-for="item in suggestions"
          :key="item"
          type="button"
          :disabled="isLoading"
          @click="submitMessage(item)"
        >
          {{ item }}
        </button>
      </div>

      <form class="chat-input" @submit.prevent="submitMessage()">
        <input
          v-model="inputMessage"
          type="text"
          maxlength="300"
          placeholder="서울 관광 정보를 물어보세요"
          aria-label="챗봇 질문"
          :disabled="isLoading"
        />
        <button type="submit" :disabled="isLoading || !inputMessage.trim()">전송</button>
      </form>
    </section>

    <button v-else type="button" class="chat-fab" aria-label="챗봇 열기" @click="isOpen = true">
      <img :src="mascotImage" alt="" class="fab-avatar" aria-hidden="true" />
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
  object-fit: cover;
}

.fab-avatar {
  width: 54px;
  height: 54px;
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
  width: min(380px, calc(100vw - 28px));
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
  min-height: 150px;
  max-height: 300px;
  display: grid;
  align-content: start;
  gap: 8px;
  margin-top: 12px;
  padding: 10px;
  overflow-y: auto;
  border-radius: 14px;
  background: #f7faf3;
}

.messages p {
  width: fit-content;
  max-width: 88%;
  margin: 0;
  padding: 8px 10px;
  border-radius: 12px;
  font-size: 12px;
  line-height: 1.55;
  white-space: pre-line;
}

.messages .bot {
  background: #eaf5e1;
}

.messages .user {
  justify-self: end;
  background: #e8f2fb;
}

.loading-message {
  opacity: 0.72;
}

.suggestions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
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

.suggestions button:disabled,
.chat-input button:disabled,
.chat-input input:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.chat-input {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  margin-top: 10px;
}

.chat-input input {
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  background: #fff;
  color: #263a2f;
  font: inherit;
  font-size: 12px;
}

.chat-input button {
  padding: 0 15px;
  border: 0;
  border-radius: var(--radius-pill);
  background: var(--color-primary-dark);
  color: #fff;
  font-size: 12px;
  font-weight: 750;
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

  .suggestions {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup>
import { ref } from 'vue'

const open = ref(false)
const input = ref('')
const messages = ref([
  { role: 'bot', text: '안녕하세요. 틈서울 챗봇입니다. 축제나 주변 장소를 물어보세요.' },
])

const toggle = () => {
  open.value = !open.value
}

const send = () => {
  const text = input.value.trim()
  if (!text) return

  messages.value.push({ role: 'user', text })
  messages.value.push({
    role: 'bot',
    text: '더미 응답입니다. 백엔드 챗봇 API 연결 시 실제 답변으로 바뀝니다.',
  })
  input.value = ''
}
</script>

<template>
  <div class="chatbot">
    <button class="fab" type="button" @click="toggle">
      {{ open ? '닫기' : '챗봇' }}
    </button>

    <section v-if="open" class="panel">
      <h3>틈서울 챗봇</h3>

      <div class="messages">
        <p
          v-for="(msg, idx) in messages"
          :key="idx"
          :class="['msg', msg.role]"
        >
          <strong>{{ msg.role === 'bot' ? '챗봇' : '나' }}</strong>
          {{ msg.text }}
        </p>
      </div>

      <form class="input-row" @submit.prevent="send">
        <input
          v-model="input"
          type="text"
          placeholder="질문을 입력하세요"
        />
        <button type="submit">전송</button>
      </form>
    </section>
  </div>
</template>

<style scoped>
.chatbot {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}

.fab {
  width: 64px;
  height: 64px;
  border: none;
  border-radius: 999px;
  background: #0f766e;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
}

.panel {
  width: 320px;
  height: 420px;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 14px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
  padding: 12px;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.panel h3 {
  margin: 0;
}

.messages {
  flex: 1;
  overflow: auto;
  background: #f9fafb;
  border-radius: 10px;
  padding: 10px;
}

.msg {
  margin: 0 0 8px;
  font-size: 14px;
}

.msg.user {
  text-align: right;
}

.input-row {
  display: flex;
  gap: 8px;
}

.input-row input {
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 8px 10px;
}

.input-row button {
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  background: #0f766e;
  color: #fff;
  cursor: pointer;
}
</style>
<script setup>
import { nextTick, ref } from 'vue'
import api, { getErrorMessage } from '../../services/api'

const open = ref(false)
const input = ref('')
const loading = ref(false)
const messages = ref([
  { role: 'assistant', content: '공연명이나 지역, 남는 시간을 알려주시면 실제 서울 데이터에서 찾아드릴게요.' },
])
const bodyRef = ref(null)

async function send() {
  const text = input.value.trim()
  if (!text || loading.value) return
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/api/chat', {
      message: text,
      history: messages.value.slice(-10),
    })
    messages.value.push({ role: 'assistant', content: data.answer, source: data.source })
  } catch (error) {
    messages.value.push({ role: 'assistant', content: getErrorMessage(error, '챗봇 응답을 받지 못했습니다.') })
  } finally {
    loading.value = false
    await nextTick()
    bodyRef.value?.scrollTo({ top: bodyRef.value.scrollHeight, behavior: 'smooth' })
  }
}
</script>

<template>
  <button v-if="!open" class="chat-fab" type="button" aria-label="챗봇 열기" @click="open = true">틈봇</button>
  <aside v-else class="chat-panel" aria-label="틈서울 챗봇">
    <header>
      <div><strong>틈봇</strong><small>서울 공공데이터 기반</small></div>
      <button type="button" aria-label="챗봇 닫기" @click="open = false">×</button>
    </header>
    <div ref="bodyRef" class="chat-body">
      <div v-for="(message, index) in messages" :key="index" :class="['chat-message', message.role]">
        <p>{{ message.content }}</p>
        <small v-if="message.source === 'fallback'">검색 결과 기반 기본 응답</small>
      </div>
      <div v-if="loading" class="chat-message assistant"><p>실제 데이터를 찾고 있습니다…</p></div>
    </div>
    <form class="chat-form" @submit.prevent="send">
      <input v-model="input" placeholder="예: 대학로 공연 후 1시간" aria-label="챗봇 메시지" />
      <button type="submit">전송</button>
    </form>
  </aside>
</template>

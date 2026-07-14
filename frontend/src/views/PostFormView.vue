<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api, { getErrorMessage } from '../services/api'

const route = useRoute()
const router = useRouter()
const editing = computed(() => Boolean(route.params.id))
const loading = ref(false)
const error = ref('')
const form = reactive({
  title: '', content: '', category: route.query.category || '공연 후 코스', password: '',
  performance_name: route.query.performance || '', available_minutes: route.query.minutes ? Number(route.query.minutes) : null,
})

onMounted(async () => {
  if (!editing.value) {
    if (route.query.places) form.content = `추천 코스: ${route.query.places}\n\n직접 방문한 후기를 작성해 주세요.`
    return
  }
  try {
    const { data } = await api.get(`/api/posts/${route.params.id}`)
    Object.assign(form, { title: data.title, content: data.content, category: data.category, performance_name: data.performance_name, available_minutes: data.available_minutes })
  } catch (e) { error.value = getErrorMessage(e) }
})

async function submit() {
  loading.value = true
  error.value = ''
  try {
    const payload = { ...form, available_minutes: form.available_minutes ? Number(form.available_minutes) : null }
    const { data } = editing.value
      ? await api.put(`/api/posts/${route.params.id}`, payload)
      : await api.post('/api/posts', payload)
    router.push(`/posts/${data.id}`)
  } catch (e) { error.value = getErrorMessage(e) }
  finally { loading.value = false }
}
</script>

<template>
  <main class="page-shell narrow-page">
    <header class="page-header"><span class="eyebrow">WRITE A GAP</span><h1>{{ editing ? '후기 수정' : '틈 공유하기' }}</h1><p>개인정보 없이 익명으로 작성됩니다. 비밀번호는 수정과 삭제에 사용합니다.</p></header>
    <form class="post-form" @submit.prevent="submit">
      <label class="field"><span>카테고리</span><select v-model="form.category"><option>공연 전 코스</option><option>공연 후 코스</option><option>장소 후기</option><option>자유</option></select></label>
      <label class="field"><span>제목</span><input v-model.trim="form.title" maxlength="200" required /></label>
      <div class="two-columns"><label class="field"><span>공연명</span><input v-model.trim="form.performance_name" maxlength="255" /></label><label class="field"><span>남았던 시간</span><div class="input-suffix"><input v-model="form.available_minutes" type="number" min="30" max="180" /><span>분</span></div></label></div>
      <label class="field"><span>후기 내용</span><textarea v-model.trim="form.content" rows="10" maxlength="10000" required></textarea></label>
      <label class="field"><span>수정·삭제 비밀번호</span><input v-model="form.password" type="password" required /><small>교육용 요구사항에 따라 서버에서 평문 비교됩니다. 다른 서비스에서 쓰는 비밀번호는 사용하지 마세요.</small></label>
      <p v-if="error" class="form-error">{{ error }}</p>
      <div class="form-actions"><RouterLink class="secondary-button" to="/posts">취소</RouterLink><button class="primary-button" :disabled="loading" type="submit">{{ loading ? '저장 중…' : '저장' }}</button></div>
    </form>
  </main>
</template>

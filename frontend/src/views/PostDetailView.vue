<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api, { getErrorMessage } from '../services/api'
import { useBookmarks } from '../composables/useBookmarks'
import { useClientId } from '../composables/useClientId'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const error = ref('')
const actionError = ref('')
const { toggle, isBookmarked } = useBookmarks()
const clientId = useClientId()
const bookmarked = computed(() => post.value && isBookmarked(post.value.id))

async function load() {
  try { post.value = (await api.get(`/api/posts/${route.params.id}`)).data }
  catch (e) { error.value = getErrorMessage(e) }
}
async function like() {
  try {
    const { data } = await api.post(`/api/posts/${post.value.id}/likes/toggle`, null, { headers: { 'X-Client-ID': clientId } })
    post.value.like_count = data.like_count
  } catch (e) { actionError.value = getErrorMessage(e) }
}
async function remove() {
  const password = window.prompt('작성할 때 입력한 비밀번호를 입력하세요.')
  if (!password) return
  try {
    await api.delete(`/api/posts/${post.value.id}`, { data: { password } })
    router.push('/posts')
  } catch (e) { actionError.value = getErrorMessage(e) }
}
onMounted(load)
</script>

<template>
  <main class="page-shell narrow-page">
    <div v-if="error" class="error-state"><h1>글을 불러오지 못했습니다.</h1><p>{{ error }}</p></div>
    <article v-else-if="post" class="post-detail">
      <header><span class="category-pill">{{ post.category }}</span><h1>{{ post.title }}</h1><div class="post-meta"><span>{{ post.performance_name || '공연 정보 없음' }}</span><span v-if="post.available_minutes">{{ post.available_minutes }}분</span><span>조회 {{ post.view_count }}</span></div></header>
      <div class="post-body">{{ post.content }}</div>
      <div class="post-reactions">
        <button type="button" @click="like">♥ 좋아요 {{ post.like_count }}</button>
        <button type="button" :class="{ active: bookmarked }" @click="toggle(post.id)">{{ bookmarked ? '★ 북마크됨' : '☆ 북마크' }}</button>
      </div>
      <p v-if="actionError" class="form-error">{{ actionError }}</p>
      <footer><RouterLink :to="`/posts/${post.id}/edit`">수정</RouterLink><button type="button" @click="remove">삭제</button><RouterLink to="/posts">목록</RouterLink></footer>
    </article>
  </main>
</template>

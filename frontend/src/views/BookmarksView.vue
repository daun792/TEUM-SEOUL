<script setup>
import { onMounted, ref } from 'vue'
import api, { getErrorMessage } from '../services/api'
import { useBookmarks } from '../composables/useBookmarks'

const { ids, removeMissing } = useBookmarks()
const posts = ref([])
const error = ref('')

onMounted(async () => {
  if (!ids.value.length) return
  try {
    const { data } = await api.get('/api/posts', { params: { ids: ids.value.join(','), size: 100 } })
    posts.value = data.items
    removeMissing(posts.value.map((post) => post.id))
  } catch (e) { error.value = getErrorMessage(e) }
})
</script>

<template>
  <main class="page-shell">
    <header class="page-header"><span class="eyebrow">BOOKMARKS</span><h1>내가 저장한 틈</h1><p>북마크는 현재 브라우저에만 저장되며 다른 기기와 동기화되지 않습니다.</p></header>
    <p v-if="error" class="form-error">{{ error }}</p>
    <div v-else-if="posts.length" class="post-grid"><RouterLink v-for="post in posts" :key="post.id" :to="`/posts/${post.id}`" class="post-card"><span class="category-pill">{{ post.category }}</span><h2>{{ post.title }}</h2><p>{{ post.content }}</p><div><span>{{ post.performance_name }}</span><span>좋아요 {{ post.like_count }}</span></div></RouterLink></div>
    <div v-else class="empty-card large">아직 북마크한 글이 없습니다.</div>
  </main>
</template>

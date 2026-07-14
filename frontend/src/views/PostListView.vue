<script setup>
import { onMounted, reactive, ref } from 'vue'
import api, { getErrorMessage } from '../services/api'

const posts = ref([])
const total = ref(0)
const loading = ref(false)
const error = ref('')
const filters = reactive({ q: '', category: '' })

async function load() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/posts', { params: filters })
    posts.value = data.items
    total.value = data.total
  } catch (e) {
    error.value = getErrorMessage(e)
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>

<template>
  <main class="page-shell">
    <header class="page-header inline-header"><div><span class="eyebrow">COMMUNITY</span><h1>다른 사람의 틈</h1><p>공연 전후 실제로 방문한 짧은 코스를 익명으로 공유합니다.</p></div><RouterLink class="primary-button" to="/posts/new">후기 작성</RouterLink></header>
    <form class="filter-bar" @submit.prevent="load">
      <input v-model="filters.q" name="q" type="search" placeholder="공연명, 장소, 후기 검색" />
      <select v-model="filters.category" name="category">
        <option value="">전체 카테고리</option><option>공연 전 코스</option><option>공연 후 코스</option><option>장소 후기</option><option>자유</option>
      </select>
      <button type="submit">검색</button>
    </form>
    <p class="list-count">총 {{ total }}개의 글</p>
    <div v-if="loading" class="loading-inline">글을 불러오는 중입니다.</div>
    <div v-else-if="error" class="form-error">{{ error }}</div>
    <div v-else-if="posts.length" class="post-grid">
      <RouterLink v-for="post in posts" :key="post.id" :to="`/posts/${post.id}`" class="post-card">
        <span class="category-pill">{{ post.category }}</span>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <div><span>{{ post.performance_name || '공연 정보 없음' }}</span><span>조회 {{ post.view_count }} · 좋아요 {{ post.like_count }}</span></div>
      </RouterLink>
    </div>
    <div v-else class="empty-card large">검색 조건에 맞는 글이 없습니다.</div>
  </main>
</template>

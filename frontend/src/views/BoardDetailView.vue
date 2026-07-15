<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { posts } from '../mocks/posts'

const route = useRoute()
const router = useRouter()

const post = computed(() =>
  posts.find((item) => item.id === String(route.params.id))
)

const goList = () => router.push('/board')
const goEdit = () => router.push('/board/edit/' + route.params.id)
const removePost = () => {
  alert('더미 화면입니다. 삭제 API 연결 시 실제 삭제됩니다.')
}
</script>

<template>
  <main v-if="post" class="container detail-page">
    <section class="section-card detail-card">
      <h2>{{ post.title }}</h2>
      <p class="meta">{{ post.author }} | {{ post.createdAt }}</p>
      <div class="content">{{ post.content }}</div>

      <div class="actions">
        <button type="button" class="ghost" @click="goList">목록</button>
        <button type="button" class="edit" @click="goEdit">수정</button>
        <button type="button" class="danger" @click="removePost">삭제</button>
      </div>
    </section>
  </main>

  <main v-else class="container detail-page">
    <section class="section-card detail-card missing">
      <h2>게시글을 찾을 수 없습니다.</h2>
      <button type="button" class="ghost" @click="goList">목록으로</button>
    </section>
  </main>
</template>

<style scoped>
.detail-page {
  padding: 24px 0 40px;
}

.detail-card {
  padding: 20px;
}

h2 {
  margin: 0;
  color: #223b30;
  font-size: 28px;
  letter-spacing: -0.03em;
}

.meta {
  color: #6f8178;
  margin: 8px 0 16px;
}

.content {
  min-height: 200px;
  border: 1px solid #e2e8de;
  border-radius: 14px;
  background: #fcfef9;
  padding: 16px;
  margin-bottom: 16px;
  line-height: 1.6;
  color: #2f443a;
}

.actions {
  display: flex;
  gap: 8px;
}

.actions button {
  border: 0;
  border-radius: var(--radius-pill);
  padding: 9px 14px;
  font-weight: 800;
  cursor: pointer;
}

.ghost {
  background: #eef2eb;
  color: #42584d;
}

.edit {
  background: #e8f5dc;
  color: var(--color-primary-dark);
}

.danger {
  background: #f25752;
  color: #fff;
}

.missing {
  display: grid;
  gap: 14px;
  justify-items: start;
}

@media (max-width: 760px) {
  .detail-page {
    padding-top: 18px;
  }

  h2 {
    font-size: 24px;
  }
}
</style>
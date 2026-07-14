<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const posts = [
  { id: '1', title: '여름 음악축제 사람 많나요?', content: '다녀오신 분 후기 부탁해요.', author: '익명', createdAt: '2026-07-14' },
  { id: '2', title: '한강 축제 근처 주차 팁 공유', content: '여의도 공영주차장 정보 공유합니다.', author: '익명', createdAt: '2026-07-14' },
  { id: '3', title: '인사동 축제 체험 후기', content: '전통 공예 체험이 특히 좋았어요.', author: '익명', createdAt: '2026-07-13' },
]

const post = computed(() => posts.find((item) => item.id === String(route.params.id)))

const goList = () => router.push('/board')
const goEdit = () => router.push('/board/edit/' + route.params.id)
const removePost = () => {
  alert('더미 화면입니다. 삭제 API 연결 시 실제 삭제됩니다.')
}
</script>

<template>
  <section v-if="post" class="detail">
    <h2>{{ post.title }}</h2>
    <p class="meta">{{ post.author }} | {{ post.createdAt }}</p>
    <div class="content">{{ post.content }}</div>

    <div class="actions">
      <button type="button" @click="goList">목록</button>
      <button type="button" @click="goEdit">수정</button>
      <button type="button" class="danger" @click="removePost">삭제</button>
    </div>
  </section>

  <section v-else>
    <h2>게시글을 찾을 수 없습니다.</h2>
    <button type="button" @click="goList">목록으로</button>
  </section>
</template>

<style scoped>
.detail {
  max-width: 900px;
}
.meta {
  color: #6b7280;
  margin: 6px 0 16px;
}
.content {
  min-height: 160px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 16px;
}
.actions {
  display: flex;
  gap: 8px;
}
.danger {
  background: #dc2626;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
}
</style>
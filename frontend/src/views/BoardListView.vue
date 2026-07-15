<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getPostList } from '../mocks/posts'

const router = useRouter()
const posts = ref([])

onMounted(async () => {
  posts.value = await getPostList()
})

const goDetail = (id) => {
  router.push('/board/' + id)
}

const goWrite = () => {
  router.push('/board/write')
}
</script>

<template>
  <main class="container board-page">
    <header class="board-header">
      <h2>익명 게시판</h2>
      <button type="button" class="write-btn" @click="goWrite">글쓰기</button>
    </header>

    <ul class="post-list section-card">
      <li
        v-for="post in posts"
        :key="post.id"
        class="post-item"
        @click="goDetail(post.id)"
      >
        <span class="avatar" aria-hidden="true">익명</span>
        <div class="post-main">
          <h3>{{ post.title }}</h3>
          <p>{{ post.author }} | {{ post.createdAt }}</p>
        </div>
      </li>
    </ul>
  </main>
</template>

<style scoped>
.board-page {
  padding: 24px 0 40px;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

h2 {
  margin: 0;
  color: #223b30;
  font-size: 28px;
  letter-spacing: -0.03em;
}

.write-btn {
  border: 0;
  border-radius: var(--radius-pill);
  background: var(--color-primary);
  color: #fff;
  font-weight: 800;
  padding: 9px 14px;
  cursor: pointer;
}

.post-list {
  list-style: none;
  padding: 8px;
  margin: 0;
}

.post-item {
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  border-radius: 14px;
  padding: 10px;
  cursor: pointer;
}

.post-item + .post-item {
  margin-top: 8px;
}

.post-item:hover {
  background: #fbfdf8;
}

.avatar {
  width: 52px;
  height: 52px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  border: 1.5px dashed #bfd1b7;
  background: #f5fbef;
  color: #6f7f74;
  font-size: 11px;
  font-weight: 900;
}

.post-main {
  min-width: 0;
}

.post-item h3 {
  margin: 0 0 6px;
  color: #2d4439;
  font-size: 16px;
  line-height: 1.35;
}

.post-item p {
  margin: 0;
  color: #75867d;
  font-size: 13px;
}

@media (max-width: 760px) {
  .board-page {
    padding-top: 18px;
  }

  h2 {
    font-size: 24px;
  }

  .post-item {
    grid-template-columns: 44px minmax(0, 1fr);
    gap: 10px;
  }

  .avatar {
    width: 42px;
    height: 42px;
  }
}
</style>
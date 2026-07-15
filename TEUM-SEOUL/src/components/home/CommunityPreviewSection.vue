<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const previewPosts = [
  {
    id: '101',
    title: '이번 주말 여의도 축제 사람 많을까요?',
    timeAgo: '12분 전',
    commentCount: 8,
    avatar: '🐻',
  },
  {
    id: '102',
    title: '성수 근처 무료 전시 추천해요!',
    timeAgo: '1시간 전',
    commentCount: 3,
    avatar: '🐸',
  },
  {
    id: '103',
    title: '아이와 함께 가기 좋은 체험 축제 있을까요?',
    timeAgo: '2시간 전',
    commentCount: 5,
    avatar: '🐰',
  },
]

const goDetail = (id) => {
  router.push(`/board/${id}`)
}
</script>

<template>
  <section class="container board-preview section-card">
    <div class="section-head">
      <h3>틈서울 익명 게시판</h3>
      <RouterLink to="/board" class="more-link">더보기</RouterLink>
    </div>

    <ul class="post-list">
      <li
        v-for="post in previewPosts"
        :key="post.id"
        class="post-item"
        @click="goDetail(post.id)"
      >
        <div class="avatar" aria-hidden="true">{{ post.avatar }}</div>
        <div class="post-main">
          <p class="title">{{ post.title }}</p>
          <p class="meta">{{ post.timeAgo }} · 댓글 {{ post.commentCount }}</p>
        </div>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.board-preview {
  padding: 18px;
  display: grid;
  gap: 12px;
}

.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-head h3 {
  margin: 0;
  font-size: 24px;
  color: #25453a;
}

.more-link {
  font-weight: 700;
  color: var(--color-primary-dark);
}

.post-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.post-item {
  display: grid;
  grid-template-columns: 42px 1fr;
  gap: 10px;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 10px;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.post-item:hover {
  border-color: #bcdcb4;
  transform: translateY(-1px);
}

.post-item:focus-within {
  outline: 2px solid var(--color-sky);
  outline-offset: 2px;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #f4faef;
  font-size: 22px;
}

.post-main {
  min-width: 0;
}

.title {
  margin: 0;
  color: #26473b;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta {
  margin: 4px 0 0;
  color: #688379;
  font-size: 13px;
}
</style>
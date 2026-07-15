<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getPostList } from '../../services/postsApi'

const router = useRouter()
const previewPosts = ref([])

onMounted(async () => {
  try {
    const result = await getPostList({ page: 1, size: 3 })
    previewPosts.value = result.items.map((item, index) => ({
      id: item.id,
      title: item.title,
      timeAgo: item.createdAt,
      comments: 0,
      avatar: String.fromCharCode(65 + index),
    }))
  } catch {
    previewPosts.value = []
  }
})
</script>

<template>
  <section class="community-section section-card">
    <header class="section-head">
      <h2>틈서울 익명 게시판</h2>
      <RouterLink to="/board">더보기 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <ul class="post-list">
      <li v-for="post in previewPosts" :key="post.id">
        <button type="button" class="post-button" @click="router.push(`/board/${post.id}`)">
          <span class="avatar-placeholder" aria-hidden="true">{{ post.avatar }}</span>
          <span class="post-copy">
            <strong>{{ post.title }}</strong>
            <small>{{ post.timeAgo }}　○ {{ post.comments }}</small>
          </span>
        </button>
      </li>
      <li v-if="!previewPosts.length" class="empty-item">아직 등록된 게시글이 없습니다.</li>
    </ul>
  </section>
</template>

<style scoped>
.community-section {
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 18px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

h2 {
  margin: 0;
  color: #24372e;
  font-size: 20px;
  letter-spacing: -0.035em;
}

.section-head a {
  color: #6b756f;
  font-size: 12px;
  font-weight: 750;
}

.post-list {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid #e3e5de;
  border-radius: 14px;
  overflow: hidden;
}

.post-list li + li {
  border-top: 1px solid #ecece6;
}

.empty-item {
  padding: 16px 12px;
  color: #788780;
  font-size: 12px;
  font-weight: 700;
}

.post-button {
  width: 100%;
  min-height: 84px;
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  align-items: center;
  gap: 10px;
  padding: 12px 10px;
  border: 0;
  background: #fff;
  text-align: left;
  cursor: pointer;
}

.post-button:hover {
  background: #fbfcf8;
}

.avatar-placeholder {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border: 1.5px dashed #b9c9b2;
  border-radius: 50%;
  background: #f5f9f0;
  color: #7b8a75;
  font-size: 10px;
  font-weight: 900;
}

.post-copy {
  min-width: 0;
  display: grid;
  gap: 5px;
}

.post-copy strong {
  overflow: hidden;
  color: #34463d;
  font-size: 12px;
  line-height: 1.45;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-copy small {
  color: #8a928d;
  font-size: 10px;
}

</style>

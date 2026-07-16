<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPostList } from '../services/postsApi'

const router = useRouter()
const route = useRoute()
const posts = ref([])
const loading = ref(true)
const errorMessage = ref('')
const keyword = ref('')
const selectedCategory = ref('전체')
const page = ref(1)
const size = 10
const pages = ref(0)
const total = ref(0)
const categoryOptions = ['전체', '축제후기', '주변장소', '자유']

const loadPosts = async () => {
  try {
    loading.value = true
    const result = await getPostList({
      page: page.value,
      size,
      keyword: keyword.value,
      category: selectedCategory.value === '전체' ? undefined : selectedCategory.value,
      festivalId: typeof route.query.festival_id === 'string' ? route.query.festival_id : undefined,
    })
    posts.value = result.items
    pages.value = result.pages
    total.value = result.total
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '게시글을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(loadPosts)

const submitSearch = async () => {
  page.value = 1
  await loadPosts()
}

const movePage = async (nextPage) => {
  if (nextPage < 1 || (pages.value > 0 && nextPage > pages.value)) return
  page.value = nextPage
  await loadPosts()
}

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

    <form class="search-row" @submit.prevent="submitSearch">
      <select v-model="selectedCategory" aria-label="카테고리 필터">
        <option v-for="option in categoryOptions" :key="option" :value="option">{{ option }}</option>
      </select>
      <input v-model="keyword" type="text" placeholder="제목/내용 검색" />
      <button type="submit">검색</button>
    </form>

    <ul v-if="!loading && !errorMessage && posts.length" class="post-list section-card">
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

    <section v-else class="section-card state-box">
      {{ loading ? '게시글을 불러오는 중입니다...' : (errorMessage || '작성된 게시글이 없습니다.') }}
    </section>

    <nav v-if="!loading && pages > 1" class="pager" aria-label="게시글 페이지">
      <button type="button" :disabled="page <= 1" @click="movePage(page - 1)">이전</button>
      <span>{{ page }} / {{ pages }} (총 {{ total }}건)</span>
      <button type="button" :disabled="page >= pages" @click="movePage(page + 1)">다음</button>
    </nav>
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

.search-row {
  display: grid;
  grid-template-columns: 130px minmax(0, 1fr) auto;
  gap: 8px;
  margin-bottom: 12px;
}

.search-row select,
.search-row input {
  border: 1px solid #d9e2d5;
  border-radius: 10px;
  padding: 9px 10px;
  font-size: 13px;
}

.search-row button {
  border: 0;
  border-radius: 10px;
  padding: 0 12px;
  background: #deeeda;
  color: #395347;
  font-weight: 800;
  cursor: pointer;
}

.post-list {
  list-style: none;
  padding: 8px;
  margin: 0;
}

.state-box {
  min-height: 120px;
  display: grid;
  place-items: center;
  color: #60746a;
  font-weight: 700;
}

.pager {
  margin-top: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.pager button {
  border: 1px solid #d2ddd0;
  border-radius: 999px;
  padding: 7px 11px;
  background: #fff;
  color: #406053;
  font-weight: 800;
  cursor: pointer;
}

.pager span {
  color: #60756b;
  font-weight: 700;
  font-size: 13px;
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

  .search-row {
    grid-template-columns: 1fr;
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
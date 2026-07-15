<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { posts } from '../mocks/posts'

const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => Boolean(route.params.id))
const targetPost = computed(() =>
  posts.find((item) => item.id === String(route.params.id))
)

const form = ref({
  title: '',
  content: '',
})

onMounted(() => {
  if (isEditMode.value && targetPost.value) {
    form.value.title = targetPost.value.title
    form.value.content = targetPost.value.content
  }
})

const submitForm = () => {
  if (isEditMode.value) {
    alert('수정 완료(더미)')
  } else {
    alert('작성 완료(더미)')
  }
  router.push('/board')
}

const cancel = () => {
  router.push('/board')
}
</script>

<template>
  <main class="container write-page">
    <section class="section-card write-card">
      <h2>{{ isEditMode ? '게시글 수정' : '게시글 작성' }}</h2>

      <form class="form" @submit.prevent="submitForm">
        <label>
          제목
          <input v-model="form.title" type="text" placeholder="제목을 입력하세요" required />
        </label>

        <label>
          내용
          <textarea v-model="form.content" rows="10" placeholder="내용을 입력하세요" required />
        </label>

        <div class="actions">
          <button type="submit" class="submit">{{ isEditMode ? '수정하기' : '등록하기' }}</button>
          <button type="button" class="ghost" @click="cancel">취소</button>
        </div>
      </form>
    </section>
  </main>
</template>

<style scoped>
.write-page {
  padding: 24px 0 40px;
}

.write-card {
  padding: 20px;
}

h2 {
  margin: 0 0 16px;
  color: #223b30;
  font-size: 28px;
  letter-spacing: -0.03em;
}

.form {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 8px;
  font-weight: 800;
  color: #2c4438;
}

input,
textarea {
  width: 100%;
  border: 1px solid #dbe3d8;
  border-radius: 12px;
  background: #fcfef9;
  padding: 11px 12px;
  font-size: 14px;
}

input:focus,
textarea:focus {
  outline: 2px solid rgba(105, 182, 47, 0.22);
  border-color: var(--color-primary);
}

.actions {
  display: flex;
  gap: 8px;
}

button {
  border: none;
  border-radius: var(--radius-pill);
  padding: 9px 14px;
  font-weight: 800;
  cursor: pointer;
}

.submit {
  background: var(--color-primary);
  color: #fff;
}

.ghost {
  background: #eef2eb;
  color: #42584d;
}

@media (max-width: 760px) {
  .write-page {
    padding-top: 18px;
  }

  h2 {
    font-size: 24px;
  }
}
</style>
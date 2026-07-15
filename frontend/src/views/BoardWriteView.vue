<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createPost, getPostById, updatePost } from '../services/postsApi'

const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => Boolean(route.params.id))
const loading = ref(false)
const submitting = ref(false)
const errorMessage = ref('')

const form = ref({
  title: '',
  content: '',
  author: '익명',
  password: '',
})

onMounted(async () => {
  if (isEditMode.value) {
    loading.value = true
    errorMessage.value = ''
    try {
      const post = await getPostById(route.params.id)
      form.value.title = post.title
      form.value.content = post.content
      form.value.author = post.author
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : '게시글 정보를 불러오지 못했습니다.'
    } finally {
      loading.value = false
    }
  }
})

const submitForm = async () => {
  submitting.value = true
  errorMessage.value = ''

  try {
    if (isEditMode.value) {
      await updatePost(route.params.id, {
        title: form.value.title,
        content: form.value.content,
        password: form.value.password,
      })
      window.alert('수정이 완료되었습니다.')
    } else {
      await createPost({
        title: form.value.title,
        content: form.value.content,
        author: form.value.author || '익명',
        password: form.value.password,
      })
      window.alert('작성이 완료되었습니다.')
    }
    router.push('/board')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '저장에 실패했습니다.'
  } finally {
    submitting.value = false
  }
}

const cancel = () => {
  router.push('/board')
}
</script>

<template>
  <main class="container write-page">
    <section class="section-card write-card">
      <h2>{{ isEditMode ? '게시글 수정' : '게시글 작성' }}</h2>

      <p v-if="loading" class="state-text">게시글 정보를 불러오는 중입니다...</p>
      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <form class="form" @submit.prevent="submitForm">
        <label>
          제목
          <input v-model="form.title" type="text" placeholder="제목을 입력하세요" required />
        </label>

        <label v-if="!isEditMode">
          작성자
          <input v-model="form.author" type="text" placeholder="작성자 이름" maxlength="50" required />
        </label>

        <label>
          내용
          <textarea v-model="form.content" rows="10" placeholder="내용을 입력하세요" required />
        </label>

        <label>
          비밀번호
          <input
            v-model="form.password"
            type="password"
            placeholder="비밀번호 4자리 이상"
            minlength="4"
            required
          />
        </label>

        <div class="actions">
          <button type="submit" class="submit" :disabled="loading || submitting">
            {{ submitting ? '저장 중...' : (isEditMode ? '수정하기' : '등록하기') }}
          </button>
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

.state-text {
  margin: 0 0 10px;
  color: #5f7268;
  font-weight: 700;
}

.error-text {
  margin: 0 0 10px;
  color: #b23b3b;
  font-weight: 700;
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
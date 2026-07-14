<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => Boolean(route.params.id))

const form = ref({
  title: isEditMode.value ? '기존 글 제목 예시' : '',
  content: isEditMode.value ? '기존 글 내용 예시' : '',
})

const submitForm = () => {
  alert(isEditMode.value ? '수정 완료(더미)' : '작성 완료(더미)')
  router.push('/board')
}

const cancel = () => {
  router.push('/board')
}
</script>

<template>
  <section class="write">
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
        <button type="submit">{{ isEditMode ? '수정하기' : '등록하기' }}</button>
        <button type="button" class="ghost" @click="cancel">취소</button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.write {
  max-width: 900px;
}
.form {
  display: grid;
  gap: 14px;
}
label {
  display: grid;
  gap: 8px;
  font-weight: 600;
}
input,
textarea {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
}
.actions {
  display: flex;
  gap: 8px;
}
button {
  border: none;
  border-radius: 8px;
  padding: 10px 14px;
  cursor: pointer;
}
.ghost {
  background: #f3f4f6;
}
</style>
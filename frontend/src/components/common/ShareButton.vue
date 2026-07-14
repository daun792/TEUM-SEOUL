<script setup>
import { ref } from 'vue'
import { shareCourse } from '../../utils/share'

const props = defineProps({ course: { type: Object, required: true } })
const message = ref('')

async function share() {
  try {
    const result = await shareCourse(props.course)
    message.value = result === 'shared' ? '공유 창을 열었습니다.' : '공유 링크를 복사했습니다.'
  } catch (error) {
    if (error?.name !== 'AbortError') message.value = '공유하지 못했습니다.'
  }
}
</script>

<template>
  <div class="share-control">
    <button class="secondary-button" type="button" @click="share">코스 공유</button>
    <span v-if="message" role="status">{{ message }}</span>
  </div>
</template>

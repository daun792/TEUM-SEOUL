<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  performance: { type: Object, required: true },
})
const emit = defineEmits(['submit'])

const form = reactive({
  phase: 'before',
  availableMinutes: 90,
  preferredCategory: '상관없음',
})
const error = ref('')

function submit() {
  const minutes = Number(form.availableMinutes)
  if (!Number.isInteger(minutes) || minutes < 30 || minutes > 180) {
    error.value = '남는 시간은 30분에서 180분 사이로 입력해 주세요.'
    return
  }
  error.value = ''
  emit('submit', {
    performance_id: props.performance.id,
    phase: form.phase,
    available_minutes: minutes,
    preferred_category: form.preferredCategory,
  })
}
</script>

<template>
  <form class="condition-card" @submit.prevent="submit">
    <div class="selected-performance">
      <span class="eyebrow">선택한 공연</span>
      <strong>{{ performance.name }}</strong>
      <small>{{ performance.address || '주소 정보 없음' }}</small>
    </div>

    <fieldset>
      <legend>언제 시간이 남나요?</legend>
      <div class="segmented">
        <label><input v-model="form.phase" type="radio" name="phase" value="before" />공연 전</label>
        <label><input v-model="form.phase" type="radio" name="phase" value="after" />공연 후</label>
      </div>
    </fieldset>

    <label class="field">
      <span>남는 시간</span>
      <div class="input-suffix">
        <input v-model="form.availableMinutes" name="availableMinutes" type="number" min="30" max="180" step="10" />
        <span>분</span>
      </div>
      <small>30분부터 최대 3시간까지 입력할 수 있습니다.</small>
    </label>

    <label class="field">
      <span>선호 카테고리</span>
      <select v-model="form.preferredCategory" name="preferredCategory">
        <option>상관없음</option>
        <option>문화시설</option>
        <option>관광지</option>
        <option>쇼핑</option>
        <option>레포츠</option>
      </select>
    </label>

    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <button class="primary-button" type="submit">이 틈에 갈 곳 찾기</button>
  </form>
</template>

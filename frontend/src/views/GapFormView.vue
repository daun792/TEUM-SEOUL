<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PerformanceSearch from '../components/course/PerformanceSearch.vue'
import GapConditionForm from '../components/course/GapConditionForm.vue'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const selected = ref(null)

onMounted(async () => {
  if (route.query.performanceId) {
    try {
      const { data } = await api.get('/api/performances', { params: { limit: 50 } })
      selected.value = data.items.find((item) => item.id === Number(route.query.performanceId)) || null
    } catch {
      selected.value = null
    }
  }
})

function submit(payload) {
  router.push({
    path: '/course/result',
    query: {
      performanceId: payload.performance_id,
      phase: payload.phase,
      minutes: payload.available_minutes,
      category: payload.preferred_category,
    },
  })
}
</script>

<template>
  <main class="page-shell narrow-page">
    <header class="page-header">
      <span class="eyebrow">FILL THE GAP</span>
      <h1>어떤 틈을 채울까요?</h1>
      <p>공연을 선택한 뒤 남는 시간을 알려주세요. 지도 없이도 시간 안에 들어오는 실제 장소를 계산합니다.</p>
    </header>
    <PerformanceSearch v-if="!selected" @select="selected = $event" />
    <div v-else>
      <button class="back-selection" type="button" @click="selected = null">← 공연 다시 선택</button>
      <GapConditionForm :performance="selected" @submit="submit" />
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CourseTimeline from '../components/course/CourseTimeline.vue'
import ShareButton from '../components/common/ShareButton.vue'
import api, { getErrorMessage } from '../services/api'

const props = defineProps({ shared: { type: Boolean, default: false } })
const route = useRoute()
const router = useRouter()
const course = ref(null)
const loading = ref(true)
const error = ref('')

const request = computed(() => ({
  performance_id: Number(route.query.performanceId),
  phase: route.query.phase,
  available_minutes: Number(route.query.minutes),
  preferred_category: route.query.category || '상관없음',
}))

async function load() {
  loading.value = true
  error.value = ''
  try {
    if (props.shared) {
      const { data } = await api.get('/api/courses/shared', {
        params: {
          performance_id: request.value.performance_id,
          phase: request.value.phase,
          minutes: request.value.available_minutes,
          category: request.value.preferred_category,
          place_ids: route.query.placeIds,
        },
      })
      course.value = data
    } else {
      const { data } = await api.post('/api/courses/recommend', request.value)
      course.value = data
    }
  } catch (e) {
    error.value = getErrorMessage(e, '코스를 생성하지 못했습니다.')
  } finally {
    loading.value = false
  }
}

function writeReview() {
  router.push({
    path: '/posts/new',
    query: {
      performance: course.value.performance.name,
      minutes: course.value.available_minutes,
      category: course.value.phase === 'before' ? '공연 전 코스' : '공연 후 코스',
      places: course.value.places.map((place) => place.name).join(', '),
    },
  })
}

onMounted(load)
watch(() => route.fullPath, load)
</script>

<template>
  <main class="page-shell result-page">
    <div v-if="loading" class="loading-state"><span></span><p>남는 시간 안에 들어오는 장소를 계산하고 있습니다.</p></div>
    <div v-else-if="error" class="error-state"><h1>코스를 만들지 못했습니다.</h1><p>{{ error }}</p><RouterLink class="primary-button" to="/gap">조건 다시 선택</RouterLink></div>
    <template v-else-if="course">
      <header class="result-header">
        <div><span class="eyebrow">YOUR SEOUL GAP</span><h1>{{ course.available_minutes }}분의 틈을<br />이렇게 채워보세요.</h1><p>{{ course.performance.name }} · {{ course.phase === 'before' ? '공연 전' : '공연 후' }}</p></div>
        <div class="result-actions"><ShareButton :course="course" /><button class="primary-button" type="button" @click="writeReview">후기 쓰기</button></div>
      </header>
      <CourseTimeline :course="course" />
      <div class="bottom-actions"><RouterLink class="secondary-button" to="/gap">다른 조건으로 다시 찾기</RouterLink></div>
    </template>
  </main>
</template>

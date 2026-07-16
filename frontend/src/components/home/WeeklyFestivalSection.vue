<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import FestivalCard from '../festival/FestivalCard.vue'
import { getFestivalPage } from '../../services/festivalsApi.js'
import { useFestivalQuery } from '../../composables/useFestivalQuery.js'
import { addDaysIso, todayIso } from '../../utils/dateRange.js'
import { getFestivalStatus, getFestivalTags } from '../../utils/festivalTags.js'

const props = defineProps({
  selectedCategory: {
    type: String,
    default: '전체',
  },
})

const festivalQuery = useFestivalQuery(
  (params, options) => getFestivalPage(params, options),
  { initialData: { items: [], total: 0, page: 1, size: 18, pages: 0 } },
)

const weeklyFestivals = computed(() => (festivalQuery.data.value?.items || []).map((festival) => ({
  id: festival.id,
  title: festival.title,
  date: festival.period,
  place: festival.place,
  imageUrl: festival.imageUrl,
  status: getFestivalStatus(festival),
  priceType: /무료/.test(festival.title) ? '무료' : '정보 없음',
  tags: getFestivalTags(festival),
})))

const filteredFestivals = computed(() => weeklyFestivals.value
  .filter((festival) => festival.tags.includes(props.selectedCategory)))

function loadUpcomingFestivals(options = {}) {
  const startDate = todayIso()
  const endDate = addDaysIso(startDate, 90)
  return festivalQuery.run({
    startDate,
    endDate,
    page: 1,
    size: 18,
  }, options)
}

onMounted(() => loadUpcomingFestivals())
</script>

<template>
  <section class="weekly section-card" :aria-busy="festivalQuery.loading.value">
    <header class="section-head">
      <div>
        <h2>진행 중·예정 행사</h2>
        <p>오늘부터 90일 안의 서울 문화행사</p>
      </div>
      <RouterLink to="/festivals">더보기 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <div v-if="festivalQuery.waking.value" class="inline-state" aria-live="polite">
      서버를 깨우는 중입니다. 잠시만 기다려 주세요.
    </div>
    <div v-else-if="festivalQuery.loading.value && !weeklyFestivals.length" class="inline-state" aria-live="polite">
      가까운 행사를 불러오는 중입니다.
    </div>
    <div v-else-if="festivalQuery.error.value" class="inline-state error-state" aria-live="assertive">
      <span>{{ festivalQuery.error.value }}</span>
      <button type="button" @click="festivalQuery.retry">다시 시도</button>
    </div>

    <div v-else-if="filteredFestivals.length" class="card-slider">
      <FestivalCard v-for="item in filteredFestivals" :key="item.id" :festival="item" />
    </div>

    <p v-else class="empty-state">선택한 카테고리에 맞는 진행 중·예정 행사가 없습니다.</p>
  </section>
</template>

<style scoped>
.weekly {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 18px;
}

.section-head {
  display: flex;
  align-items: flex-start;
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

.section-head p {
  margin: 4px 0 0;
  color: #75827b;
  font-size: 11px;
}

.section-head a {
  flex: none;
  color: #6b756f;
  font-size: 12px;
  font-weight: 750;
}

.card-slider {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 6px;
  scroll-snap-type: x proximity;
  scrollbar-width: thin;
}

.card-slider :deep(.festival-card) {
  flex: 0 0 clamp(220px, 22vw, 250px);
  scroll-snap-align: start;
}

.inline-state,
.empty-state {
  margin: 10px 0 2px;
  flex: 1;
  min-height: 110px;
  display: grid;
  place-items: center;
  border: 1px dashed #d6dfd1;
  border-radius: 14px;
  padding: 14px;
  background: #fbfdf8;
  color: #6a7b72;
  text-align: center;
  font-size: 13px;
  font-weight: 700;
}

.error-state {
  gap: 10px;
  border-color: #e7c8c2;
  background: #fff9f7;
}

.error-state button {
  border: 1px solid #cfdbca;
  border-radius: 9px;
  padding: 7px 11px;
  background: #fff;
  color: #365a3f;
  cursor: pointer;
  font-weight: 750;
}

@media (max-width: 760px) {
  .card-slider {
    gap: 8px;
  }

  .card-slider :deep(.festival-card) {
    flex-basis: 230px;
  }
}
</style>

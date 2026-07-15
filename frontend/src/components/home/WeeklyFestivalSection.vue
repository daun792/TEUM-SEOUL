<script setup>
import { computed } from 'vue'
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import FestivalCard from '../festival/FestivalCard.vue'
import { getFestivalList } from '../../services/festivalsApi'
import { getFestivalStatus, getFestivalTags } from '../../utils/festivalTags'

const props = defineProps({
  selectedCategory: {
    type: String,
    default: '오늘',
  },
})

const weeklyFestivals = ref([])

onMounted(async () => {
  try {
    const festivals = await getFestivalList({ page: 1, size: 18 })
    weeklyFestivals.value = festivals.map((festival) => ({
      id: festival.id,
      title: festival.title,
      date: festival.period,
      place: festival.place,
      imageUrl: festival.imageUrl,
      status: getFestivalStatus(festival),
      priceType: /무료/.test(festival.title) ? '무료' : '유료',
      tags: getFestivalTags(festival),
    }))
  } catch {
    weeklyFestivals.value = []
  }
})

const filteredFestivals = computed(() =>
  weeklyFestivals.value.filter((festival) => festival.tags.includes(props.selectedCategory)),
)
</script>

<template>
  <section class="weekly section-card">
    <header class="section-head">
      <h2>이번 주 추천 축제</h2>
      <RouterLink to="/festivals">더보기 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <div v-if="filteredFestivals.length" class="card-grid">
      <FestivalCard v-for="item in filteredFestivals" :key="item.id" :festival="item" />
    </div>

    <p v-else class="empty-state">선택한 카테고리에 맞는 추천 축제를 준비 중입니다.</p>
  </section>
</template>

<style scoped>
.weekly {
  height: 100%;
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

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.empty-state {
  margin: 10px 0 2px;
  min-height: 110px;
  display: grid;
  place-items: center;
  border: 1px dashed #d6dfd1;
  border-radius: 14px;
  background: #fbfdf8;
  color: #6a7b72;
  font-size: 13px;
  font-weight: 700;
}

@media (max-width: 760px) {
  .card-grid {
    display: flex;
    overflow-x: auto;
    padding-bottom: 5px;
    scrollbar-width: thin;
  }
}
</style>

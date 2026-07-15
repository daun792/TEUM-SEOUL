<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import FestivalCard from '../festival/FestivalCard.vue'

const props = defineProps({
  selectedCategory: {
    type: String,
    default: '오늘',
  },
})

const weeklyFestivals = [
  {
    id: '1',
    title: '한강 여름 음악축제',
    date: '7.12(금) - 7.14(일)',
    place: '여의도 한강공원',
    status: '진행중',
    priceType: '무료',
    tags: ['오늘', '이번 주말', '무료 축제', '공연', '야외 행사'],
  },
  {
    id: '2',
    title: '서울숲 피크닉 페스티벌',
    date: '7.13(토) - 7.15(월)',
    place: '서울숲 공원',
    status: '진행중',
    priceType: '무료',
    tags: ['오늘', '이번 주말', '무료 축제', '야외 행사'],
  },
  {
    id: '3',
    title: '북촌 한옥 야행',
    date: '7.19(금) - 7.21(일)',
    place: '북촌 한옥마을',
    status: '예정',
    priceType: '유료',
    tags: ['전통'],
  },
]

const filteredFestivals = computed(() =>
  weeklyFestivals.filter((festival) => festival.tags.includes(props.selectedCategory)),
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

<script setup>
import FestivalCard from '../festival/FestivalCard.vue'

const FestivalListStubView = {
  template: `
    <main class="container" style="padding: 24px 0 40px;">
      <h2 style="margin:0 0 8px;">축제 캘린더</h2>
      <p style="margin:0;color:#5f766d;">메인 페이지에서 캘린더/추천 축제를 확인할 수 있어요.</p>
    </main>
  `,
}

const MapStubView = {
  template: `
    <main class="container" style="padding: 24px 0 40px;">
      <h2 style="margin:0 0 8px;">지도 탐색</h2>
      <p style="margin:0;color:#5f766d;">현재는 홈의 지도 미리보기 UI를 사용 중입니다.</p>
    </main>
  `,
}

const weeklyFestivals = [
  {
    id: 'w1',
    title: '한강 불빛 축제 2025',
    date: '2026.07.18 - 2026.07.20',
    place: '여의도 한강공원',
    status: '진행중',
    priceType: '무료',
    imageUrl: '',
  },
  {
    id: 'w2',
    title: '서울숲 음악 페스티벌',
    date: '2026.07.19 - 2026.07.21',
    place: '서울숲 공원',
    status: '진행중',
    priceType: '무료',
    imageUrl: '',
  },
  {
    id: 'w3',
    title: '북촌 한옥 야행',
    date: '2026.07.24 - 2026.07.25',
    place: '북촌 한옥마을',
    status: '예정',
    priceType: '유료',
    imageUrl: '',
  },
]
</script>

<template>
  <section class="container weekly">
    <div class="section-head">
      <h3>이번 주 추천 축제</h3>
      <RouterLink to="/festivals" class="more-link">전체 보기</RouterLink>
    </div>

    <div class="card-grid">
      <FestivalCard
        v-for="item in weeklyFestivals"
        :key="item.id"
        :festival="item"
      />
    </div>
  </section>
</template>

<style scoped>
.weekly {
  display: grid;
  gap: 14px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-head h3 {
  margin: 0;
  font-size: 24px;
  color: #25453a;
}

.more-link {
  font-weight: 700;
  color: var(--color-primary-dark);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .card-grid {
    display: flex;
    overflow-x: auto;
    gap: 12px;
    padding-bottom: 6px;
  }

  .card-grid > * {
    flex: 0 0 82%;
  }
}
</style>
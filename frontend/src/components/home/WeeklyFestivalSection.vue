<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import FestivalCard from '../festival/FestivalCard.vue'
import { getCurrentMonthSingleDayFestivals } from '../../services/festivalsApi'
import { getFestivalStatus, getFestivalTags } from '../../utils/festivalTags'
const props = defineProps({ selectedCategory: { type: String, default: '전체' } })
const weeklyFestivals = ref([])
onMounted(async () => {
  try {
    const festivals = await getCurrentMonthSingleDayFestivals()
    weeklyFestivals.value = festivals.map((festival) => ({
      id: festival.id, title: festival.title, date: festival.period, place: festival.place,
      imageUrl: festival.imageUrl, status: getFestivalStatus(festival),
      priceType: /무료/.test(festival.title) ? '무료' : '유료', tags: getFestivalTags(festival),
    }))
  } catch { weeklyFestivals.value = [] }
})
const filteredFestivals = computed(() => weeklyFestivals.value.filter((festival) => festival.tags.includes(props.selectedCategory)))
</script>
<template>
  <section class="weekly section-card">
    <header class="section-head"><h2>축제 목록</h2><RouterLink to="/festivals">더보기 <span>›</span></RouterLink></header>
    <div v-if="filteredFestivals.length" class="card-slider"><FestivalCard v-for="item in filteredFestivals" :key="item.id" :festival="item" /></div>
    <p v-else class="empty-state">이번 달에 진행하는 당일 축제가 없습니다.</p>
  </section>
</template>
<style scoped>
.weekly{height:100%;display:flex;flex-direction:column;padding:16px;border-radius:18px}.section-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px}h2{margin:0;color:#24372e;font-size:20px;letter-spacing:-.035em}.section-head a{color:#6b756f;font-size:12px;font-weight:750}.card-slider{flex:1;display:flex;align-items:stretch;gap:10px;overflow-x:auto;padding-bottom:6px;scroll-snap-type:x proximity;scrollbar-width:thin}.card-slider :deep(.festival-card){flex:0 0 clamp(220px,22vw,250px);scroll-snap-align:start}.empty-state{margin:10px 0 2px;flex:1;min-height:110px;display:grid;place-items:center;border:1px dashed #d6dfd1;border-radius:14px;background:#fbfdf8;color:#6a7b72;font-size:13px;font-weight:700}@media(max-width:760px){.card-slider{gap:8px}.card-slider :deep(.festival-card){flex-basis:230px}}
</style>

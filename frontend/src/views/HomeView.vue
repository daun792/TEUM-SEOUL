<script setup>
import { ref } from 'vue'
import HeroSection from '../components/home/HeroSection.vue'
import QuickCategoryMenu from '../components/home/QuickCategoryMenu.vue'
import WeeklyFestivalSection from '../components/home/WeeklyFestivalSection.vue'
import FestivalCalendarSection from '../components/home/FestivalCalendarSection.vue'
import MapPreviewSection from '../components/home/MapPreviewSection.vue'
import CommunityPreviewSection from '../components/home/CommunityPreviewSection.vue'
import HomeDecoration from '../components/home/HomeDecoration.vue'

const activeCategory = ref('전체')
</script>

<template>
  <div class="home-page">
    <HeroSection />

    <div class="quick-layer">
      <QuickCategoryMenu v-model="activeCategory" />
    </div>

    <section class="container dashboard" aria-label="틈서울 메인 콘텐츠">
      <WeeklyFestivalSection class="festival-panel" :selected-category="activeCategory" />
      <FestivalCalendarSection class="calendar-panel" :selected-category="activeCategory" />
      <MapPreviewSection class="map-panel" :selected-category="activeCategory" />
      <CommunityPreviewSection class="community-panel" />
    </section>

    <HomeDecoration />
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(circle at 90% 22%, rgba(181, 224, 91, 0.1), transparent 24%),
    linear-gradient(180deg, #fffef9 0%, #fbfaf4 100%);
}

.quick-layer {
  position: relative;
  z-index: 6;
  margin-top: -34px;
}

.dashboard {
  position: relative;
  z-index: 4;
  display: grid;
  grid-template-columns: minmax(470px, 1.65fr) minmax(280px, 0.92fr) minmax(350px, 1.18fr) minmax(280px, 0.92fr);
  gap: 14px;
  margin-top: 14px;
  align-items: start;
}

.dashboard > * {
  min-width: 0;
}

@media (max-width: 1320px) {
  .dashboard {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .quick-layer {
    margin-top: -18px;
  }

  .dashboard {
    grid-template-columns: 1fr;
    gap: 14px;
  }
}
</style>

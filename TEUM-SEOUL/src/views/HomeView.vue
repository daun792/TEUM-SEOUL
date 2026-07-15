<script setup>
import HeroSection from '../components/home/HeroSection.vue'
import QuickCategoryMenu from '../components/home/QuickCategoryMenu.vue'
import WeeklyFestivalSection from '../components/home/WeeklyFestivalSection.vue'
import FestivalCalendarSection from '../components/home/FestivalCalendarSection.vue'
import MapPreviewSection from '../components/home/MapPreviewSection.vue'
import CommunityPreviewSection from '../components/home/CommunityPreviewSection.vue'
</script>

<template>
  <div class="home-page">
    <HeroSection />
    <QuickCategoryMenu />
    <WeeklyFestivalSection />

    <div class="grid-2 container">
      <FestivalCalendarSection />
      <MapPreviewSection />
    </div>

    <CommunityPreviewSection />
  </div>
</template>

<style scoped>
.home-page {
  display: grid;
  gap: 24px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 1024px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
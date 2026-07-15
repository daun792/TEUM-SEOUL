<script setup>
import { RouterLink } from 'vue-router'
import HomeDecoration from './HomeDecoration.vue'
</script>

<template>
  <section class="hero container">
    <div class="hero-text">
      <p class="eyebrow">서울의 틈에서, 오늘의 즐거움을 발견하세요.</p>
      <h2>
        서울 곳곳의 축제와<br />
        주변 명소를 한눈에!
      </h2>
      <p class="desc">
        축제 정보부터 주변 관광지, 문화시설, 쇼핑까지
        지도에서 쉽고 빠르게 찾아보세요.
      </p>

      <div class="hero-actions">
        <RouterLink class="primary-btn" to="/festivals">이번 주 축제 보기</RouterLink>
        <RouterLink class="ghost-btn" to="/map">지도에서 둘러보기</RouterLink>
      </div>
    </div>

    <HomeDecoration />
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 24px;
  align-items: center;
  margin-top: 8px;
}

.hero-text {
  display: grid;
  gap: 14px;
}

.eyebrow {
  display: inline-flex;
  width: fit-content;
  padding: 7px 12px;
  border-radius: 999px;
  background: #ecfbe7;
  color: var(--color-primary-dark);
  font-weight: 700;
  font-size: 13px;
}

h2 {
  margin: 0;
  font-size: clamp(28px, 4vw, 46px);
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: #214338;
}

.desc {
  margin: 0;
  color: #4f6a60;
}

.hero-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.primary-btn,
.ghost-btn {
  border-radius: var(--radius-pill);
  padding: 10px 16px;
  font-weight: 700;
}

.primary-btn {
  background: var(--color-primary);
  color: #fff;
}

.ghost-btn {
  background: #fff;
  border: 1px solid var(--color-border);
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
  }
}
</style>
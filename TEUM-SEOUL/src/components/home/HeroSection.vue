<script setup>
import { RouterLink } from 'vue-router'

const markers = [
  { label: '관광지', className: 'marker-tour' },
  { label: '공연', className: 'marker-show' },
  { label: '전시', className: 'marker-exhibit' },
  { label: '체험', className: 'marker-experience' },
  { label: '쇼핑', className: 'marker-shopping' },
]
</script>

<template>
  <section class="hero-shell">
    <div class="container hero">
      <div class="hero-copy">
        <p class="eyebrow">서울의 틈을 따라 <span aria-hidden="true">↗</span></p>
        <h1>오늘의 축제를<br />발견해보세요!</h1>
        <p class="description">
          서울 곳곳에서 열리는 축제와<br />주변 명소를 지도에서 쉽고 빠르게 찾아보세요.
        </p>

        <div class="hero-actions">
          <RouterLink class="primary-btn" to="/festivals">
            <span class="btn-icon" aria-hidden="true">◌</span>
            축제 둘러보기
          </RouterLink>
          <RouterLink class="secondary-btn" to="/map">
            <span class="btn-icon" aria-hidden="true">⌖</span>
            지도에서 찾기
          </RouterLink>
        </div>
      </div>

      <div class="hero-visual asset-placeholder" aria-label="3D 서울 미니어처 일러스트 자리">
        <div class="placeholder-copy">
          <strong>3D 서울 미니어처 메인 일러스트</strong>
          <span>한강 · 남산타워 · 한옥 · 공연장 · DDP · 상점</span>
        </div>

        <button
          v-for="marker in markers"
          :key="marker.label"
          type="button"
          class="floating-marker"
          :class="marker.className"
        >
          <span class="marker-dot" aria-hidden="true"></span>
          {{ marker.label }}
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-shell {
  position: relative;
  isolation: isolate;
  min-height: 472px;
  overflow: hidden;
  background:
    radial-gradient(circle at 67% 18%, rgba(169, 228, 236, 0.3), transparent 28%),
    radial-gradient(circle at 40% 74%, rgba(185, 221, 90, 0.15), transparent 28%),
    linear-gradient(110deg, #fffef9 0%, #fffdf7 34%, #f6fbef 100%);
}

.hero-shell::before,
.hero-shell::after {
  content: '';
  position: absolute;
  z-index: -1;
  border-radius: 50%;
  filter: blur(4px);
}

.hero-shell::before {
  width: 320px;
  height: 320px;
  right: -90px;
  top: 22px;
  background: rgba(169, 228, 236, 0.22);
}

.hero-shell::after {
  width: 220px;
  height: 220px;
  left: 38%;
  bottom: -120px;
  background: rgba(185, 221, 90, 0.18);
}

.hero {
  min-height: 472px;
  display: grid;
  grid-template-columns: minmax(350px, 0.9fr) minmax(620px, 1.85fr);
  align-items: center;
  gap: 16px;
}

.hero-copy {
  position: relative;
  z-index: 4;
  padding: 34px 0 74px 28px;
}

.eyebrow {
  margin: 0 0 16px;
  color: var(--color-primary-dark);
  font-size: 16px;
  font-weight: 850;
  letter-spacing: -0.04em;
}

.eyebrow span {
  color: var(--color-primary);
}

h1 {
  margin: 0;
  font-size: clamp(46px, 4.2vw, 66px);
  line-height: 1.13;
  letter-spacing: -0.065em;
  color: #1a3629;
}

.description {
  margin: 22px 0 0;
  color: #40554c;
  font-size: 16px;
  line-height: 1.75;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.primary-btn,
.secondary-btn {
  min-height: 50px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 0 22px;
  border-radius: var(--radius-pill);
  font-size: 15px;
  font-weight: 850;
  box-shadow: 0 10px 22px rgba(40, 67, 53, 0.1);
}

.primary-btn {
  background: linear-gradient(135deg, #76bd38, #4f9d27);
  color: #fff;
}

.secondary-btn {
  border: 1px solid #dcded5;
  background: rgba(255, 255, 255, 0.9);
  color: #273a31;
}

.btn-icon {
  font-size: 18px;
}

.hero-visual {
  position: relative;
  align-self: stretch;
  min-height: 438px;
  margin: 18px 0 54px;
  border-radius: 42% 20% 18% 36% / 18% 23% 38% 28%;
  box-shadow: inset 0 0 0 14px rgba(255, 255, 255, 0.22);
}

.hero-visual::after {
  content: none;
}

.placeholder-copy {
  display: grid;
  gap: 8px;
  padding: 18px 26px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(105, 182, 47, 0.2);
  box-shadow: 0 12px 30px rgba(54, 90, 70, 0.1);
}

.placeholder-copy strong {
  color: #3d603b;
  font-size: 17px;
}

.placeholder-copy span {
  color: #70806f;
  font-size: 13px;
}

.floating-marker {
  position: absolute;
  z-index: 3;
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 15px;
  border: 1px solid rgba(220, 222, 213, 0.9);
  border-radius: var(--radius-pill);
  background: rgba(255, 255, 255, 0.94);
  color: #34453d;
  font-weight: 850;
  box-shadow: 0 10px 22px rgba(56, 80, 68, 0.13);
}

.marker-dot {
  width: 14px;
  height: 14px;
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  background: currentColor;
}

.marker-tour {
  top: 14%;
  left: 48%;
  color: #4b9d27;
}

.marker-show {
  top: 35%;
  left: 30%;
  color: #f2584f;
}

.marker-exhibit {
  top: 27%;
  right: 8%;
  color: #7867ca;
}

.marker-experience {
  top: 53%;
  left: 52%;
  color: #2da6bc;
}

.marker-shopping {
  right: 5%;
  bottom: 17%;
  color: #ec781e;
}

@media (max-width: 1100px) {
  .hero {
    grid-template-columns: minmax(320px, 0.9fr) minmax(480px, 1.4fr);
  }

  .hero-copy {
    padding-left: 0;
  }
}

@media (max-width: 850px) {
  .hero-shell,
  .hero {
    min-height: auto;
  }

  .hero {
    grid-template-columns: 1fr;
    padding-top: 20px;
  }

  .hero-copy {
    padding: 28px 0 6px;
  }

  h1 {
    font-size: clamp(40px, 11vw, 56px);
  }

  .hero-visual {
    min-height: 340px;
    margin: 8px 0 46px;
  }
}

@media (max-width: 520px) {
  .description br {
    display: none;
  }

  .hero-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .primary-btn,
  .secondary-btn {
    padding: 0 14px;
    font-size: 13px;
  }

  .hero-visual {
    min-height: 300px;
    border-radius: 24px;
  }

  .floating-marker {
    min-height: 36px;
    padding: 0 11px;
    font-size: 12px;
  }
}
</style>

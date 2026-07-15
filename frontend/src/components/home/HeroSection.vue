<script setup>
import { RouterLink } from 'vue-router'
import heroImage from '../../assets/hero-seoul-isometric.webp'

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
          서울 곳곳에서 열리는 축제와<br />
          주변 명소를 지도에서 쉽고 빠르게 찾아보세요.
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

      <div class="hero-visual" aria-label="3D 서울 미니어처 일러스트">
        <img class="hero-art" :src="heroImage" alt="3D 서울 미니어처 메인 일러스트" />

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
    radial-gradient(circle at 10% 20%, rgba(185, 221, 90, 0.12), transparent 35%),
    radial-gradient(circle at 90% 12%, rgba(169, 228, 236, 0.18), transparent 34%),
    linear-gradient(180deg, #fffef9 0%, #fbfaf4 100%);
}

.hero {
  min-height: 472px;
  display: grid;
  grid-template-columns: minmax(340px, 0.9fr) minmax(620px, 1.85fr);
  align-items: center;
  gap: 12px;
}

.hero-copy {
  position: relative;
  z-index: 5;
  padding: 26px 0 42px;
}

.eyebrow {
  margin: 0 0 14px;
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
  font-size: clamp(46px, 4.1vw, 66px);
  line-height: 1.12;
  letter-spacing: -0.065em;
  color: #1a3629;
}

.description {
  margin: 18px 0 0;
  color: #40554c;
  font-size: 16px;
  line-height: 1.75;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
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
  background: rgba(255, 255, 255, 0.92);
  color: #273a31;
}

.btn-icon {
  font-size: 18px;
}

.hero-visual {
  position: relative;
  align-self: stretch;
  min-height: 428px;
  overflow: hidden;
}

.hero-art {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
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
  background: rgba(255, 255, 255, 0.95);
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
  top: 13%;
  left: 47%;
  transform: translateX(-50%);
  color: #4b9d27;
}

.marker-show {
  top: 33%;
  left: 30%;
  color: #f2584f;
}

.marker-exhibit {
  top: 24%;
  right: 7%;
  color: #7867ca;
}

.marker-experience {
  top: 52%;
  left: 41%;
  color: #2da6bc;
}

.marker-shopping {
  right: 5%;
  bottom: 24%;
  color: #ec781e;
}

@media (max-width: 1100px) {
  .hero {
    grid-template-columns: minmax(320px, 0.95fr) minmax(520px, 1.4fr);
  }

  .hero-copy {
    padding-top: 18px;
  }

  h1 {
    font-size: clamp(40px, 5vw, 56px);
  }
}

@media (max-width: 850px) {
  .hero-shell,
  .hero {
    min-height: auto;
  }

  .hero {
    grid-template-columns: 1fr;
    gap: 8px;
    padding-top: 18px;
  }

  .hero-copy {
    padding: 16px 0 6px;
  }

  .hero-visual {
    min-height: 340px;
  }

  .hero-art {
    object-position: center top;
  }

  .marker-tour {
    top: 9%;
    left: 50%;
    transform: translateX(-50%);
  }

  .marker-show {
    top: 31%;
    left: 16%;
  }

  .marker-exhibit {
    top: 23%;
    right: 4%;
  }

  .marker-experience {
    top: 52%;
    left: 40%;
  }

  .marker-shopping {
    right: 3%;
    bottom: 14%;
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
  }

  .floating-marker {
    min-height: 36px;
    padding: 0 11px;
    font-size: 12px;
  }
}
</style>

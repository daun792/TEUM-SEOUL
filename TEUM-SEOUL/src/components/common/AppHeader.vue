<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const mobileOpen = ref(false)

const closeMobileMenu = () => {
  mobileOpen.value = false
}
</script>

<template>
  <header class="app-header">
    <div class="container header-inner">
      <RouterLink class="brand" to="/" aria-label="틈서울 홈" @click="closeMobileMenu">
        <span class="brand-word">틈서울</span>
        <span class="brand-pin" aria-hidden="true"></span>
      </RouterLink>

      <nav class="desktop-nav" aria-label="주요 메뉴">
        <RouterLink to="/festivals">축제 캘린더</RouterLink>
        <RouterLink to="/map">지도 탐색</RouterLink>
        <RouterLink to="/board">게시판</RouterLink>
        <RouterLink to="/about">틈서울 소개</RouterLink>
      </nav>

      <div class="desktop-actions">
        <button type="button" class="round-action" aria-label="검색">
          <span aria-hidden="true">⌕</span>
        </button>
        <button type="button" class="round-action" aria-label="북마크">
          <span aria-hidden="true">♡</span>
        </button>
        <RouterLink class="week-btn" to="/festivals">이번 주 축제</RouterLink>
      </div>

      <button
        type="button"
        class="mobile-menu-btn"
        :aria-expanded="mobileOpen"
        aria-controls="mobile-nav"
        aria-label="메뉴 열기"
        @click="mobileOpen = !mobileOpen"
      >
        <span></span><span></span><span></span>
      </button>
    </div>

    <nav v-if="mobileOpen" id="mobile-nav" class="mobile-nav" aria-label="모바일 메뉴">
      <RouterLink to="/festivals" @click="closeMobileMenu">축제 캘린더</RouterLink>
      <RouterLink to="/map" @click="closeMobileMenu">지도 탐색</RouterLink>
      <RouterLink to="/board" @click="closeMobileMenu">게시판</RouterLink>
      <RouterLink to="/about" @click="closeMobileMenu">틈서울 소개</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid rgba(224, 225, 214, 0.92);
  background: rgba(255, 254, 249, 0.94);
  backdrop-filter: blur(16px);
}

.header-inner {
  min-height: 76px;
  display: grid;
  grid-template-columns: 220px 1fr 260px;
  align-items: center;
  gap: 20px;
}

.brand {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  gap: 7px;
}

.brand-word {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.09em;
  color: #274f2d;
}

.brand-word::first-letter {
  color: var(--color-primary);
}

.brand-pin {
  position: relative;
  width: 17px;
  height: 17px;
  border-radius: 50% 50% 50% 0;
  background: var(--color-primary);
  transform: rotate(-45deg);
}

.brand-pin::after {
  content: '';
  position: absolute;
  width: 6px;
  height: 6px;
  left: 5px;
  top: 5px;
  border-radius: 50%;
  background: #fff;
}

.desktop-nav {
  display: flex;
  justify-content: center;
  gap: clamp(22px, 3vw, 52px);
}

.desktop-nav a {
  position: relative;
  padding: 8px 0;
  font-size: 15px;
  font-weight: 750;
  color: #1f2d27;
}

.desktop-nav a::after {
  content: '';
  position: absolute;
  left: 0;
  right: 100%;
  bottom: 2px;
  height: 2px;
  border-radius: 2px;
  background: var(--color-primary);
  transition: right 0.2s ease;
}

.desktop-nav a:hover::after,
.desktop-nav a.router-link-active::after {
  right: 0;
}

.desktop-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}

.round-action {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  background: #fff;
  color: #1c2b24;
  cursor: pointer;
  font-size: 24px;
  line-height: 1;
}

.week-btn {
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
  border-radius: var(--radius-pill);
  background: linear-gradient(135deg, #75bc36, #4c9c27);
  color: #fff;
  font-size: 14px;
  font-weight: 800;
  box-shadow: 0 8px 18px rgba(76, 156, 39, 0.2);
}

.mobile-menu-btn,
.mobile-nav {
  display: none;
}

@media (max-width: 1100px) {
  .header-inner {
    grid-template-columns: auto 1fr auto;
  }

  .desktop-nav {
    gap: 20px;
  }

  .desktop-actions .round-action {
    display: none;
  }
}

@media (max-width: 780px) {
  .header-inner {
    min-height: 66px;
    grid-template-columns: 1fr auto;
  }

  .brand-word {
    font-size: 24px;
  }

  .desktop-nav,
  .desktop-actions {
    display: none;
  }

  .mobile-menu-btn {
    width: 42px;
    height: 42px;
    display: grid;
    place-content: center;
    gap: 5px;
    border: 1px solid var(--color-border);
    border-radius: 50%;
    background: #fff;
  }

  .mobile-menu-btn span {
    width: 18px;
    height: 2px;
    border-radius: 2px;
    background: #26382f;
  }

  .mobile-nav {
    display: grid;
    gap: 4px;
    padding: 10px 14px 16px;
    border-top: 1px solid var(--color-border);
    background: #fffef9;
  }

  .mobile-nav a {
    padding: 11px 14px;
    border-radius: 12px;
    font-weight: 750;
  }

  .mobile-nav a.router-link-active {
    background: var(--color-primary-soft);
    color: var(--color-primary-dark);
  }
}
</style>

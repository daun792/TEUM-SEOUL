<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const mobileOpen = ref(false)

const toggleMobileMenu = () => {
  mobileOpen.value = !mobileOpen.value
}

const closeMobileMenu = () => {
  mobileOpen.value = false
}
</script>

<template>
  <header class="app-header">
    <div class="container header-inner">
      <RouterLink class="brand" to="/" @click="closeMobileMenu">
        <span class="pin" aria-hidden="true">📍</span>
        <span class="brand-text">틈서울</span>
      </RouterLink>

      <nav class="desktop-nav" aria-label="주요 메뉴">
        <RouterLink to="/festivals">축제 캘린더</RouterLink>
        <RouterLink to="/map">지도 탐색</RouterLink>
        <RouterLink to="/board">게시판</RouterLink>
        <RouterLink to="/about">틈서울 소개</RouterLink>
      </nav>

      <div class="desktop-actions">
        <button type="button" class="icon-btn" aria-label="검색">검색</button>
        <button type="button" class="icon-btn" aria-label="북마크">북마크</button>
        <button type="button" class="week-btn">이번 주 축제</button>
      </div>

      <button
        type="button"
        class="mobile-menu-btn"
        :aria-expanded="mobileOpen ? 'true' : 'false'"
        aria-controls="mobile-nav"
        @click="toggleMobileMenu"
      >
        메뉴
      </button>
    </div>

    <nav
      v-show="mobileOpen"
      id="mobile-nav"
      class="mobile-nav"
      aria-label="모바일 메뉴"
    >
      <div class="container mobile-nav-inner">
        <RouterLink to="/festivals" @click="closeMobileMenu">축제 캘린더</RouterLink>
        <RouterLink to="/map" @click="closeMobileMenu">지도 탐색</RouterLink>
        <RouterLink to="/board" @click="closeMobileMenu">게시판</RouterLink>
        <RouterLink to="/about" @click="closeMobileMenu">틈서울 소개</RouterLink>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border);
}

.header-inner {
  min-height: 72px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 16px;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  color: var(--color-primary-dark);
}

.pin {
  width: 30px;
  height: 30px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #eaf8e6;
}

.brand-text {
  font-size: 20px;
  letter-spacing: -0.02em;
}

.desktop-nav {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.desktop-nav a {
  padding: 8px 10px;
  border-radius: 999px;
  font-weight: 600;
  color: var(--color-text);
}

.desktop-nav a.router-link-active {
  background: #eef9e7;
  color: var(--color-primary-dark);
}

.desktop-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.icon-btn,
.week-btn,
.mobile-menu-btn {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-pill);
  background: #fff;
  color: var(--color-text);
  padding: 8px 12px;
  cursor: pointer;
}

.week-btn {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
  font-weight: 700;
}

.mobile-menu-btn {
  display: none;
}

.mobile-nav {
  border-top: 1px solid var(--color-border);
  background: #fff;
}

.mobile-nav-inner {
  display: grid;
  gap: 8px;
  padding: 12px 0 16px;
}

.mobile-nav a {
  padding: 10px 12px;
  border-radius: 10px;
  font-weight: 600;
}

.mobile-nav a.router-link-active {
  background: #eef9e7;
  color: var(--color-primary-dark);
}

@media (max-width: 1024px) {
  .desktop-actions {
    display: none;
  }
}

@media (max-width: 768px) {
  .header-inner {
    grid-template-columns: auto auto;
    justify-content: space-between;
  }

  .desktop-nav {
    display: none;
  }

  .mobile-menu-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
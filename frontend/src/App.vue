<script setup>
import { ref } from 'vue'
import ChatWidget from './components/chat/ChatWidget.vue'

const menuOpen = ref(false)
</script>

<template>
  <div class="app-layout">
    <header class="site-header">
      <RouterLink class="brand" to="/" @click="menuOpen = false"><span>틈</span>서울</RouterLink>
      <button class="menu-button" type="button" aria-label="메뉴 열기" @click="menuOpen = !menuOpen">☰</button>
      <nav :class="{ open: menuOpen }">
        <RouterLink to="/gap" @click="menuOpen = false">코스 추천</RouterLink>
        <RouterLink to="/posts" @click="menuOpen = false">커뮤니티</RouterLink>
        <RouterLink to="/bookmarks" @click="menuOpen = false">북마크</RouterLink>
      </nav>
    </header>
    <RouterView />
    <footer class="site-footer">
      <div><RouterLink class="brand footer-brand" to="/"><span>틈</span>서울</RouterLink><p>공연 전후 남는 시간을 채워주는 초단기 서울 코스 커뮤니티</p></div>
      <p>이 서비스는 한국관광공사 TourAPI 4.0 데이터를 활용했습니다.<br />라이선스: 공공누리 제3유형</p>
    </footer>
    <ChatWidget />
  </div>
</template>

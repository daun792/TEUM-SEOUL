<script setup>
import AppHeader from './components/common/AppHeader.vue'
import FloatingChatbot from './components/chat/FloatingChatbot.vue'
</script>

<template>
  <div class="app-shell">
    <AppHeader />

    <main class="main">
      <router-view />
    </main>

    <footer class="footer">
      <div class="container footer-inner">
        <p>© 2026 틈서울</p>
      </div>
    </footer>

    <FloatingChatbot />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  padding: 20px 0 40px;
}

.footer {
  border-top: 1px solid var(--color-border);
  background: #fff;
}

.footer-inner {
  min-height: 64px;
  display: flex;
  align-items: center;
  color: #5f766d;
}
</style>
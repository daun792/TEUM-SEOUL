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

    <FloatingChatbot />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.main {
  min-height: calc(100vh - 76px);
}
</style>

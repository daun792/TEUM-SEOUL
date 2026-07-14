<template> 
  <div class="app-shell"> 
    <header class="header"> 
      <h1 class="logo">틈서울</h1> 
      <nav class="nav"> 
        <router-link to="/">홈</router-link> 
        <router-link to="/board">게시판</router-link> 
        <router-link to="/about">소개</router-link> 
      </nav> 
    </header>
    <main class="main">
      <router-view />
    </main>
    <footer class="footer">
      <p>© 2026 틈서울</p>
    </footer>
    <button class="chatbot-fab" type="button">챗봇</button>
  </div> 
</template> 

<style scoped> 
  .app-shell { min-height: 100vh; 
    display: flex; 
    flex-direction: column; } 
  .header { position: sticky; 
    top: 0; z-index: 10; 
    background: #ffffff; 
    border-bottom: 1px solid #e5e7eb; 
    padding: 14px 20px; 
    display: flex; 
    justify-content: space-between; 
    align-items: center; } 
  .logo { margin: 0; 
    font-size: 20px; } 
  .nav { display: flex; 
    gap: 14px; } 
  .main { flex: 1; 
    padding: 20px; } 
  .footer { border-top: 1px solid #e5e7eb; 
    padding: 12px 20px; 
    background: #fafafa; } 
  .chatbot-fab { position: fixed; 
    right: 20px; 
    bottom: 20px; 
    width: 64px; 
    height: 64px; 
    border: none; 
    border-radius: 999px; 
    background: #0f766e; 
    color: white; 
    font-weight: 700; 
    cursor: pointer; } 
</style>
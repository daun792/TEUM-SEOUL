<template>
  <footer class="home-footer">
    <div class="landscape" aria-hidden="true">
      <span class="hill hill-one"></span>
      <span class="hill hill-two"></span>
      <span class="tower"></span>
      <span class="bridge"></span>
      <span v-for="index in 12" :key="index" class="tree" :style="{ '--i': index }"></span>
    </div>

    <div class="container footer-inner">
      <div class="footer-links">
        <a href="#">이용약관</a>
        <a href="#">개인정보처리방침</a>
        <a href="#">문의하기</a>
      </div>
      <p>© 2026 틈서울. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.home-footer {
  position: relative;
  margin-top: 34px;
  padding-top: 88px;
  background: #fffef9;
}

.landscape {
  position: absolute;
  inset: 0 0 auto;
  height: 95px;
  overflow: hidden;
}

.hill {
  position: absolute;
  bottom: -62px;
  width: 58%;
  height: 115px;
  border-radius: 50% 50% 0 0;
  background: #e7f2d9;
}

.hill-one {
  left: -6%;
}

.hill-two {
  right: -8%;
  background: #eff6e7;
}

.tree {
  position: absolute;
  left: calc((var(--i) - 1) * 8.7% + 2%);
  bottom: 14px;
  width: 7px;
  height: calc(17px + (var(--i) % 4) * 5px);
  border-radius: 999px 999px 4px 4px;
  background: #a8ca94;
}

.tree::after {
  content: '';
  position: absolute;
  left: 3px;
  bottom: -7px;
  width: 2px;
  height: 9px;
  background: #b7a487;
}

.tower {
  position: absolute;
  left: 50%;
  bottom: 10px;
  width: 5px;
  height: 48px;
  background: #adc9b4;
}

.tower::before,
.tower::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  background: #adc9b4;
}

.tower::before {
  bottom: 8px;
  width: 15px;
  height: 5px;
  border-radius: 5px;
}

.tower::after {
  top: -12px;
  width: 2px;
  height: 15px;
}

.bridge {
  position: absolute;
  left: 55%;
  bottom: 12px;
  width: 140px;
  height: 20px;
  border: 3px solid #b8d6d7;
  border-bottom: 0;
  border-radius: 80px 80px 0 0;
}

.footer-inner {
  min-height: 96px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  border-top: 1px solid #e5e7de;
  color: #7a837e;
  font-size: 11px;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-inner p {
  margin: 0;
}

@media (max-width: 700px) {
  .footer-inner {
    min-height: 110px;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }
}
</style>

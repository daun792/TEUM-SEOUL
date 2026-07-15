<script setup>
const markers = [
  { label: '공연', x: '18%', y: '58%', color: '#63B94F' },
  { label: '체험', x: '33%', y: '42%', color: '#FF8A3D' },
  { label: '관광지', x: '56%', y: '36%', color: '#A9E4EC' },
  { label: '문화시설', x: '72%', y: '54%', color: '#F45B4F' },
  { label: '쇼핑', x: '84%', y: '33%', color: '#B9DD5A' },
]
</script>

<template>
  <div class="mini-city section-card" aria-label="서울 미니어처 도시 일러스트">
    <div class="river"></div>
    <div class="tower">남산타워</div>
    <div class="hanok">전통 건물</div>
    <div class="park">공원</div>
    <div class="stage">축제 무대</div>
    <div class="truck">푸드트럭</div>
    <div class="ddp">DDP 느낌</div>

    <button
      v-for="marker in markers"
      :key="marker.label"
      class="marker"
      type="button"
      :style="{ left: marker.x, top: marker.y, '--marker-color': marker.color }"
    >
      {{ marker.label }}
    </button>
  </div>
</template>

<style scoped>
.mini-city {
  position: relative;
  min-height: 360px;
  overflow: hidden;
  padding: 20px;
  background:
    radial-gradient(circle at 18% 20%, #f0ffe4 0%, rgba(240, 255, 228, 0) 34%),
    radial-gradient(circle at 78% 16%, #e5f8ff 0%, rgba(229, 248, 255, 0) 32%),
    linear-gradient(180deg, #ffffff 0%, #f6fff5 100%);
}

.river {
  position: absolute;
  left: -5%;
  right: -5%;
  top: 52%;
  height: 70px;
  background: linear-gradient(90deg, #9de1ee, #6dd0e3, #9de1ee);
  border-radius: 999px;
  transform: rotate(-8deg);
  opacity: 0.8;
}

.tower,
.hanok,
.park,
.stage,
.truck,
.ddp {
  position: absolute;
  border-radius: 14px;
  padding: 8px 10px;
  font-size: 13px;
  font-weight: 700;
  color: #1f3d32;
  background: #fff;
  border: 1px solid var(--color-border);
}

.tower { left: 12%; top: 18%; }
.hanok { left: 34%; top: 20%; }
.park { left: 58%; top: 16%; }
.stage { left: 22%; top: 68%; }
.truck { left: 52%; top: 70%; }
.ddp { left: 74%; top: 64%; }

.marker {
  position: absolute;
  transform: translate(-50%, -50%);
  border: none;
  border-radius: 999px;
  padding: 6px 10px;
  font-weight: 700;
  font-size: 12px;
  color: #163428;
  background: var(--marker-color);
  cursor: pointer;
}

@media (max-width: 768px) {
  .mini-city {
    min-height: 280px;
  }
}
</style>
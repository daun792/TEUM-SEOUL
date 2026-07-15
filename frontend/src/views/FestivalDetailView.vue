<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getFestivalById } from '../mocks/festivals'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const route = useRoute()
const mapEl = ref(null)
const festival = ref(null)

let map = null
let marker = null

function renderMap() {
  if (!festival.value || !mapEl.value) return

  const { lat, lng, name } = festival.value

  if (!map) {
    map = L.map(mapEl.value).setView([lat, lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map)
  } else {
    map.setView([lat, lng], 15)
  }

  if (marker) marker.remove()
  marker = L.marker([lat, lng]).addTo(map).bindPopup(name).openPopup()
}

const loadFestival = async () => {
  festival.value = await getFestivalById(route.params.id)
  await nextTick()
  renderMap()
}

onMounted(async () => {
  await loadFestival()
})

watch(
  () => route.params.id,
  async () => {
    await loadFestival()
  }
)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    marker = null
  }
})
</script>

<template>
  <main v-if="festival" class="container detail-page">
    <section class="section-card detail-card">
      <header class="head">
        <h2>{{ festival.name }}</h2>
        <RouterLink to="/festivals" class="back-link">목록으로</RouterLink>
      </header>

      <div class="thumb" :class="{ placeholder: !festival.imageUrl }">
        <img v-if="festival.imageUrl" :src="festival.imageUrl" :alt="festival.name" />
        <span v-else>이미지 준비중</span>
      </div>

      <div class="meta-grid">
        <p><strong>기간</strong><span>{{ festival.period }}</span></p>
        <p><strong>장소</strong><span>{{ festival.place }}</span></p>
      </div>

      <p class="description">{{ festival.description }}</p>

      <h3>축제 위치</h3>
      <div ref="mapEl" class="map"></div>
    </section>
  </main>

  <main v-else class="container detail-page">
    <section class="section-card detail-card">
      <h2>축제를 찾을 수 없습니다.</h2>
      <RouterLink to="/festivals" class="back-link">목록으로</RouterLink>
    </section>
  </main>
</template>

<style scoped>
.detail-page {
  padding: 24px 0 40px;
}

.detail-card {
  padding: 20px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

h2 {
  margin: 0;
  color: #223b30;
  font-size: 28px;
  letter-spacing: -0.03em;
}

.back-link {
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border);
  background: #fff;
  color: #486357;
  font-size: 13px;
  font-weight: 800;
  padding: 8px 12px;
}

.thumb {
  height: 260px;
  border: 1px solid #e1e7dc;
  border-radius: 14px;
  overflow: hidden;
  background: #f5f8f0;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb.placeholder {
  display: grid;
  place-items: center;
  color: #6f8177;
  font-weight: 700;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 14px;
}

.meta-grid p {
  margin: 0;
  padding: 10px 12px;
  border: 1px solid #e3e8dd;
  border-radius: 12px;
  background: #fcfef9;
  display: grid;
  gap: 4px;
}

.meta-grid strong {
  color: #466055;
  font-size: 12px;
}

.meta-grid span {
  color: #243c31;
  font-weight: 700;
}

.description {
  margin: 12px 0 0;
  color: #3d564b;
  line-height: 1.6;
}

h3 {
  margin: 18px 0 10px;
  color: #2c453a;
  font-size: 18px;
}

.map {
  width: 100%;
  height: 360px;
  border: 1px solid #e1e7dc;
  border-radius: 14px;
}

@media (max-width: 760px) {
  .detail-page {
    padding-top: 18px;
  }

  .head {
    flex-wrap: wrap;
  }

  h2 {
    font-size: 24px;
  }

  .thumb {
    height: 210px;
  }

  .meta-grid {
    grid-template-columns: 1fr;
  }

  .map {
    height: 300px;
  }
}
</style>
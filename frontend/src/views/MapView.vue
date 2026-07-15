<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const mapRef = ref(null)
const selectedFilter = ref('축제')
const filters = ['축제', '관광지', '문화시설', '쇼핑', '체험', '반경 2km']

const places = [
  { id: 'f1', type: '축제', name: '한강 여름 음악축제', lat: 37.5288, lng: 126.9326 },
  { id: 'f2', type: '축제', name: '서울숲 피크닉 페스티벌', lat: 37.5444, lng: 127.0374 },
  { id: 't1', type: '관광지', name: '남산서울타워', lat: 37.5512, lng: 126.9882 },
  { id: 't2', type: '관광지', name: '경복궁', lat: 37.5796, lng: 126.977 },
  { id: 'c1', type: '문화시설', name: 'DDP', lat: 37.5663, lng: 127.0092 },
  { id: 's1', type: '쇼핑', name: '명동 거리', lat: 37.5637, lng: 126.9834 },
  { id: 'e1', type: '체험', name: '북촌 공예 체험관', lat: 37.5826, lng: 126.9832 },
]

const isInRadius2Km = (place) => {
  const center = { lat: 37.5665, lng: 126.978 }
  const dLat = place.lat - center.lat
  const dLng = place.lng - center.lng
  const approxKm = Math.sqrt(dLat * dLat + dLng * dLng) * 111
  return approxKm <= 2
}

const filteredPlaces = computed(() => {
  if (selectedFilter.value === '반경 2km') {
    return places.filter((place) => isInRadius2Km(place))
  }
  return places.filter((place) => place.type === selectedFilter.value)
})

let map = null
let markers = []

const renderMarkers = () => {
  if (!map) return

  markers.forEach((marker) => marker.remove())
  markers = filteredPlaces.value.map((place) =>
    L.marker([place.lat, place.lng]).addTo(map).bindPopup(`<strong>${place.name}</strong><br>${place.type}`),
  )
}

onMounted(async () => {
  await nextTick()
  if (!mapRef.value) return

  map = L.map(mapRef.value, { zoomControl: true }).setView([37.5665, 126.978], 12)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)

  renderMarkers()
})

watch(filteredPlaces, renderMarkers)

onBeforeUnmount(() => {
  map?.remove()
  map = null
})
</script>

<template>
  <main class="container map-page">
    <header class="page-head">
      <h1>지도 탐색</h1>
      <p>축제와 주변 장소를 유형별로 탐색해보세요.</p>
    </header>

    <section class="layout">
      <div class="map-box" ref="mapRef" aria-label="서울 지도"></div>

      <aside class="side-panel">
        <h2>표시 목록</h2>
        <ul>
          <li v-for="place in filteredPlaces" :key="place.id">
            <strong>{{ place.name }}</strong>
            <span>{{ place.type }}</span>
          </li>
        </ul>
      </aside>
    </section>

    <div class="filters" aria-label="지도 필터">
      <button
        v-for="item in filters"
        :key="item"
        type="button"
        class="chip"
        :class="{ active: selectedFilter === item }"
        @click="selectedFilter = item"
      >
        {{ item }}
      </button>
    </div>
  </main>
</template>

<style scoped>
.map-page {
  padding: 28px 0 40px;
  display: grid;
  gap: 14px;
}

.page-head h1 {
  margin: 0;
  font-size: 28px;
  letter-spacing: -0.03em;
  color: #233c31;
}

.page-head p {
  margin: 8px 0 0;
  color: #60756c;
}

.layout {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 14px;
}

.map-box {
  width: 100%;
  min-height: 520px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  overflow: hidden;
}

.side-panel {
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: #fff;
  padding: 12px;
}

.side-panel h2 {
  margin: 0 0 10px;
  font-size: 16px;
  color: #2f463b;
}

.side-panel ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.side-panel li {
  border: 1px solid #e8ebe4;
  border-radius: 10px;
  padding: 10px;
  display: grid;
  gap: 2px;
}

.side-panel strong {
  color: #274237;
  font-size: 14px;
}

.side-panel span {
  color: #667a71;
  font-size: 12px;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border: 1px solid var(--color-border);
  background: #fff;
  border-radius: var(--radius-pill);
  padding: 8px 12px;
  color: #304f42;
  font-weight: 750;
  cursor: pointer;
}

.chip.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

@media (max-width: 980px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .map-box {
    min-height: 400px;
  }
}

@media (max-width: 760px) {
  .map-page {
    padding-top: 18px;
  }

  .map-box {
    min-height: 320px;
  }
}
</style>

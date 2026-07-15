<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
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

const filters = ['축제', '관광지', '문화시설', '쇼핑', '반경 2km']

const allPlaces = [
  { id: 1, type: '축제', name: '한강 불빛 축제', lat: 37.5288, lng: 126.9326 },
  { id: 2, type: '관광지', name: '남산서울타워', lat: 37.5512, lng: 126.9882 },
  { id: 3, type: '문화시설', name: '국립중앙박물관', lat: 37.5239, lng: 126.9803 },
  { id: 4, type: '쇼핑', name: '명동 쇼핑거리', lat: 37.5637, lng: 126.9834 },
  { id: 5, type: '축제', name: '서울숲 음악 페스티벌', lat: 37.5444, lng: 127.0374 },
  { id: 6, type: '관광지', name: '경복궁', lat: 37.5796, lng: 126.977 },
  { id: 7, type: '문화시설', name: 'DDP', lat: 37.5665, lng: 127.0092 },
]

const filteredPlaces = computed(() => {
  if (selectedFilter.value === '반경 2km') {
    const center = { lat: 37.5665, lng: 126.978 }
    return allPlaces.filter((p) => {
      const dLat = p.lat - center.lat
      const dLng = p.lng - center.lng
      const approxKm = Math.sqrt(dLat * dLat + dLng * dLng) * 111
      return approxKm <= 2
    })
  }

  return allPlaces.filter((p) => p.type === selectedFilter.value)
})

let map = null
let markers = []

const renderMarkers = () => {
  if (!map) return

  markers.forEach((m) => m.remove())
  markers = []

  filteredPlaces.value.forEach((place) => {
    const marker = L.marker([place.lat, place.lng])
      .addTo(map)
      .bindPopup(`<b>${place.name}</b><br/>${place.type}`)
    markers.push(marker)
  })
}

onMounted(async () => {
  await nextTick()

  if (!mapRef.value) return

  map = L.map(mapRef.value).setView([37.5665, 126.978], 12)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)

  renderMarkers()
})

watch(filteredPlaces, () => {
  renderMarkers()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<template>
  <section class="container map-section section-card">
    <div class="section-head">
      <div>
        <h3>지도 미리보기</h3>
        <p>축제와 주변 관광지를 빠르게 탐색해보세요.</p>
      </div>
      <RouterLink to="/map" class="all-map-btn">전체 지도</RouterLink>
    </div>

    <div ref="mapRef" class="map-box"></div>

    <div class="filter-row">
      <button
        v-for="item in filters"
        :key="item"
        type="button"
        class="filter-btn"
        :class="{ active: selectedFilter === item }"
        @click="selectedFilter = item"
      >
        {{ item }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.map-section {
  padding: 18px;
  display: grid;
  gap: 14px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.section-head h3 {
  margin: 0;
  font-size: 24px;
  color: #25453a;
}

.section-head p {
  margin: 6px 0 0;
  color: #5c776d;
}

.all-map-btn {
  border-radius: 999px;
  border: 1px solid var(--color-border);
  padding: 8px 14px;
  background: #fff;
  font-weight: 700;
  color: var(--color-primary-dark);
}

.map-box {
  width: 100%;
  height: 420px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.filter-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-btn {
  border: 1px solid var(--color-border);
  background: #fff;
  color: #35584b;
  border-radius: 999px;
  padding: 8px 12px;
  font-weight: 700;
  cursor: pointer;
}

.filter-btn.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

@media (max-width: 768px) {
  .map-box {
    height: 320px;
  }
}
</style>
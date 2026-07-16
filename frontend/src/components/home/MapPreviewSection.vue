<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getPlaces } from '../../services/placesApi'
import { getFestivalList } from '../../services/festivalsApi'
import { placeTypeLabel, toApiCategory } from '../../utils/placeFilters'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const mapRef = ref(null)
const selectedFilter = ref('전체')
const filters = ['전체', '축제', '관광지', '문화시설', '쇼핑', '체험']
const allPlaces = ref([])
const filteredPlaces = computed(() => allPlaces.value)

const mapFestivalFallback = (festivals) =>
  festivals
    .filter((festival) => typeof festival.lat === 'number' && typeof festival.lng === 'number')
    .map((festival) => ({
      id: `festival-${festival.id}`,
      name: festival.title,
      type: festival.category || '축제공연행사',
      lat: festival.lat,
      lng: festival.lng,
    }))

const loadPlaces = async () => {
  try {
    const params = { page: 1, size: 200 }
    const apiCategory = toApiCategory(selectedFilter.value)
    if (apiCategory) params.category = apiCategory

    const page = await getPlaces(params)
    allPlaces.value = page.items.filter((place) => typeof place.lat === 'number' && typeof place.lng === 'number')

    if (!allPlaces.value.length) {
      const festivals = await getFestivalList({ page: 1, size: 200 })
      allPlaces.value = mapFestivalFallback(festivals)
    }
  } catch {
    try {
      const festivals = await getFestivalList({ page: 1, size: 200 })
      allPlaces.value = mapFestivalFallback(festivals)
    } catch {
      allPlaces.value = []
    }
  }
}

let map
let markers = []

const renderMarkers = () => {
  if (!map) return
  markers.forEach((marker) => marker.remove())
  markers = filteredPlaces.value.map((place) =>
    L.marker([place.lat, place.lng]).addTo(map).bindPopup(`<strong>${place.name}</strong><br>${placeTypeLabel(place)}`),
  )

  requestAnimationFrame(() => {
    map?.invalidateSize()
  })
}

onMounted(async () => {
  await nextTick()
  if (!mapRef.value) return

  map = L.map(mapRef.value, { zoomControl: true }).setView([37.5665, 126.978], 12)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)
  requestAnimationFrame(() => {
    map?.invalidateSize()
  })
  await loadPlaces()
  renderMarkers()
})

watch(filteredPlaces, renderMarkers)
watch(selectedFilter, async () => {
  await loadPlaces()
  renderMarkers()
})

onBeforeUnmount(() => {
  map?.remove()
  map = null
})
</script>

<template>
  <section class="map-section section-card">
    <header class="section-head">
      <h2>지도에서 찾기</h2>
      <RouterLink to="/map">전체 지도 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <div ref="mapRef" class="map-box" aria-label="서울 축제 지도"></div>

    <div class="filter-row">
      <button
        v-for="(item, index) in filters"
        :key="item"
        type="button"
        class="filter-btn"
        :class="{ active: selectedFilter === item }"
        @click="selectedFilter = item"
      >
        <span class="filter-icon" aria-hidden="true">{{ String(index + 1).padStart(2, '0') }}</span>
        <span class="filter-label">{{ item }}</span>
      </button>

    </div>
  </section>
</template>

<style scoped>
.map-section {
  padding: 16px;
  border-radius: 18px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

h2 {
  margin: 0;
  color: #24372e;
  font-size: 20px;
  letter-spacing: -0.035em;
}

.section-head a {
  color: #6b756f;
  font-size: 12px;
  font-weight: 750;
}

.map-box {
  width: 100%;
  height: 292px;
  overflow: hidden;
  border: 1px solid #e1e3dc;
  border-radius: 14px;
  background: #f0f4ed;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow-x: auto;
  padding-top: 12px;
  scrollbar-width: none;
}

.filter-row::-webkit-scrollbar {
  display: none;
}

.filter-btn {
  flex: 0 0 auto;
  width: 66px;
  min-height: 70px;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 8px;
  border: 0;
  border-radius: var(--radius-pill);
  background: #fff;
  color: #4d5c54;
  font-size: 11px;
  font-weight: 800;
  cursor: pointer;
  white-space: normal;
  text-align: center;
}

.filter-icon {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border: 1.5px dashed #b9c7b4;
  border-radius: 50%;
  font-size: 8px;
}

.filter-label {
  line-height: 1.15;
}

.filter-btn.active {
  color: var(--color-primary-dark);
}

.filter-btn.active .filter-icon {
  border-style: solid;
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
}

:deep(.leaflet-control-attribution) {
  font-size: 8px;
}

@media (max-width: 1320px) {
  .map-box {
    height: 355px;
  }
}

@media (max-width: 760px) {
  .map-box {
    height: 320px;
  }

  .filter-btn {
    width: 60px;
    min-height: 66px;
    padding-inline: 6px;
  }
}
</style>

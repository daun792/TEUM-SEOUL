<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getPlaces } from '../../services/placesApi'
import { MAP_FILTERS, placeTypeLabel, toApiCategory } from '../../utils/placeFilters'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const props = defineProps({
  selectedCategory: {
    type: String,
    default: '전체',
  },
})

const mapRef = ref(null)
const selectedFilter = ref('전체')
const filters = MAP_FILTERS
const allPlaces = ref([])
const filteredPlaces = computed(() => allPlaces.value)

const categoryToMapFilter = {
  전체: '전체',
  '다가오는 축제': '축제',
  '무료 축제': '축제',
  공연: '축제',
  전시: '전체',
  전통: '관광지',
  '야외 행사': '축제',
}

const loadPlaces = async () => {
  try {
    const params = { page: 1, size: 200 }
    if (selectedFilter.value === '반경 2km') {
      params.lat = 37.5665
      params.lng = 126.978
      params.radiusKm = 2
    } else {
      const apiCategory = toApiCategory(selectedFilter.value)
      if (apiCategory) params.category = apiCategory
    }

    const page = await getPlaces(params)
    allPlaces.value = page.items.filter((place) => typeof place.lat === 'number' && typeof place.lng === 'number')
  } catch {
    allPlaces.value = []
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

watch(
  () => props.selectedCategory,
  (category) => {
    selectedFilter.value = categoryToMapFilter[category] || '전체'
  },
  { immediate: true },
)

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
        {{ item }}
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
  gap: 8px;
  overflow-x: auto;
  padding-top: 12px;
  scrollbar-width: none;
}

.filter-row::-webkit-scrollbar {
  display: none;
}

.filter-btn {
  flex: 0 0 auto;
  min-height: 34px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 0;
  border-radius: var(--radius-pill);
  background: #fff;
  color: #4d5c54;
  font-size: 10px;
  font-weight: 800;
  cursor: pointer;
}

.filter-btn {
  padding: 0 8px 0 5px;
}

.filter-icon {
  width: 26px;
  height: 26px;
  display: grid;
  place-items: center;
  border: 1.5px dashed #b9c7b4;
  border-radius: 50%;
  font-size: 8px;
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
}
</style>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getPlaces } from '../services/placesApi'
import { getFestivalList } from '../services/festivalsApi'
import { MAP_FILTERS, placeTypeLabel, toApiCategory } from '../utils/placeFilters'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const mapRef = ref(null)
const selectedFilter = ref('전체')
const filters = MAP_FILTERS
const places = ref([])
const loading = ref(false)
const errorMessage = ref('')

const filteredPlaces = computed(() => {
  return places.value
})

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
  loading.value = true
  errorMessage.value = ''

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
    places.value = page.items.filter((place) => typeof place.lat === 'number' && typeof place.lng === 'number')

    if (!places.value.length) {
      const festivals = await getFestivalList({ page: 1, size: 200 })
      places.value = mapFestivalFallback(festivals)
    }
  } catch (error) {
    try {
      const festivals = await getFestivalList({ page: 1, size: 200 })
      places.value = mapFestivalFallback(festivals)
      errorMessage.value = places.value.length
        ? '장소 API 응답이 없어 축제 데이터만 표시 중입니다.'
        : (error instanceof Error ? error.message : '장소 데이터를 불러오지 못했습니다.')
    } catch {
      places.value = []
      errorMessage.value = error instanceof Error ? error.message : '장소 데이터를 불러오지 못했습니다.'
    }
  } finally {
    loading.value = false
  }
}

let map = null
let markers = []

const renderMarkers = () => {
  if (!map) return

  markers.forEach((marker) => marker.remove())
  markers = filteredPlaces.value.map((place) =>
    L.marker([place.lat, place.lng]).addTo(map).bindPopup(`<strong>${place.name}</strong><br>${placeTypeLabel(place)}`),
  )

  requestAnimationFrame(() => {
    map?.invalidateSize()
    if (markers.length > 1) {
      const group = L.featureGroup(markers)
      map?.fitBounds(group.getBounds(), { padding: [20, 20] })
    }
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
            <span>{{ placeTypeLabel(place) }}</span>
          </li>
        </ul>
        <p v-if="!loading && !filteredPlaces.length" class="state-text">표시 가능한 위치 데이터가 없습니다.</p>
        <p v-if="loading" class="state-text">장소 데이터를 불러오는 중입니다...</p>
        <p v-if="errorMessage" class="state-text error">{{ errorMessage }}</p>
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

.state-text {
  margin: 10px 0 0;
  color: #60756b;
  font-size: 12px;
  font-weight: 700;
}

.state-text.error {
  color: #b23b3b;
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

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getFestivalById, getFestivalNearby } from '../services/festivalsApi'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const route = useRoute()
const mapEl = ref(null)
const festival = ref(null)
const loading = ref(true)
const errorMessage = ref('')
const nearbyPlaces = ref([])
const nearbyLoading = ref(false)
const nearbyErrorMessage = ref('')
const selectedNearbyCategory = ref('전체')
const nearbyCategories = ['전체', '관광지', '문화시설', '쇼핑']

let map = null
let festivalMarker = null
let nearbyMarkers = []

const filteredNearbyPlaces = computed(() => {
  if (selectedNearbyCategory.value === '전체') {
    return nearbyPlaces.value
  }
  return nearbyPlaces.value.filter((place) => place.category === selectedNearbyCategory.value)
})

function renderMap() {
  if (!festival.value || !mapEl.value) return

  const { lat, lng, name } = festival.value
  if (typeof lat !== 'number' || typeof lng !== 'number') return

  if (!map) {
    map = L.map(mapEl.value).setView([lat, lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map)
    requestAnimationFrame(() => {
      map?.invalidateSize()
    })
  } else {
    map.setView([lat, lng], 15)
  }

  if (festivalMarker) festivalMarker.remove()
  festivalMarker = L.marker([lat, lng]).addTo(map).bindPopup(name).openPopup()

  nearbyMarkers.forEach((item) => item.remove())
  nearbyMarkers = filteredNearbyPlaces.value
    .filter((item) => typeof item.lat === 'number' && typeof item.lng === 'number')
    .map((item) => {
      const distanceLabel = typeof item.distanceKm === 'number' ? `${item.distanceKm.toFixed(2)}km` : '-'
      return L.marker([item.lat, item.lng])
        .addTo(map)
        .bindPopup(`<strong>${item.title}</strong><br>${item.category}<br>${distanceLabel}`)
    })
}

const loadNearbyPlaces = async () => {
  if (!festival.value) return
  nearbyLoading.value = true
  nearbyErrorMessage.value = ''
  try {
    const nearby = await getFestivalNearby(route.params.id, {
      radiusKm: 2,
      categories: ['관광지', '문화시설', '쇼핑'],
      limit: 8,
    })
    nearbyPlaces.value = nearby.items
  } catch (error) {
    nearbyPlaces.value = []
    nearbyErrorMessage.value = error instanceof Error ? error.message : '주변 장소를 불러오지 못했습니다.'
  } finally {
    nearbyLoading.value = false
  }
}

const loadFestival = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    festival.value = await getFestivalById(route.params.id)
    await nextTick()
    renderMap()
    await loadNearbyPlaces()
    await nextTick()
    renderMap()
  } catch (error) {
    festival.value = null
    errorMessage.value = error instanceof Error ? error.message : '축제 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
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

watch(filteredNearbyPlaces, async () => {
  await nextTick()
  renderMap()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    festivalMarker = null
    nearbyMarkers = []
  }
})
</script>

<template>
  <main v-if="loading" class="container detail-page">
    <section class="section-card detail-card">
      <h2>축제 정보를 불러오는 중입니다.</h2>
    </section>
  </main>

  <main v-else-if="festival" class="container detail-page">
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

      <RouterLink class="related-link" :to="`/board?festival_id=${festival.id}`">이 축제 관련 게시글 보기</RouterLink>

      <p class="description">{{ festival.description }}</p>

      <h3>축제 위치</h3>
      <div v-if="typeof festival.lat === 'number' && typeof festival.lng === 'number'" ref="mapEl" class="map"></div>
      <p v-else class="map-empty">위치 좌표가 없어 지도를 표시할 수 없습니다.</p>

      <h3>주변 장소 (반경 2km, 최대 8개)</h3>
      <p class="distance-note">거리 값은 실제 이동거리/시간이 아닌 직선거리 기준입니다.</p>

      <div class="filter-row">
        <button
          v-for="category in nearbyCategories"
          :key="category"
          type="button"
          class="filter-btn"
          :class="{ active: selectedNearbyCategory === category }"
          @click="selectedNearbyCategory = category"
        >
          {{ category }}
        </button>
      </div>

      <ul v-if="!nearbyLoading && filteredNearbyPlaces.length" class="nearby-list">
        <li v-for="place in filteredNearbyPlaces" :key="place.id + place.title">
          <strong>{{ place.title }}</strong>
          <span>{{ place.category }} | {{ place.address }}</span>
          <span class="distance">직선거리 {{ typeof place.distanceKm === 'number' ? `${place.distanceKm.toFixed(2)}km` : '-' }}</span>
        </li>
      </ul>
      <p v-else-if="nearbyLoading" class="map-empty">주변 장소를 불러오는 중입니다.</p>
      <p v-else-if="nearbyErrorMessage" class="map-empty">{{ nearbyErrorMessage }}</p>
      <p v-else class="map-empty">조건에 맞는 주변 장소가 없습니다.</p>
    </section>
  </main>

  <main v-else class="container detail-page">
    <section class="section-card detail-card">
      <h2>{{ errorMessage || '축제를 찾을 수 없습니다.' }}</h2>
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

.related-link {
  display: inline-flex;
  margin-top: 12px;
  border-radius: var(--radius-pill);
  border: 1px solid #c9d8c4;
  padding: 8px 12px;
  color: #3e5a4e;
  font-size: 13px;
  font-weight: 800;
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

.map-empty {
  margin: 0;
  padding: 14px;
  border: 1px dashed #d4ded0;
  border-radius: 12px;
  color: #5f7468;
  background: #f9fcf6;
}

.distance-note {
  margin: 0 0 10px;
  color: #667b70;
  font-size: 13px;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.filter-btn {
  border: 1px solid #d2ddd0;
  border-radius: var(--radius-pill);
  background: #fff;
  color: #426256;
  padding: 7px 12px;
  font-weight: 800;
  cursor: pointer;
}

.filter-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

.nearby-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.nearby-list li {
  border: 1px solid #dfe7da;
  border-radius: 12px;
  padding: 10px 12px;
  display: grid;
  gap: 4px;
}

.nearby-list strong {
  color: #2a4338;
}

.nearby-list span {
  color: #5f7469;
  font-size: 13px;
}

.nearby-list .distance {
  font-weight: 800;
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
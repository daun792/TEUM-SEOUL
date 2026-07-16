<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getFestivalById, getFestivalNearby } from '../services/festivalsApi'

L.Icon.Default.mergeOptions({ iconRetinaUrl: markerIcon2x, iconUrl: markerIcon, shadowUrl: markerShadow })
const route = useRoute()
const mapEl = ref(null)
const festival = ref(null)
const loading = ref(true)
const errorMessage = ref('')
const nearbyPlaces = ref([])
const nearbyLoading = ref(false)
const nearbyErrorMessage = ref('')
const selectedNearbyCategory = ref('전체')
const selectedPlace = ref(null)
const nearbyCategories = ['전체', '관광지', '문화시설', '쇼핑']
let map = null
let festivalMarker = null
let nearbyMarkers = []

const filteredNearbyPlaces = computed(() => selectedNearbyCategory.value === '전체'
  ? nearbyPlaces.value
  : nearbyPlaces.value.filter((place) => place.category === selectedNearbyCategory.value))
const festivalDays = computed(() => {
  if (!festival.value?.start || !festival.value?.end) return ''
  const days = Math.round((new Date(festival.value.end) - new Date(festival.value.start)) / 86400000) + 1
  return Number.isFinite(days) && days > 0 ? `${days}일간` : ''
})
const categoryIcon = (category) => ({ 관광지: '🌳', 문화시설: '🏛️', 쇼핑: '🛍️' }[category] || '📍')

function selectPlace(place) {
  selectedPlace.value = place
  if (map && typeof place.lat === 'number' && typeof place.lng === 'number') map.flyTo([place.lat, place.lng], 16)
}

function renderMap() {
  if (!festival.value || !mapEl.value) return
  const { lat, lng, name } = festival.value
  if (typeof lat !== 'number' || typeof lng !== 'number') return
  if (!map) {
    map = L.map(mapEl.value).setView([lat, lng], 15)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors' }).addTo(map)
    requestAnimationFrame(() => map?.invalidateSize())
  } else map.setView([lat, lng], 15)
  festivalMarker?.remove()
  festivalMarker = L.marker([lat, lng]).addTo(map).bindPopup(name).openPopup()
  nearbyMarkers.forEach((item) => item.remove())
  nearbyMarkers = filteredNearbyPlaces.value
    .filter((item) => typeof item.lat === 'number' && typeof item.lng === 'number')
    .map((item) => L.marker([item.lat, item.lng]).addTo(map)
      .bindPopup(`<strong>${item.title}</strong><br>${item.category}<br>${typeof item.distanceKm === 'number' ? item.distanceKm.toFixed(2) + 'km' : '-'}`)
      .on('click', () => { selectedPlace.value = item }))
}

async function loadNearbyPlaces() {
  if (!festival.value) return
  nearbyLoading.value = true
  nearbyErrorMessage.value = ''
  try {
    const nearby = await getFestivalNearby(route.params.id, { radiusKm: 2, categories: ['관광지', '문화시설', '쇼핑'], limit: 8 })
    nearbyPlaces.value = nearby.items
    selectedPlace.value = nearby.items[0] || null
  } catch (error) {
    nearbyPlaces.value = []
    selectedPlace.value = null
    nearbyErrorMessage.value = error instanceof Error ? error.message : '주변 장소를 불러오지 못했습니다.'
  } finally { nearbyLoading.value = false }
}

async function loadFestival() {
  loading.value = true
  errorMessage.value = ''
  try {
    festival.value = await getFestivalById(route.params.id)
    await loadNearbyPlaces()
  } catch (error) {
    festival.value = null
    errorMessage.value = error instanceof Error ? error.message : '축제 정보를 불러오지 못했습니다.'
  } finally { loading.value = false }
  await nextTick()
  renderMap()
}
onMounted(loadFestival)
watch(() => route.params.id, loadFestival)
watch(filteredNearbyPlaces, async (places) => {
  if (!places.some((place) => place.id === selectedPlace.value?.id)) selectedPlace.value = places[0] || null
  await nextTick()
  renderMap()
})
onBeforeUnmount(() => { map?.remove(); map = null; festivalMarker = null; nearbyMarkers = [] })
</script>

<template>
  <main v-if="loading" class="container detail-page"><section class="section-card status-card"><span class="loader"></span><h2>축제 정보를 불러오는 중입니다.</h2></section></main>
  <main v-else-if="festival" class="detail-page">
    <div class="container">
      <nav class="breadcrumb"><RouterLink to="/">홈</RouterLink><span>›</span><RouterLink to="/festivals">축제 캘린더</RouterLink><span>›</span><strong>축제 상세</strong></nav>
      <section class="hero-card">
        <div class="hero-image" :class="{ placeholder: !festival.imageUrl }">
          <img v-if="festival.imageUrl" :src="festival.imageUrl" :alt="festival.name" /><span v-else>이미지 준비중</span>
          <div class="hero-tags"><span>진행중</span><span>{{ festival.category }}</span></div>
        </div>
        <div class="hero-info">
          <div class="title-row"><h1>{{ festival.name }}</h1><span class="star">★</span></div>
          <dl class="festival-meta">
            <div><dt>▣ &nbsp;기간</dt><dd>{{ festival.period }} <em v-if="festivalDays">{{ festivalDays }}</em></dd></div>
            <div><dt>⌖ &nbsp;장소</dt><dd>{{ festival.place }}</dd></div>
            <div><dt>◫ &nbsp;분류</dt><dd><b class="tag">{{ festival.category }}</b></dd></div>
          </dl>
          <RouterLink class="related-link" :to="`/board?festival_id=${festival.id}`">축제 이야기 보러 가기 →</RouterLink>
        </div>
      </section>

      <section class="intro-card section-card">
        <div class="intro-icon">🌱</div><div><h2>축제 소개 <span>●</span></h2><p>{{ festival.description }}</p></div>
        <RouterLink class="intro-cta" :to="`/board?festival_id=${festival.id}`">관련 게시글 보기 ↗</RouterLink>
      </section>

      <section class="location-section">
        <div class="map-panel section-card">
          <div class="section-heading"><h2>축제 위치 및 주변 정보</h2><p>지도 마커를 선택하면 장소 정보를 확인할 수 있어요.</p></div>
          <div v-if="typeof festival.lat === 'number' && typeof festival.lng === 'number'" ref="mapEl" class="map"></div>
          <p v-else class="empty-state">위치 좌표가 없어 지도를 표시할 수 없습니다.</p>
        </div>
        <aside class="selected-panel section-card">
          <p class="eyebrow">선택한 장소</p>
          <template v-if="selectedPlace">
            <div class="place-visual" :data-category="selectedPlace.category"><span>{{ categoryIcon(selectedPlace.category) }}</span></div>
            <div class="place-title"><span>{{ categoryIcon(selectedPlace.category) }}</span><h3>{{ selectedPlace.title }}</h3><b>{{ selectedPlace.category }}</b></div>
            <p class="place-copy">축제와 함께 둘러보기 좋은 주변 {{ selectedPlace.category }} 장소입니다.</p>
            <dl class="place-details"><div><dt>거리</dt><dd>{{ typeof selectedPlace.distanceKm === 'number' ? `${selectedPlace.distanceKm.toFixed(2)}km` : '-' }} <small>직선거리</small></dd></div><div><dt>주소</dt><dd>{{ selectedPlace.address }}</dd></div></dl>
          </template>
          <p v-else class="empty-state">선택할 수 있는 주변 장소가 없습니다.</p>
        </aside>
      </section>

      <section class="nearby-section section-card">
        <div class="nearby-head"><div><h2>주변 추천 장소 <span>🌿</span></h2><p>축제 반경 2km 이내 장소 · 거리는 직선거리 기준</p></div>
          <div class="filter-row"><button v-for="category in nearbyCategories" :key="category" type="button" class="filter-btn" :class="{ active: selectedNearbyCategory === category }" @click="selectedNearbyCategory = category">{{ category }}</button></div>
        </div>
        <div v-if="!nearbyLoading && filteredNearbyPlaces.length" class="nearby-grid">
          <button v-for="place in filteredNearbyPlaces" :key="place.id + place.title" type="button" class="place-card" :class="{ selected: selectedPlace?.id === place.id }" @click="selectPlace(place)">
            <div class="card-visual" :data-category="place.category"><span>{{ categoryIcon(place.category) }}</span><b>{{ place.category }}</b></div>
            <div class="card-body"><h3>{{ place.title }}</h3><p>{{ typeof place.distanceKm === 'number' ? `${place.distanceKm.toFixed(2)}km` : '거리 정보 없음' }}</p><small>{{ place.address }}</small><span class="map-link">⌖ 지도에서 보기</span></div>
          </button>
        </div>
        <p v-else-if="nearbyLoading" class="empty-state">주변 장소를 불러오는 중입니다.</p><p v-else-if="nearbyErrorMessage" class="empty-state">{{ nearbyErrorMessage }}</p><p v-else class="empty-state">조건에 맞는 주변 장소가 없습니다.</p>
      </section>
    </div>
  </main>
  <main v-else class="container detail-page"><section class="section-card status-card"><h2>{{ errorMessage || '축제를 찾을 수 없습니다.' }}</h2><RouterLink to="/festivals" class="related-link">목록으로</RouterLink></section></main>
</template>

<style scoped>
.detail-page{padding:22px 0 56px;background:radial-gradient(circle at 72% 2%,#f0f9e7 0,transparent 22%),var(--color-bg)}.breadcrumb{display:flex;align-items:center;gap:10px;margin:10px 4px 30px;color:#849087;font-size:13px}.breadcrumb strong{color:#445249}.hero-card{display:grid;grid-template-columns:1.02fr 1fr;min-height:410px;overflow:hidden;border:1px solid #e3e4d6;border-top:3px solid #69b62f;border-radius:28px;background:#fff;box-shadow:0 12px 34px rgba(64,83,49,.12)}.hero-image{position:relative;min-height:410px;overflow:hidden;background:linear-gradient(135deg,#dff0c8,#8dc5d7)}.hero-image img{width:100%;height:100%;object-fit:cover}.hero-image.placeholder{display:grid;place-items:center;color:#56724f;font-weight:800}.hero-tags{position:absolute;top:20px;left:20px;display:flex;gap:8px}.hero-tags span{padding:8px 14px;border-radius:999px;color:#fff;background:#64b433;box-shadow:0 4px 14px #0002;font-size:13px;font-weight:800}.hero-tags span+span{background:#3e9cdf}.hero-info{display:flex;flex-direction:column;justify-content:center;padding:clamp(28px,4vw,54px)}.title-row{display:flex;align-items:flex-start;gap:12px}h1{margin:0;color:#18221d;font-size:clamp(29px,3vw,42px);line-height:1.25;letter-spacing:-.045em}.star{color:#ffc853;font-size:25px}.festival-meta{display:grid;gap:22px;margin:34px 0 28px}.festival-meta>div{display:grid;grid-template-columns:94px 1fr;gap:14px}.festival-meta dt{color:#606b64;font-size:14px;font-weight:800}.festival-meta dd{margin:0;color:#252f29;font-size:15px;font-weight:650}.festival-meta em,.tag{display:inline-flex;margin-left:7px;padding:4px 9px;border-radius:99px;color:#54a929;background:#ecf8e4;font-size:12px;font-style:normal}.tag{margin:0;color:#347fc4;background:#e9f3ff}.related-link{display:inline-flex;align-items:center;align-self:flex-start;padding:11px 17px;border:1px solid #cce0be;border-radius:999px;color:#438f24;background:#f8fff4;font-size:13px;font-weight:800}.intro-card{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:22px;margin-top:24px;padding:24px 30px}.intro-icon{display:grid;width:72px;height:72px;place-items:center;border-radius:50%;background:#eaf7df;font-size:38px}.intro-card h2,.section-heading h2,.nearby-section h2{margin:0 0 6px;color:#243128;font-size:20px}.intro-card h2 span{color:#65b639;font-size:10px}.intro-card p,.section-heading p,.nearby-head p{margin:0;color:#667068;font-size:14px}.intro-cta{padding:13px 20px;border-radius:999px;color:#fff;background:linear-gradient(135deg,#66b735,#44a522);font-size:13px;font-weight:800}.location-section{display:grid;grid-template-columns:minmax(0,2.1fr) minmax(280px,1fr);gap:20px;margin-top:24px}.map-panel,.selected-panel{padding:22px}.section-heading{margin-bottom:14px}.map{width:100%;height:430px;overflow:hidden;border:1px solid #e2e7db;border-radius:18px}.eyebrow{margin:0 0 14px;color:#59645d;font-size:14px;font-weight:800}.place-visual,.card-visual{position:relative;display:grid;place-items:center;overflow:hidden;background:linear-gradient(150deg,#cce9f1,#eaf6d5)}.place-visual{height:154px;border-radius:15px}.place-visual:before,.card-visual:before{content:'';position:absolute;width:64%;height:45%;bottom:-18%;border-radius:50%;background:#53a63647;box-shadow:-70px 0 #53a6361f,70px -12px #53a63629}.place-visual>span,.card-visual>span{z-index:1;font-size:52px;filter:drop-shadow(0 6px 6px #32501e29)}[data-category="문화시설"]{background:linear-gradient(145deg,#e7e2f6,#dceff4)}[data-category="쇼핑"]{background:linear-gradient(145deg,#ffe9bf,#f3f0dc)}.place-title{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:8px;margin-top:16px}.place-title h3,.card-body h3{margin:0;color:#263029;font-size:17px}.place-title b{padding:4px 8px;border-radius:99px;color:#3b86cc;background:#eaf4ff;font-size:11px}.place-copy{color:#707972;font-size:12px}.place-details{margin:16px 0 0}.place-details div{display:grid;grid-template-columns:52px 1fr;gap:8px;padding:12px 0;border-top:1px solid #eceee7;font-size:12px}.place-details dt{color:#5d675f;font-weight:800}.place-details dd{margin:0;color:#303a33}.place-details small{color:#8b948e}.nearby-section{margin-top:24px;padding:24px}.nearby-head{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:18px}.filter-row{display:flex;flex-wrap:wrap;gap:7px}.filter-btn{padding:7px 12px;border:1px solid #d8e2d2;border-radius:999px;color:#5c6d61;background:#fff;font-size:12px;font-weight:800;cursor:pointer}.filter-btn.active{border-color:#5eae32;color:#fff;background:#5eae32}.nearby-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.place-card{overflow:hidden;padding:0;border:1px solid #e2e5dc;border-radius:17px;color:inherit;background:#fff;text-align:left;cursor:pointer;transition:.2s}.place-card:hover,.place-card.selected{transform:translateY(-3px);border-color:#8bc96a;box-shadow:0 9px 22px #48673421}.card-visual{height:118px}.card-visual>span{font-size:40px}.card-visual b{position:absolute;z-index:2;top:9px;left:9px;padding:4px 8px;border-radius:99px;color:#fff;background:#67b43c;font-size:10px}.card-body{display:grid;gap:6px;padding:13px}.card-body h3{overflow:hidden;font-size:14px;text-overflow:ellipsis;white-space:nowrap}.card-body p,.card-body small{margin:0;color:#737d76;font-size:11px}.card-body small{min-height:32px}.map-link{margin-top:5px;padding:7px;border:1px solid #dce5d6;border-radius:99px;color:#4a9b29;text-align:center;font-size:11px;font-weight:800}.empty-state{margin:0;padding:30px;border:1px dashed #d4ded0;border-radius:14px;color:#66776d;background:#f9fcf6;text-align:center}.status-card{display:flex;min-height:260px;align-items:center;justify-content:center;gap:14px;padding:30px;text-align:center}.status-card h2{margin:0;font-size:22px}.loader{width:22px;height:22px;border:3px solid #dcebd2;border-top-color:#5caf32;border-radius:50%;animation:spin .8s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}@media(max-width:1020px){.nearby-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:820px){.hero-card,.location-section{grid-template-columns:1fr}.hero-image{min-height:320px}.intro-card{grid-template-columns:auto 1fr}.intro-cta{grid-column:1/-1;text-align:center}.nearby-head{align-items:flex-start;flex-direction:column}}@media(max-width:560px){.detail-page{padding-top:10px}.breadcrumb{margin-bottom:18px}.hero-card{border-radius:20px}.hero-image{min-height:240px}.hero-info{padding:25px 20px}.festival-meta>div{grid-template-columns:75px 1fr}.intro-card{gap:12px;padding:18px}.intro-icon{width:52px;height:52px;font-size:27px}.map-panel,.selected-panel,.nearby-section{padding:16px}.map{height:330px}.nearby-grid{grid-template-columns:1fr}}
</style>

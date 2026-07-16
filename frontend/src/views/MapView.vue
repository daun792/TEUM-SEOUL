<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getPlaces } from '../services/placesApi'
import { getFestivalList } from '../services/festivalsApi'
import { placeTypeLabel } from '../utils/placeFilters'

L.Icon.Default.mergeOptions({ iconRetinaUrl: markerIcon2x, iconUrl: markerIcon, shadowUrl: markerShadow })
const mapRef = ref(null)
const selectedFilter = ref('전체')
const searchInput = ref('')
const searchQuery = ref('')
const filters = ['전체', '축제', '공연', '전시', '체험', '전통', '야외 행사', '관광지', '문화시설', '쇼핑']
const places = ref([])
const loading = ref(false)
const errorMessage = ref('')
const activePlaceId = ref('')
const visibleCount = ref(7)
const markerMap = new Map()
let map = null
let markers = []

function normalizedType(place) {
  const source = `${placeTypeLabel(place)} ${place.name}`
  if (/축제|페스티벌/.test(source)) return '축제'
  if (/공연|음악|콘서트|연극|뮤지컬/.test(source)) return '공연'
  if (/전시|미술|페어|박람회/.test(source)) return '전시'
  if (/체험|레포츠|워크숍/.test(source)) return '체험'
  if (/전통|한옥|궁/.test(source)) return '전통'
  if (/야외|공원|광장|분수/.test(source)) return '야외 행사'
  return placeTypeLabel(place)
}
const iconOf = (type) => ({ 전체:'▦',축제:'✿',공연:'♫',전시:'▣',체험:'♣',전통:'♜','야외 행사':'♟',관광지:'♜',문화시설:'▥',쇼핑:'♙' }[type] || '●')
const filteredPlaces = computed(() => places.value.filter((place) => {
  const matchesType = selectedFilter.value === '전체' || normalizedType(place) === selectedFilter.value
  const haystack = `${place.name} ${place.address || ''}`.toLowerCase()
  return matchesType && (!searchQuery.value || haystack.includes(searchQuery.value.toLowerCase()))
}))
const visiblePlaces = computed(() => filteredPlaces.value.slice(0, visibleCount.value))

const festivalFallback = (items) => items.filter((item) => typeof item.lat === 'number' && typeof item.lng === 'number').map((item) => ({
  id: `festival-${item.id}`, name: item.title, type: item.category || '축제공연행사',
  lat: item.lat, lng: item.lng, address: item.place, start: item.start, end: item.end, imageUrl: item.imageUrl,
}))

async function loadPlaces() {
  loading.value = true; errorMessage.value = ''
  try {
    const [page, festivals] = await Promise.all([getPlaces({ page: 1, size: 200 }), getFestivalList({ page: 1, size: 100 })])
    places.value = [...page.items.filter((p) => typeof p.lat === 'number' && typeof p.lng === 'number'), ...festivalFallback(festivals)]
  } catch (error) {
    try { places.value = festivalFallback(await getFestivalList({ page: 1, size: 100 })) }
    catch { places.value = []; errorMessage.value = error instanceof Error ? error.message : '장소 데이터를 불러오지 못했습니다.' }
  } finally { loading.value = false }
}
function submitSearch() { searchQuery.value = searchInput.value.trim(); visibleCount.value = 7 }
function focusPlace(place) {
  if (!map) return
  activePlaceId.value = place.id
  map.flyTo([place.lat, place.lng], 15, { duration: .65 })
  markerMap.get(place.id)?.openPopup()
}
function renderMarkers() {
  if (!map) return
  markers.forEach((marker) => marker.remove()); markerMap.clear()
  markers = filteredPlaces.value.map((place) => {
    const marker = L.marker([place.lat, place.lng]).addTo(map).bindPopup(`<strong>${place.name}</strong><br>${normalizedType(place)}<br>${place.address || ''}`)
    marker.on('click', () => { activePlaceId.value = place.id }); markerMap.set(place.id, marker); return marker
  })
  requestAnimationFrame(() => { map?.invalidateSize(); if (markers.length > 1) map.fitBounds(L.featureGroup(markers).getBounds(), { padding: [30, 30], maxZoom: 14 }) })
}
onMounted(async () => {
  await nextTick()
  map = L.map(mapRef.value).setView([37.5665, 126.978], 12)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors' }).addTo(map)
  await loadPlaces(); renderMarkers()
})
watch(filteredPlaces, () => { activePlaceId.value = ''; visibleCount.value = 7; renderMarkers() })
onBeforeUnmount(() => { map?.remove(); map = null })
</script>

<template>
  <main class="map-page">
    <section class="map-hero container">
      <div><h1>지도 탐색 <span>●</span></h1><p>서울 곳곳의 축제와 명소를 지도에서<br>유형별로 탐색해보세요.</p></div>
      <form class="search" @submit.prevent="submitSearch"><span>⌕</span><input v-model="searchInput" aria-label="장소 검색" placeholder="지역, 축제, 장소를 검색해보세요"><button type="submit">⌕</button></form>
      <div class="scene" aria-hidden="true"><span>🌳</span><span>🗼</span><span>🔎</span><span>🏙️</span></div>
    </section>

    <section class="container explorer section-card">
      <div class="filters"><button v-for="item in filters" :key="item" type="button" :class="{ active: selectedFilter === item }" @click="selectedFilter = item"><span>{{ iconOf(item) }}</span>{{ item }}</button></div>
      <div class="layout">
        <div ref="mapRef" class="map-box" aria-label="서울 지도"></div>
        <aside class="list-panel">
          <header><h2>표시 목록</h2><b>{{ filteredPlaces.length }}개</b></header>
          <ul v-if="visiblePlaces.length">
            <li v-for="place in visiblePlaces" :key="place.id">
              <button type="button" :class="{ active: activePlaceId === place.id }" @click="focusPlace(place)">
                <div class="place-image" :data-type="normalizedType(place)"><img v-if="place.imageUrl" :src="place.imageUrl" alt=""><span v-else>{{ iconOf(normalizedType(place)) }}</span></div>
                <div><p><i>{{ iconOf(normalizedType(place)) }}</i><strong>{{ place.name }}</strong><em>{{ normalizedType(place) }}</em></p><small>⌖ {{ place.address || '서울' }}</small><small v-if="place.start">◷ {{ place.start }}<template v-if="place.end"> ~ {{ place.end }}</template></small></div>
              </button>
            </li>
          </ul>
          <p v-else-if="loading" class="state">장소 데이터를 불러오는 중입니다...</p><p v-else class="state">{{ errorMessage || '검색 조건에 맞는 장소가 없습니다.' }}</p>
          <button v-if="visibleCount < filteredPlaces.length" class="more" type="button" @click="visibleCount += 7">더 많은 장소 보기⌄</button>
        </aside>
      </div>
    </section>
    <aside class="container tip"><span>🌱</span><p><strong>팁!</strong> 원하는 장소를 클릭하면 상세 정보를 확인할 수 있어요.</p><button type="button" aria-label="닫기">×</button></aside>
  </main>
</template>

<style scoped>
.map-page{min-height:calc(100vh - 76px);padding:24px 0 40px;background:radial-gradient(circle at 14% 8%,#eff9f3,transparent 26%),#fffcf7}.map-hero{display:grid;grid-template-columns:.72fr 1fr 1.18fr;align-items:center;min-height:165px}.map-hero h1{margin:0;color:#17231d;font-size:40px;letter-spacing:-.05em}.map-hero h1 span{color:#64ae3b;font-size:32px}.map-hero p{margin:13px 0 0;color:#4f5d55;font-size:14px;line-height:1.7}.search{z-index:2;display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:10px;padding:5px 6px 5px 17px;border:1px solid #dfdfd8;border-radius:99px;background:#fff;box-shadow:0 5px 16px #3b4f3520}.search input{min-width:0;border:0;outline:0;color:#38423c;background:transparent}.search button{width:48px;height:48px;border:0;border-radius:50%;color:#fff;background:linear-gradient(#75bd45,#55a62d);font-size:22px;cursor:pointer}.scene{align-self:end;display:flex;align-items:flex-end;justify-content:flex-end;gap:3px;height:150px;padding:0 20px 8px;border-radius:50% 50% 0 0;background:linear-gradient(180deg,transparent 40%,#dcecba 41%,#8dc15c 90%);font-size:50px}.scene span:nth-child(2){font-size:78px}.scene span:nth-child(3){font-size:61px}.scene span:nth-child(4){font-size:48px}.explorer{padding:20px;border-radius:24px}.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}.filters button{padding:10px 16px;border:0;border-radius:99px;color:#4d5b53;background:#fbfaf7;font-size:12px;font-weight:800;cursor:pointer}.filters button span{margin-right:7px;color:#62aa39}.filters button.active{color:#4f982b;background:#edf6e5}.layout{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(340px,1fr);gap:18px}.map-box{height:610px;overflow:hidden;border:1px solid #e3e5de;border-radius:18px}.list-panel{display:flex;height:610px;flex-direction:column;overflow:hidden;border:1px solid #e5e4de;border-radius:17px;background:#fff}.list-panel header{display:flex;align-items:center;gap:10px;padding:16px 18px;border-bottom:1px solid #ecebe6}.list-panel h2{margin:0;font-size:16px}.list-panel header b{padding:3px 8px;border-radius:99px;color:#66a73e;background:#eef7e7;font-size:11px}.list-panel ul{flex:1;margin:0;padding:0;overflow:auto;list-style:none}.list-panel li{border-bottom:1px solid #eeede8}.list-panel li>button{display:grid;width:100%;grid-template-columns:82px 1fr;gap:12px;padding:9px 14px;border:0;background:#fff;text-align:left;cursor:pointer}.list-panel li>button:hover,.list-panel li>button.active{background:#f7fbf4}.place-image{display:grid;width:82px;height:70px;place-items:center;overflow:hidden;border-radius:10px;background:linear-gradient(145deg,#d8ecf2,#e7f2d9);font-size:31px}.place-image img{width:100%;height:100%;object-fit:cover}.place-image[data-type="전시"],.place-image[data-type="문화시설"]{background:#ebe4f7}.place-image[data-type="쇼핑"]{background:#ffebc8}.list-panel li>button>div+div{display:flex;min-width:0;flex-direction:column;justify-content:center;gap:5px}.list-panel p{display:flex;align-items:center;gap:7px;margin:0}.list-panel p i{color:#69ac44;font-style:normal}.list-panel p strong{overflow:hidden;font-size:13px;text-overflow:ellipsis;white-space:nowrap}.list-panel p em{padding:3px 7px;border-radius:99px;color:#477fc4;background:#e9f2ff;font-size:9px;font-style:normal}.list-panel small{overflow:hidden;color:#778079;font-size:10px;text-overflow:ellipsis;white-space:nowrap}.state{margin:auto!important;color:#758078;text-align:center}.more{margin:12px auto;padding:9px 48px;border:1px solid #e0ded6;border-radius:99px;background:#fff;font-size:11px;font-weight:800;cursor:pointer}.tip{display:flex;align-items:center;gap:14px;margin-top:15px;padding:11px 24px;border:1px solid #e2e8da;border-radius:15px;background:linear-gradient(90deg,#f8fff3,#fff)}.tip>span{font-size:36px}.tip p{margin:0;font-size:12px}.tip p strong{font-size:14px}.tip button{margin-left:auto;border:0;background:transparent;font-size:22px;cursor:pointer}
@media(max-width:1020px){.map-hero{grid-template-columns:1fr 1.5fr}.scene{display:none}.layout{grid-template-columns:1fr}.map-box{height:480px}.list-panel{height:540px}}@media(max-width:680px){.map-page{padding-top:12px}.map-hero{grid-template-columns:1fr;gap:16px;padding-bottom:20px}.map-hero h1{font-size:32px}.explorer{padding:12px}.filters{flex-wrap:nowrap;overflow-x:auto}.filters button{flex:none}.map-box{height:360px}.list-panel{height:500px}}
</style>

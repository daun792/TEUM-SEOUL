<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { getFestivalById, getFestivalNearby } from '../services/festivalsApi'
import { getPlaces } from '../services/placesApi'
L.Icon.Default.mergeOptions({ iconRetinaUrl:markerIcon2x,iconUrl:markerIcon,shadowUrl:markerShadow })
const route=useRoute(),mapEl=ref(null),festival=ref(null),loading=ref(true),errorMessage=ref('')
const nearbyPlaces=ref([]),nearbyLoading=ref(false),nearbyErrorMessage=ref(''),selectedNearbyCategory=ref('전체'),selectedPlace=ref(null)
const nearbyCategories=['전체','관광지','문화시설','쇼핑']
let map=null,festivalMarker=null,nearbyMarkers=[]
const filteredNearbyPlaces=computed(()=>selectedNearbyCategory.value==='전체'?nearbyPlaces.value:nearbyPlaces.value.filter(p=>p.category===selectedNearbyCategory.value))
const categoryIcon=c=>({관광지:'🌳',문화시설:'🏛️',쇼핑:'🛍️'}[c]||'📍')
function distanceKm(a,b,c,d){const r=x=>x*Math.PI/180,x=r(c-a),y=r(d-b),z=Math.sin(x/2)**2+Math.cos(r(a))*Math.cos(r(c))*Math.sin(y/2)**2;return 6371*2*Math.atan2(Math.sqrt(z),Math.sqrt(1-z))}
function selectPlace(place){selectedPlace.value=place;if(map&&typeof place.lat==='number'&&typeof place.lng==='number'){map.flyTo([place.lat,place.lng],16);nearbyMarkers.find(m=>m.placeId===place.id)?.openPopup()}}
function renderMap(){
  if(!festival.value||!mapEl.value)return
  const{lat,lng,name}=festival.value;if(typeof lat!=='number'||typeof lng!=='number')return
  if(!map){map=L.map(mapEl.value).setView([lat,lng],15);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OpenStreetMap contributors'}).addTo(map)}
  festivalMarker?.remove();festivalMarker=L.marker([lat,lng]).addTo(map).bindPopup(name)
  nearbyMarkers.forEach(m=>m.remove())
  nearbyMarkers=filteredNearbyPlaces.value.filter(p=>typeof p.lat==='number'&&typeof p.lng==='number').map(p=>{const m=L.marker([p.lat,p.lng]).addTo(map).bindPopup(`<strong>${p.title}</strong><br>${p.category}<br>${p.distanceKm?.toFixed(2)??'-'}km`);m.placeId=p.id;m.on('click',()=>selectedPlace.value=p);return m})
  const all=[festivalMarker,...nearbyMarkers];if(all.length>1)map.fitBounds(L.featureGroup(all).getBounds(),{padding:[34,34],maxZoom:15});else map.setView([lat,lng],15)
  requestAnimationFrame(()=>map?.invalidateSize())
}
async function loadNearbyPlaces(){
  nearbyLoading.value=true;nearbyErrorMessage.value=''
  try{
    let items=(await getFestivalNearby(route.params.id,{radiusKm:5,categories:['관광지','문화시설','쇼핑'],limit:12})).items
    if(!items.length&&typeof festival.value.lat==='number'&&typeof festival.value.lng==='number'){
      const page=await getPlaces({page:1,size:200})
      items=page.items.filter(p=>['관광지','문화시설','쇼핑'].includes(p.type)&&typeof p.lat==='number'&&typeof p.lng==='number')
        .map(p=>({...p,title:p.title||p.name,category:p.type,distanceKm:distanceKm(festival.value.lat,festival.value.lng,p.lat,p.lng)}))
        .filter(p=>p.distanceKm<=5).sort((a,b)=>a.distanceKm-b.distanceKm).slice(0,12)
    }
    nearbyPlaces.value=items;selectedPlace.value=items[0]||null
  }catch(e){nearbyPlaces.value=[];selectedPlace.value=null;nearbyErrorMessage.value=e instanceof Error?e.message:'주변 장소를 불러오지 못했습니다.'}
  finally{nearbyLoading.value=false}
}
async function loadFestival(){loading.value=true;try{festival.value=await getFestivalById(route.params.id);await loadNearbyPlaces()}catch(e){festival.value=null;errorMessage.value=e instanceof Error?e.message:'축제 정보를 불러오지 못했습니다.'}finally{loading.value=false}await nextTick();renderMap()}
onMounted(loadFestival);watch(()=>route.params.id,loadFestival);watch(filteredNearbyPlaces,async()=>{await nextTick();renderMap()})
onBeforeUnmount(()=>{map?.remove();map=null})
</script>
<template>
  <main v-if="loading" class="container detail-page"><section class="section-card status-card">축제 정보를 불러오는 중입니다.</section></main>
  <main v-else-if="festival" class="detail-page"><div class="container">
    <nav class="breadcrumb"><RouterLink to="/">홈</RouterLink><span>›</span><RouterLink to="/festivals">축제 캘린더</RouterLink><span>›</span><strong>축제 상세</strong></nav>
    <section class="hero-card">
      <div class="hero-image" :class="{placeholder:!festival.imageUrl}"><img v-if="festival.imageUrl" :src="festival.imageUrl" :alt="festival.name"><span v-else>이미지 준비중</span><div class="hero-tags"><span>축제</span><span>{{ festival.category }}</span></div></div>
      <div class="hero-info"><h1>{{ festival.name }}</h1><dl><div><dt>▣ 기간</dt><dd>{{ festival.period }}</dd></div><div><dt>⌖ 장소</dt><dd>{{ festival.place }}</dd></div><div><dt>◫ 분류</dt><dd>{{ festival.category }}</dd></div></dl><RouterLink class="related-link" :to="`/board?festival_id=${festival.id}`">축제 이야기 보러 가기 →</RouterLink></div>
    </section>
    <section class="location-section">
      <div class="map-panel section-card"><header><h2>축제 위치 및 주변 정보</h2><p>축제와 주변 추천 장소를 지도에서 함께 확인할 수 있어요.</p></header><div v-if="typeof festival.lat==='number'&&typeof festival.lng==='number'" ref="mapEl" class="map"></div><p v-else class="empty">위치 좌표가 없어 지도를 표시할 수 없습니다.</p></div>
      <aside class="selected-panel section-card"><h3>선택한 장소</h3><template v-if="selectedPlace"><div class="place-visual" :data-category="selectedPlace.category">{{ categoryIcon(selectedPlace.category) }}</div><h2>{{ selectedPlace.title }} <b>{{ selectedPlace.category }}</b></h2><p>{{ selectedPlace.address }}</p><strong>{{ selectedPlace.distanceKm?.toFixed(2)??'-' }}km · 직선거리</strong></template><p v-else class="empty">선택할 수 있는 주변 장소가 없습니다.</p></aside>
    </section>
    <section class="nearby-section section-card"><div class="nearby-head"><div><h2>주변 추천 장소 🌿</h2><p>축제 반경 5km 이내 장소</p></div><div class="filters"><button v-for="c in nearbyCategories" :key="c" :class="{active:selectedNearbyCategory===c}" @click="selectedNearbyCategory=c">{{ c }}</button></div></div>
      <div v-if="!nearbyLoading&&filteredNearbyPlaces.length" class="nearby-grid"><button v-for="place in filteredNearbyPlaces" :key="place.id" class="place-card" :class="{selected:selectedPlace?.id===place.id}" @click="selectPlace(place)"><div class="card-visual" :data-category="place.category">{{ categoryIcon(place.category) }}<b>{{ place.category }}</b></div><h3>{{ place.title }}</h3><p>{{ place.distanceKm?.toFixed(2)??'-' }}km</p><small>{{ place.address }}</small><span>⌖ 지도에서 보기</span></button></div>
      <p v-else-if="nearbyLoading" class="empty">주변 장소를 불러오는 중입니다.</p><p v-else class="empty">{{ nearbyErrorMessage||'반경 5km 안에 추천 장소가 없습니다.' }}</p>
    </section>
  </div></main>
  <main v-else class="container detail-page"><section class="section-card status-card">{{ errorMessage||'축제를 찾을 수 없습니다.' }}</section></main>
</template>
<style scoped>
.detail-page{padding:22px 0 56px;background:radial-gradient(circle at 72% 2%,#f0f9e7,transparent 22%),var(--color-bg)}.breadcrumb{display:flex;gap:10px;margin:10px 4px 30px;color:#849087;font-size:13px}.hero-card{display:grid;grid-template-columns:1.02fr 1fr;min-height:400px;overflow:hidden;border:1px solid #e3e4d6;border-top:3px solid #69b62f;border-radius:28px;background:#fff;box-shadow:0 12px 34px #4053311f}.hero-image{position:relative;min-height:400px;background:#eaf4df}.hero-image img{width:100%;height:100%;object-fit:cover}.hero-image.placeholder{display:grid;place-items:center}.hero-tags{position:absolute;top:20px;left:20px;display:flex;gap:8px}.hero-tags span{padding:8px 13px;border-radius:99px;color:#fff;background:#64b433;font-size:12px;font-weight:800}.hero-tags span+span{background:#3e9cdf}.hero-info{display:flex;flex-direction:column;justify-content:center;padding:45px}.hero-info h1{margin:0;color:#18221d;font-size:38px;letter-spacing:-.045em}.hero-info dl{display:grid;gap:22px;margin:34px 0}.hero-info dl>div{display:grid;grid-template-columns:85px 1fr}.hero-info dt{color:#657067;font-size:13px;font-weight:800}.hero-info dd{margin:0;font-size:14px}.related-link{align-self:flex-start;padding:11px 17px;border:1px solid #cce0be;border-radius:99px;color:#438f24;background:#f8fff4;font-size:13px;font-weight:800}.location-section{display:grid;grid-template-columns:minmax(0,2.1fr) minmax(280px,1fr);gap:20px;margin-top:24px}.map-panel,.selected-panel,.nearby-section{padding:22px}.map-panel header{margin-bottom:14px}.map-panel h2,.nearby-head h2{margin:0 0 5px;font-size:20px}.map-panel header p,.nearby-head p{margin:0;color:#69746c;font-size:13px}.map{height:430px;border-radius:18px}.selected-panel h3{margin:0 0 14px;font-size:14px}.place-visual,.card-visual{display:grid;place-items:center;border-radius:15px;background:linear-gradient(145deg,#cde8f1,#e6f2d4);font-size:49px}.place-visual{height:155px}.selected-panel h2{font-size:17px}.selected-panel h2 b,.card-visual b{padding:3px 7px;border-radius:99px;color:#397fc3;background:#e8f2ff;font-size:10px}.selected-panel p{color:#68736b;font-size:12px}.selected-panel strong{font-size:12px}.nearby-section{margin-top:24px}.nearby-head{display:flex;align-items:flex-end;justify-content:space-between;gap:15px;margin-bottom:18px}.filters{display:flex;gap:7px}.filters button{padding:7px 12px;border:1px solid #d8e2d2;border-radius:99px;background:#fff;font-size:11px;font-weight:800;cursor:pointer}.filters button.active{color:#fff;background:#5eae32}.nearby-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.place-card{display:grid;gap:6px;padding:0 0 13px;overflow:hidden;border:1px solid #e2e5dc;border-radius:17px;background:#fff;text-align:left;cursor:pointer}.place-card.selected{border-color:#71b64a;box-shadow:0 8px 20px #48673420}.card-visual{position:relative;height:115px;border-radius:0}.card-visual b{position:absolute;top:8px;left:8px}.place-card h3,.place-card p,.place-card small,.place-card>span{margin:0 12px}.place-card h3{overflow:hidden;font-size:14px;text-overflow:ellipsis;white-space:nowrap}.place-card p,.place-card small{color:#727c75;font-size:11px}.place-card small{min-height:30px}.place-card>span{padding:6px;border:1px solid #dce5d6;border-radius:99px;color:#4a9b29;text-align:center;font-size:11px;font-weight:800}.empty,.status-card{padding:30px;color:#68786e;text-align:center}.status-card{margin-top:30px}@media(max-width:900px){.hero-card,.location-section{grid-template-columns:1fr}.nearby-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.hero-info{padding:25px 20px}.hero-info h1{font-size:29px}.nearby-head{align-items:flex-start;flex-direction:column}.filters{overflow-x:auto;max-width:100%}.nearby-grid{grid-template-columns:1fr}.map{height:340px}}
</style>

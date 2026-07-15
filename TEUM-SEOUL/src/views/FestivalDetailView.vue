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
  <section v-if="festival" class="detail">
    <h2>{{ festival.name }}</h2>
    <img :src="festival.imageUrl" :alt="festival.name" />
    <p><strong>기간:</strong> {{ festival.period }}</p>
    <p><strong>장소:</strong> {{ festival.place }}</p>
    <p><strong>설명:</strong> {{ festival.description }}</p>

    <h3>축제 위치</h3>
    <div ref="mapEl" class="map"></div>
  </section>

  <section v-else>
    <h2>축제를 찾을 수 없습니다.</h2>
  </section>
</template>

<style scoped>
.detail {
  max-width: 900px;
}
img {
  width: 100%;
  border-radius: 10px;
  margin: 10px 0 16px;
}
.map {
  width: 100%;
  height: 360px;
  border-radius: 10px;
  margin-top: 12px;
}
</style>
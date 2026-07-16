<script setup>
import { computed, onMounted, ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import { useRouter } from 'vue-router'
import { getFestivalList } from '../services/festivalsApi'

const router = useRouter()
const festivals = ref([])
const loading = ref(true)
const errorMessage = ref('')
const selectedDate = ref(new Date().toISOString().slice(0, 10))
const selectedType = ref('전체')
const categories = ['전체', '공연', '전시', '체험', '축제', '기타']

function typeOf(festival) {
  const text = `${festival.title} ${festival.category}`
  if (/공연|콘서트|음악|연극|뮤지컬|무용|국악/.test(text)) return '공연'
  if (/전시|미술|박람회|페어|아트/.test(text)) return '전시'
  if (/체험|워크숍|교육|만들기/.test(text)) return '체험'
  if (/축제|페스티벌|행사|마켓/.test(text)) return '축제'
  return '기타'
}
const typeIcon = (type) => ({ 공연: '♫', 전시: '▣', 체험: '♙', 축제: '✿', 기타: '●' }[type] || '✿')
const filteredFestivals = computed(() => selectedType.value === '전체'
  ? festivals.value : festivals.value.filter((festival) => typeOf(festival) === selectedType.value))
const monthStart = new Date()
monthStart.setDate(1)
const monthEnd = new Date(monthStart.getFullYear(), monthStart.getMonth() + 1, 0)
const toLocalDate = (date) => new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10)
const monthStartValue = toLocalDate(monthStart)
const monthEndValue = toLocalDate(monthEnd)

const events = computed(() => {
  const onePerDay = []
  const cursor = new Date(monthStart)
  while (cursor <= monthEnd) {
    const date = toLocalDate(cursor)
    const festival = filteredFestivals.value.find((item) => item.start && item.start <= date && (item.end || item.start) >= date)
    if (festival) onePerDay.push({
      id: festival.id, title: festival.title, start: date, allDay: true,
      extendedProps: { type: typeOf(festival) },
    })
    cursor.setDate(cursor.getDate() + 1)
  }
  return onePerDay
})
function includesDate(festival) {
  if (!festival.start) return false
  return festival.start <= selectedDate.value && (festival.end || festival.start) >= selectedDate.value
}
const selectedFestivals = computed(() => filteredFestivals.value.filter(includesDate).slice(0, 1))
const undatedFestivals = computed(() => filteredFestivals.value.filter((festival) => !festival.start && !festival.end))
const selectedDateLabel = computed(() => {
  const date = new Date(`${selectedDate.value}T00:00:00`)
  return new Intl.DateTimeFormat('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' }).format(date)
})

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin], initialView: 'dayGridMonth', locale: koLocale,
  headerToolbar: { left: 'prev', center: 'title', right: 'next' },
  height: 'auto', fixedWeekCount: false, dayMaxEvents: 3, events: events.value,
  dateClick(info) { selectedDate.value = info.dateStr },
  eventClick(info) { router.push(`/festivals/${info.event.id}`) },
  dayCellClassNames(info) {
    const local = new Date(info.date.getTime() - info.date.getTimezoneOffset() * 60000).toISOString().slice(0, 10)
    return local === selectedDate.value ? ['selected-day'] : []
  },
  eventContent(info) { return { html: `<span class="event-dot type-${info.event.extendedProps.type}"></span><span class="event-name">${info.event.title}</span>` } },
}))

onMounted(async () => {
  try { festivals.value = await getFestivalList({ page: 1, size: 100, startDate: monthStartValue, endDate: monthEndValue }) }
  catch (error) { errorMessage.value = error instanceof Error ? error.message : '축제 데이터를 불러오지 못했습니다.' }
  finally { loading.value = false }
})
</script>

<template>
  <main class="calendar-page">
    <section class="calendar-hero container">
      <div><h1><span>🗓️</span> 축제 캘린더 <em>♣</em></h1><p>매일 열리는 서울의 축제와 행사 정보를 확인하고, 일정을 계획해 보세요.</p></div>
      <div class="hero-scene" aria-hidden="true"><span>🏯</span><span>🌳</span><span>🎪</span><span>🏙️</span><span>🚐</span></div>
    </section>

    <section v-if="loading" class="container state-card section-card">축제 데이터를 불러오는 중입니다...</section>
    <section v-else-if="errorMessage" class="container state-card section-card">{{ errorMessage }}</section>
    <template v-else>
      <div class="container calendar-layout">
        <section class="calendar-panel section-card">
          <FullCalendar :options="calendarOptions" />
          <div class="type-filter" aria-label="축제 유형 필터">
            <button v-for="type in categories" :key="type" type="button" :class="{ active: selectedType === type }" @click="selectedType = type">
              <span>{{ type === '전체' ? '전체' : typeIcon(type) }}</span>{{ type === '전체' ? '' : type }}
            </button>
          </div>
        </section>

        <aside class="selection-panel section-card">
          <header><h2>선택한 날짜의 축제 <span>♣</span></h2><strong>{{ selectedDateLabel }}</strong></header>
          <ul v-if="selectedFestivals.length">
            <li v-for="festival in selectedFestivals.slice(0, 5)" :key="festival.id" @click="router.push(`/festivals/${festival.id}`)">
              <div class="thumb" :class="{ empty: !festival.imageUrl }"><img v-if="festival.imageUrl" :src="festival.imageUrl" alt="" /><span v-else>{{ typeIcon(typeOf(festival)) }}</span></div>
              <div><p><b :data-type="typeOf(festival)">{{ typeOf(festival) }}</b><strong>{{ festival.title }}</strong></p><small>{{ festival.place }}</small><small>{{ festival.period }}</small></div>
            </li>
          </ul>
          <p v-else class="empty-day">선택한 날짜에 진행 중인 축제가 없습니다.</p>
          <button class="day-button" type="button" @click="selectedType = '전체'">{{ selectedDate.slice(5).replace('-', '월 ') }}일 전체 축제 보기 ›</button>
        </aside>
      </div>

      <section v-if="undatedFestivals.length" class="container undated-panel section-card">
        <header><h2>날짜 정보가 없는 축제 <span>♣</span></h2><p>정확한 날짜가 추가로 공지될 예정인 축제입니다.</p></header>
        <ul><li v-for="festival in undatedFestivals.slice(0, 10)" :key="festival.id" @click="router.push(`/festivals/${festival.id}`)"><span>{{ typeIcon(typeOf(festival)) }}</span><div><strong>{{ festival.title }}</strong><small>{{ festival.place }}</small></div></li></ul>
      </section>
    </template>
  </main>
</template>

<style scoped>
.calendar-page{min-height:calc(100vh - 76px);padding:26px 0 52px;background:radial-gradient(circle at 80% 8%,#eff8df 0,transparent 25%),#fffcf6}.calendar-hero{display:grid;grid-template-columns:.75fr 1.25fr;align-items:center;min-height:135px}.calendar-hero h1{margin:0;color:#17251e;font-size:36px;letter-spacing:-.05em}.calendar-hero h1>span{font-size:31px}.calendar-hero h1 em,.selection-panel h2 span,.undated-panel h2 span{color:#62af35;font-size:15px;font-style:normal}.calendar-hero p{margin:12px 0 0;color:#4f5e55;font-size:14px}.hero-scene{display:flex;align-items:flex-end;justify-content:center;gap:10px;height:130px;padding:15px 25px 0;border-radius:50% 50% 12px 12px;background:linear-gradient(180deg,transparent 20%,#dff1bd 21%,#9bcd69 82%,#70ac45 83%);font-size:52px}.hero-scene span:nth-child(2){font-size:44px}.hero-scene span:nth-child(4){font-size:48px}.hero-scene span:nth-child(5){font-size:39px}.calendar-layout{display:grid;grid-template-columns:minmax(0,1.75fr) minmax(320px,.95fr);gap:18px}.calendar-panel,.selection-panel,.undated-panel{padding:20px;border-radius:25px}.calendar-panel{overflow:hidden}.type-filter{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.type-filter button{min-width:82px;padding:9px 16px;border:1px solid #e5e2da;border-radius:99px;color:#46534b;background:#fff;font-weight:750;cursor:pointer}.type-filter button span{margin-right:6px;color:#6db43e}.type-filter button.active{border-color:#63ae32;color:#fff;background:linear-gradient(#75be43,#55a626)}.type-filter button.active span{color:#fff}.selection-panel{display:flex;min-height:590px;flex-direction:column}.selection-panel header h2{margin:0 0 9px;font-size:19px}.selection-panel header>strong{font-size:15px}.selection-panel ul,.undated-panel ul{display:grid;gap:10px;margin:18px 0;padding:0;list-style:none}.selection-panel li{display:grid;grid-template-columns:104px 1fr;gap:12px;padding:0;border:1px solid #e7e4dc;border-radius:14px;overflow:hidden;background:#fff;box-shadow:0 3px 10px #463b2510;cursor:pointer}.thumb{height:92px;background:#e8f4d8}.thumb img{width:100%;height:100%;object-fit:cover}.thumb.empty{display:grid;place-items:center;font-size:34px}.selection-panel li>div+div{display:flex;min-width:0;flex-direction:column;justify-content:center;gap:3px;padding:8px 10px 8px 0}.selection-panel li p{display:flex;align-items:center;gap:8px;margin:0}.selection-panel li p b{padding:3px 7px;border-radius:99px;color:#fff;background:#7a70d5;font-size:10px}.selection-panel li p b[data-type="전시"]{background:#ec7b42}.selection-panel li p b[data-type="체험"]{background:#76b64e}.selection-panel li p b[data-type="축제"]{background:#e18d3e}.selection-panel li strong{overflow:hidden;color:#283229;font-size:13px;text-overflow:ellipsis;white-space:nowrap}.selection-panel li small{overflow:hidden;color:#69736c;font-size:11px;text-overflow:ellipsis;white-space:nowrap}.empty-day{margin:auto;padding:30px;color:#788079;text-align:center}.day-button{margin-top:auto;padding:12px;border:1px solid #e2dfd6;border-radius:13px;background:#fff;font-weight:800;cursor:pointer}.undated-panel{margin-top:18px}.undated-panel header h2{margin:0;font-size:18px}.undated-panel header p{margin:3px 0 0;color:#7a817b;font-size:11px}.undated-panel ul{grid-template-columns:1fr 1fr}.undated-panel li{display:grid;grid-template-columns:48px 1fr;align-items:center;gap:10px;padding:8px 14px;border:1px solid #e6e2d8;border-radius:12px;background:#fffdfa;cursor:pointer}.undated-panel li>span{display:grid;width:38px;height:38px;place-items:center;border-radius:12px;background:#edf5e3;font-size:22px}.undated-panel li div{display:grid}.undated-panel li strong{font-size:12px}.undated-panel li small{overflow:hidden;color:#737b75;font-size:10px;text-overflow:ellipsis;white-space:nowrap}.state-card{padding:50px;text-align:center}
:deep(.fc .fc-toolbar-title){font-size:25px;letter-spacing:-.04em}:deep(.fc .fc-button-primary){border:0;border-radius:7px;background:#2f4051}:deep(.fc-theme-standard td),:deep(.fc-theme-standard th){border-color:#e7e5de}:deep(.fc .fc-col-header-cell-cushion){padding:9px;color:#303730;font-size:12px}:deep(.fc .fc-daygrid-day){height:91px}:deep(.fc .fc-daygrid-day-number){padding:9px;color:#313832;font-size:12px;font-weight:800}:deep(.fc .fc-daygrid-day.selected-day){background:#fffbe7;box-shadow:inset 0 0 0 2px #80b84b}:deep(.fc .fc-day-today){background:#f4faee!important}:deep(.fc-event){border:0;background:transparent;cursor:pointer}:deep(.fc-event-main){display:flex;align-items:center;color:#334038}:deep(.event-dot){width:7px;height:7px;flex:none;border-radius:50%;background:#7b70d3}:deep(.type-전시){background:#ef7d3d}:deep(.type-체험){background:#62b13c}:deep(.type-축제){background:#35a4dc}:deep(.type-기타){background:#aaa4c7}:deep(.event-name){overflow:hidden;margin-left:4px;font-size:9px;text-overflow:ellipsis;white-space:nowrap}
@media(max-width:980px){.calendar-hero{grid-template-columns:1fr}.hero-scene{display:none}.calendar-layout{grid-template-columns:1fr}.selection-panel{min-height:auto}}@media(max-width:620px){.calendar-page{padding-top:16px}.calendar-hero{min-height:100px}.calendar-hero h1{font-size:29px}.calendar-panel,.selection-panel,.undated-panel{padding:14px}.undated-panel ul{grid-template-columns:1fr}:deep(.fc .fc-toolbar-title){font-size:19px}:deep(.fc .fc-daygrid-day){height:72px}.event-name{display:none}}
</style>

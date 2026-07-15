<script setup>
import { computed, onMounted, ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import { useRouter } from 'vue-router'
import heroImage from '../assets/hero-seoul-isometric.webp'
import { getFestivalList } from '../services/festivalsApi'
import { getFestivalTags } from '../utils/festivalTags'

const router = useRouter()
const festivals = ref([])
const loading = ref(true)
const errorMessage = ref('')
const selectedDate = ref(new Date().toISOString().slice(0, 10))

const weekdays = ['일', '월', '화', '수', '목', '금', '토']
const iconTokens = ['🎪', '🎨', '🎵', '🌿', '🧪', '🏛️', '🛍️', '🎭']
const legendChips = [
  { label: '전체', key: '전체', color: '#6fb336' },
  { label: '공연', key: '공연', color: '#6b5bd1' },
  { label: '전시', key: '전시', color: '#ff8a24' },
  { label: '체험', key: '체험', color: '#69b62f' },
  { label: '축제', key: '축제', color: '#f25752' },
  { label: '기타', key: '기타', color: '#b8b8c4' },
]

function includesSelectedDate(festival) {
  if (!festival.start) return false
  const selected = new Date(`${selectedDate.value}T00:00:00`)
  const start = new Date(`${festival.start}T00:00:00`)
  const end = new Date(`${festival.end || festival.start}T23:59:59`)
  return start <= selected && selected <= end
}

function classifyFestival(festival) {
  const tags = getFestivalTags(festival)
  const title = festival.title || ''

  if (tags.includes('공연')) return '공연'
  if (tags.includes('전시')) return '전시'
  if (/체험|투어|워크숍|캠프/.test(title)) return '체험'
  if (/축제|페스티벌|행사|마당/.test(title)) return '축제'
  return '기타'
}

function categoryColor(category) {
  const item = legendChips.find((chip) => chip.key === category)
  return item ? item.color : '#b8b8c4'
}

function formatSelectedDateLabel(value) {
  const date = new Date(`${value}T00:00:00`)
  if (Number.isNaN(date.getTime())) return value
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const weekday = weekdays[date.getDay()]
  return `${year}.${month}.${day} (${weekday})`
}

const selectedDateLabel = computed(() => formatSelectedDateLabel(selectedDate.value))

const events = computed(() =>
  festivals.value
    .filter((festival) => festival.start)
    .map((festival) => {
      const category = classifyFestival(festival)
      return {
        id: festival.id,
        title: festival.title,
        start: festival.start,
        end: festival.end || festival.start,
        allDay: true,
        display: 'list-item',
        color: categoryColor(category),
      }
    }),
)

const selectedFestivals = computed(() =>
  festivals.value
    .filter((festival) => includesSelectedDate(festival))
    .map((festival) => ({
      ...festival,
      categoryLabel: classifyFestival(festival),
      isFree: /무료/.test(festival.title || ''),
    })),
)

const undatedFestivals = computed(() => festivals.value.filter((festival) => !festival.start && !festival.end))

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  initialDate: selectedDate.value,
  locale: koLocale,
  height: 'auto',
  fixedWeekCount: true,
  showNonCurrentDates: true,
  headerToolbar: {
    left: 'prev',
    center: 'title',
    right: 'next',
  },
  events: events.value,
  dateClick: (info) => {
    selectedDate.value = info.dateStr
  },
  eventClick: (info) => {
    router.push(`/festivals/${info.event.id}`)
  },
  dayCellClassNames: (info) => (info.date.toISOString().slice(0, 10) === selectedDate.value ? ['selected-day'] : []),
}))

onMounted(async () => {
  try {
    festivals.value = await getFestivalList({ page: 1, size: 300 })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '축제 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="container festival-calendar-page">
    <section class="hero section-card">
      <div class="hero-copy">
        <p class="kicker">📅</p>
        <h1>축제 캘린더</h1>
        <p>매일 열리는 서울의 축제와 행사 정보를 확인하고, 일정을 계획해 보세요.</p>
      </div>
      <div class="hero-art" :class="{ 'asset-placeholder': !heroImage }">
        <img v-if="heroImage" :src="heroImage" alt="서울 축제 캘린더 배너" />
      </div>
    </section>

    <section v-if="loading" class="state-box">축제 데이터를 불러오는 중입니다...</section>
    <section v-else-if="errorMessage" class="state-box">{{ errorMessage }}</section>
    <section v-else-if="!festivals.length" class="state-box">표시할 축제 데이터가 없습니다.</section>

    <section v-else class="calendar-layout">
      <article class="calendar-panel section-card" aria-label="월간 축제 캘린더">
        <FullCalendar :options="calendarOptions" />

        <div class="legend-row" aria-label="축제 범례">
          <button
            v-for="item in legendChips"
            :key="item.key"
            type="button"
            class="legend-chip"
            :style="{ '--chip-color': item.color }"
          >
            <span class="dot" aria-hidden="true"></span>
            {{ item.label }}
          </button>
        </div>
      </article>

      <aside class="day-panel section-card" aria-label="선택 날짜 축제 목록">
        <h2>선택한 날짜의 축제</h2>
        <p class="selected-date">{{ selectedDateLabel }}</p>

        <ul v-if="selectedFestivals.length" class="festival-cards">
          <li
            v-for="festival in selectedFestivals"
            :key="festival.id"
            class="festival-card"
            @click="router.push(`/festivals/${festival.id}`)"
          >
            <div class="thumb" :class="{ 'asset-placeholder': !festival.imageUrl }">
              <img v-if="festival.imageUrl" :src="festival.imageUrl" :alt="festival.title" />
            </div>
            <div class="card-body">
              <div class="card-head">
                <span class="badge" :style="{ '--badge-color': categoryColor(festival.categoryLabel) }">{{ festival.categoryLabel }}</span>
                <button type="button" class="bookmark" aria-label="북마크">⟡</button>
              </div>
              <strong>{{ festival.title }}</strong>
              <span class="meta">{{ festival.period }}</span>
              <span v-if="festival.isFree" class="free-chip">무료</span>
            </div>
          </li>
        </ul>
        <p v-else class="empty-day">선택한 날짜에 진행 중인 축제가 없습니다.</p>

        <button type="button" class="all-btn">
          {{ selectedDateLabel.split(' ')[0] }} 전체 축제 보기
        </button>
      </aside>
    </section>

    <section v-if="!loading && !errorMessage && undatedFestivals.length" class="undated section-card">
      <header class="undated-head">
        <h3>날짜 정보가 없는 축제</h3>
        <p>정확한 날짜가 추가로 공지될 예정인 축제입니다.</p>
      </header>

      <ul class="undated-grid">
        <li
          v-for="(festival, index) in undatedFestivals"
          :key="festival.id + '-undated'"
          class="undated-item"
          @click="router.push(`/festivals/${festival.id}`)"
        >
          <span class="icon-box" aria-hidden="true">{{ iconTokens[index % iconTokens.length] }}</span>
          <div class="text-box">
            <strong>{{ festival.title }}</strong>
            <span>{{ festival.place }}</span>
          </div>
        </li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.festival-calendar-page {
  padding: 18px 0 36px;
  display: grid;
  gap: 14px;
}

.hero {
  min-height: 138px;
  border-radius: 22px;
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(260px, 1fr) 1.6fr;
  align-items: center;
  background:
    radial-gradient(circle at 8% 14%, rgba(160, 212, 106, 0.2), transparent 46%),
    linear-gradient(180deg, #fcfdf9, #f5f8ef);
}

.hero-copy {
  padding: 20px 20px 18px;
  display: grid;
  gap: 6px;
}

.kicker {
  margin: 0;
  font-size: 24px;
}

.hero-copy h1 {
  margin: 0;
  color: #21382f;
  font-size: 48px;
  line-height: 1;
  letter-spacing: -0.04em;
}

.hero-copy p {
  margin: 0;
  color: #5f736a;
  font-weight: 650;
}

.hero-art {
  height: 100%;
  min-height: 130px;
}

.hero-art img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.state-box {
  min-height: 190px;
  display: grid;
  place-items: center;
  border: 1px dashed #d8ddd4;
  border-radius: 18px;
  background: #fbfdf8;
  color: #62776b;
  font-weight: 750;
}

.calendar-layout {
  display: grid;
  grid-template-columns: 1.9fr 1fr;
  gap: 14px;
}

.calendar-panel {
  padding: 12px 14px 10px;
  border-radius: 20px;
}

.legend-row {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.legend-chip {
  border: 1px solid #e2e5de;
  background: #fff;
  color: #52655b;
  border-radius: var(--radius-pill);
  min-height: 30px;
  padding: 0 11px;
  font-size: 12px;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.legend-chip .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--chip-color);
}

.day-panel {
  padding: 12px;
  border-radius: 20px;
  display: grid;
  align-content: start;
  gap: 10px;
}

.day-panel h2 {
  margin: 0;
  color: #243a2f;
  font-size: 24px;
  letter-spacing: -0.03em;
}

.selected-date {
  margin: 0;
  color: #384f43;
  font-size: 20px;
  font-weight: 850;
}

.festival-cards {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.festival-card {
  border: 1px solid #e4e7de;
  border-radius: 14px;
  padding: 8px;
  display: grid;
  grid-template-columns: 104px 1fr;
  gap: 10px;
  cursor: pointer;
  transition: border-color 0.15s ease, transform 0.15s ease;
}

.festival-card:hover {
  border-color: #cddbc3;
  transform: translateY(-1px);
}

.thumb {
  width: 104px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  background: #eef3e8;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  min-width: 0;
  display: grid;
  align-content: start;
  gap: 3px;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.badge {
  display: inline-flex;
  align-items: center;
  border-radius: var(--radius-pill);
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 800;
  color: var(--badge-color);
  background: color-mix(in srgb, var(--badge-color) 16%, #fff);
}

.bookmark {
  border: 0;
  background: transparent;
  color: #7c8a83;
  font-size: 16px;
  padding: 0;
  width: 20px;
  height: 20px;
}

.card-body strong {
  color: #283f35;
  font-size: 14px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  color: #677a71;
  font-size: 12px;
}

.free-chip {
  width: fit-content;
  border-radius: var(--radius-pill);
  background: #eef8e5;
  color: #5b9a2d;
  font-size: 11px;
  font-weight: 800;
  padding: 2px 7px;
}

.empty-day {
  margin: 0;
  border: 1px dashed #d9dfd3;
  border-radius: 12px;
  padding: 13px;
  color: #677b70;
  font-weight: 700;
}

.all-btn {
  min-height: 40px;
  border: 1px solid #dbe2d6;
  border-radius: 12px;
  background: #fdfefb;
  color: #32483d;
  font-size: 13px;
  font-weight: 800;
}

.undated {
  padding: 14px;
  border-radius: 20px;
  display: grid;
  gap: 10px;
}

.undated-head h3 {
  margin: 0;
  color: #253c31;
  font-size: 20px;
  letter-spacing: -0.03em;
}

.undated-head p {
  margin: 4px 0 0;
  color: #667b70;
  font-size: 13px;
}

.undated-grid {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
}

.undated-item {
  border: 1px solid #e4e8df;
  border-radius: 12px;
  padding: 9px;
  display: grid;
  grid-template-columns: 46px 1fr;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.icon-box {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  background: #edf3e7;
  border: 1px solid #d7dfcf;
  display: grid;
  place-items: center;
  font-size: 21px;
}

.text-box {
  min-width: 0;
  display: grid;
  gap: 2px;
}

.text-box strong {
  color: #294036;
  font-size: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.text-box span {
  color: #6a7f74;
  font-size: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

:deep(.fc) {
  --fc-border-color: #ecefe8;
  --fc-page-bg-color: transparent;
  --fc-neutral-bg-color: transparent;
  --fc-today-bg-color: transparent;
  --fc-button-bg-color: #2f4153;
  --fc-button-border-color: #2f4153;
  --fc-button-hover-bg-color: #26384a;
  --fc-button-hover-border-color: #26384a;
  --fc-button-active-bg-color: #1f3040;
  --fc-button-active-border-color: #1f3040;
  font-family: inherit;
}

:deep(.fc .fc-toolbar) {
  margin-bottom: 10px;
}

:deep(.fc .fc-toolbar-title) {
  color: #243a2f;
  font-size: 37px;
  font-weight: 900;
  letter-spacing: -0.05em;
}

:deep(.fc .fc-button) {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 10px;
  box-shadow: none !important;
}

:deep(.fc .fc-col-header-cell-cushion) {
  padding: 7px 0;
  color: #728078;
  font-size: 14px;
  font-weight: 800;
}

:deep(.fc .fc-daygrid-day-frame) {
  min-height: 74px;
}

:deep(.fc .fc-daygrid-day-top) {
  justify-content: center;
}

:deep(.fc .fc-daygrid-day-number) {
  width: 54px;
  height: 44px;
  display: grid;
  place-items: center;
  padding: 0;
  border-radius: 12px;
  color: #384f43;
  font-size: 18px;
  font-weight: 800;
}

:deep(.fc .selected-day .fc-daygrid-day-number) {
  background: #f2efd5;
  border: 2px solid #b9ca7a;
  color: #2f4437;
}

:deep(.fc .fc-day-other .fc-daygrid-day-number) {
  color: #bec4bf;
}

:deep(.fc .fc-daygrid-day-events) {
  min-height: 10px;
  margin: -1px 0 0;
}

:deep(.fc .fc-daygrid-event) {
  justify-content: center;
  margin: 0;
  color: transparent;
}

:deep(.fc .fc-daygrid-event-dot) {
  border-width: 4px;
  margin: 0;
}

:deep(.fc .fc-event-title) {
  display: none;
}

@media (max-width: 1280px) {
  .hero-copy h1 {
    font-size: 40px;
  }

  :deep(.fc .fc-toolbar-title) {
    font-size: 32px;
  }
}

@media (max-width: 1080px) {
  .calendar-layout {
    grid-template-columns: 1fr;
  }

  .undated-grid {
    grid-template-columns: 1fr;
  }

  .hero {
    grid-template-columns: 1fr;
  }

  .hero-art {
    min-height: 120px;
  }
}

@media (max-width: 760px) {
  .festival-calendar-page {
    padding-top: 14px;
  }

  .hero-copy h1 {
    font-size: 32px;
  }

  .selected-date {
    font-size: 16px;
  }

  .festival-card {
    grid-template-columns: 88px 1fr;
  }

  .thumb {
    width: 88px;
    height: 72px;
  }

  :deep(.fc .fc-toolbar-title) {
    font-size: 26px;
  }

  :deep(.fc .fc-daygrid-day-number) {
    width: 40px;
    height: 34px;
    font-size: 14px;
  }

  :deep(.fc .fc-daygrid-day-frame) {
    min-height: 58px;
  }
}
</style>

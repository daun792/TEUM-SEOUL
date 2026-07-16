<script setup>
import { computed, ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import { RouterLink, useRouter } from 'vue-router'
import { getFestivalPage } from '../../services/festivalsApi.js'
import { useFestivalQuery } from '../../composables/useFestivalQuery.js'
import { addDaysIso, calendarRange, formatLocalDate, todayIso } from '../../utils/dateRange.js'
import { getFestivalTags } from '../../utils/festivalTags.js'

const CALENDAR_PAGE_SIZE = 100
const selectedDate = ref(todayIso())
const visibleRange = ref(null)
const router = useRouter()
const props = defineProps({
  selectedCategory: {
    type: String,
    default: '전체',
  },
})

const festivalQuery = useFestivalQuery(
  (params, options) => getFestivalPage(params, options),
  { initialData: { items: [], total: 0, page: 1, size: CALENDAR_PAGE_SIZE, pages: 0 } },
)

const categoryPalette = {
  공연: '#6b5bd1',
  전시: '#42a9cd',
  전통: '#69b62f',
  '야외 행사': '#f25752',
  전체: '#ff8a24',
}

function eventCategory(tags) {
  return ['공연', '전시', '전통', '야외 행사'].find((tag) => tags.includes(tag)) || '전체'
}

const events = computed(() => (festivalQuery.data.value?.items || [])
  .filter((festival) => festival.start)
  .map((festival) => {
    const tags = getFestivalTags(festival)
    const category = eventCategory(tags)
    return {
      id: festival.id,
      title: festival.title,
      start: festival.start,
      end: addDaysIso(festival.end || festival.start, 1),
      color: categoryPalette[category],
      display: 'list-item',
      allDay: true,
      extendedProps: { tags },
    }
  }))

const filteredEvents = computed(() => events.value
  .filter((event) => event.extendedProps.tags.includes(props.selectedCategory)))

function loadVisibleRange(options = {}) {
  if (!visibleRange.value) return Promise.resolve(null)
  return festivalQuery.run({
    startDate: visibleRange.value.startDate,
    endDate: visibleRange.value.endDate,
    page: 1,
    size: CALENDAR_PAGE_SIZE,
  }, options)
}

function handleDatesSet(info) {
  const range = calendarRange(info.start, info.end)
  const unchanged = visibleRange.value
    && visibleRange.value.startDate === range.startDate
    && visibleRange.value.endDate === range.endDate
  visibleRange.value = range
  if (!unchanged) loadVisibleRange()
}

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: 'prev',
    center: 'title',
    right: 'today next',
  },
  height: 'auto',
  fixedWeekCount: true,
  showNonCurrentDates: true,
  events: filteredEvents.value,
  datesSet: handleDatesSet,
  dateClick: (info) => {
    selectedDate.value = info.dateStr
  },
  eventClick: (info) => {
    router.push(`/festivals/${info.event.id}`)
  },
  dayCellClassNames: (info) => (
    formatLocalDate(info.date) === selectedDate.value ? ['selected-day'] : []
  ),
}))
</script>

<template>
  <section class="calendar-section section-card" :aria-busy="festivalQuery.loading.value">
    <header class="section-head">
      <div>
        <h2>축제 캘린더</h2>
        <p>달을 이동하면 해당 기간의 행사만 불러옵니다.</p>
      </div>
      <RouterLink to="/festivals?view=calendar">더보기 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <div class="calendar-status" aria-live="polite">
      <span v-if="festivalQuery.waking.value">서버를 깨우는 중입니다.</span>
      <span v-else-if="festivalQuery.loading.value">이 달의 행사를 불러오는 중입니다.</span>
      <button v-if="festivalQuery.error.value" type="button" @click="festivalQuery.retry">다시 시도</button>
    </div>

    <FullCalendar :options="calendarOptions" />

    <p v-if="festivalQuery.data.value?.total > CALENDAR_PAGE_SIZE" class="limit-note">
      {{ festivalQuery.data.value.total }}건 중 {{ CALENDAR_PAGE_SIZE }}건을 표시합니다.
    </p>

    <div class="legend" aria-label="축제 유형 범례">
      <span class="performance">공연</span>
      <span class="exhibition">전시</span>
      <span class="tradition">전통</span>
      <span class="experience">야외 행사</span>
      <span class="etc">기타</span>
    </div>
  </section>
</template>

<style scoped>
.calendar-section {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
  border-radius: 18px;
}

.section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}

h2 {
  margin: 0;
  color: #24372e;
  font-size: 20px;
  letter-spacing: -0.035em;
}

.section-head p {
  margin: 4px 0 0;
  color: #75827b;
  font-size: 10px;
}

.section-head a {
  color: #6b756f;
  font-size: 12px;
  font-weight: 750;
}

.calendar-status {
  min-height: 20px;
  color: #6a7b72;
  font-size: 10px;
}

.calendar-status button {
  border: 1px solid #ccd9c7;
  border-radius: 8px;
  padding: 4px 8px;
  background: #fff;
  color: #365a3f;
  cursor: pointer;
  font-size: 10px;
  font-weight: 750;
}

.limit-note {
  margin: 8px 0 0;
  color: #718078;
  font-size: 10px;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 11px;
  margin-top: 12px;
  color: #5e6d65;
  font-size: 10px;
  font-weight: 750;
}

.legend span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.legend span::before {
  content: '';
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.performance::before { background: #6b5bd1; }
.exhibition::before { background: #42a9cd; }
.tradition::before { background: #69b62f; }
.experience::before { background: #f25752; }
.etc::before { background: #ff8a24; }

:deep(.fc) {
  flex: 1;
  --fc-border-color: transparent;
  --fc-button-text-color: #304139;
  --fc-button-bg-color: transparent;
  --fc-button-border-color: transparent;
  --fc-button-hover-bg-color: #f2f5ed;
  --fc-button-hover-border-color: transparent;
  --fc-button-active-bg-color: #edf4e6;
  --fc-button-active-border-color: transparent;
  --fc-page-bg-color: transparent;
  --fc-neutral-bg-color: transparent;
  --fc-today-bg-color: transparent;
  font-family: inherit;
}

:deep(.fc .fc-toolbar) { margin-bottom: 10px; }
:deep(.fc .fc-toolbar-title) { color: #263a30; font-size: 14px; font-weight: 850; }
:deep(.fc .fc-button) { padding: 3px 7px; border-radius: 50%; box-shadow: none !important; font-size: 10px; }
:deep(.fc .fc-col-header-cell-cushion) { padding: 5px 0; color: #7b847e; font-size: 10px; font-weight: 700; }
:deep(.fc-theme-standard td),
:deep(.fc-theme-standard th) { border: 0; }
:deep(.fc .fc-daygrid-day-frame) { min-height: 40px; }
:deep(.fc .fc-daygrid-day-top) { justify-content: center; }
:deep(.fc .fc-daygrid-day-number) {
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  padding: 0;
  border-radius: 50%;
  color: #4e5c54;
  font-size: 10px;
  font-weight: 750;
}
:deep(.fc .selected-day .fc-daygrid-day-number) { background: var(--color-primary); color: #fff; }
:deep(.fc .fc-day-other .fc-daygrid-day-number) { color: #c2c6c3; }
:deep(.fc .fc-daygrid-day-events) { min-height: 7px; margin: -2px 0 0; }
:deep(.fc .fc-daygrid-event) { justify-content: center; margin: 0; color: transparent; }
:deep(.fc .fc-daygrid-event-dot) { border-width: 3px; margin: 0; }
:deep(.fc .fc-event-title) { display: none; }

@media (max-width: 1320px) {
  :deep(.fc .fc-daygrid-day-frame) { min-height: 52px; }
}

@media (max-width: 760px) {
  :deep(.fc .fc-toolbar-title) { font-size: 12px; }
  :deep(.fc .fc-button) { padding: 3px 5px; }
  :deep(.fc .fc-daygrid-day-number) { width: 24px; height: 24px; }
}
</style>

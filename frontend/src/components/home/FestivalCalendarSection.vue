<script setup>
import { computed, onMounted, ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import { useRouter } from 'vue-router'
import { getFestivalList } from '../../mocks/festivals'

const selectedDate = ref('2026-07-18')
const router = useRouter()
const props = defineProps({
  selectedCategory: {
    type: String,
    default: '오늘',
  },
})

const categoryPalette = ['#6b5bd1', '#42a9cd', '#69b62f', '#f25752', '#ff8a24']
const events = ref([])

onMounted(async () => {
  const festivals = await getFestivalList()
  events.value = festivals.map((festival, index) => ({
    id: festival.id,
    title: festival.title,
    start: festival.start,
    end: festival.end,
    color: categoryPalette[index % categoryPalette.length],
    display: 'list-item',
    extendedProps: {
      tags:
        index === 0
          ? ['오늘', '이번 주말', '무료 축제', '공연', '야외 행사']
          : index === 1
            ? ['오늘', '이번 주말', '무료 축제', '전시']
            : ['전통'],
    },
  }))
})

const filteredEvents = computed(() =>
  events.value.filter((event) => event.extendedProps.tags.includes(props.selectedCategory)),
)

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  initialDate: '2026-07-18',
  locale: koLocale,
  headerToolbar: {
    left: 'prev',
    center: 'title',
    right: 'next',
  },
  height: 'auto',
  fixedWeekCount: true,
  showNonCurrentDates: true,
  events: filteredEvents.value,
  dateClick: (info) => {
    selectedDate.value = info.dateStr
  },
  eventClick: (info) => {
    router.push(`/festivals/${info.event.id}`)
  },
  dayCellClassNames: (info) => (info.date.toISOString().slice(0, 10) === selectedDate.value ? ['selected-day'] : []),
}))
</script>

<template>
  <section class="calendar-section section-card">
    <header class="section-head">
      <h2>축제 캘린더</h2>
      <RouterLink to="/festivals">더보기 <span aria-hidden="true">›</span></RouterLink>
    </header>

    <FullCalendar :options="calendarOptions" />

    <div class="legend" aria-label="축제 유형 범례">
      <span class="performance">공연</span>
      <span class="exhibition">전시</span>
      <span class="tradition">전통</span>
      <span class="experience">체험</span>
      <span class="etc">기타</span>
    </div>
  </section>
</template>

<style scoped>
.calendar-section {
  height: 100%;
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

:deep(.fc .fc-toolbar) {
  margin-bottom: 10px;
}

:deep(.fc .fc-toolbar-title) {
  color: #263a30;
  font-size: 14px;
  font-weight: 850;
}

:deep(.fc .fc-button) {
  padding: 3px 7px;
  border-radius: 50%;
  box-shadow: none !important;
  font-size: 11px;
}

:deep(.fc .fc-col-header-cell-cushion) {
  padding: 5px 0;
  color: #7b847e;
  font-size: 10px;
  font-weight: 700;
}

:deep(.fc-theme-standard td),
:deep(.fc-theme-standard th) {
  border: 0;
}

:deep(.fc .fc-daygrid-day-frame) {
  min-height: 40px;
}

:deep(.fc .fc-daygrid-day-top) {
  justify-content: center;
}

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

:deep(.fc .selected-day .fc-daygrid-day-number) {
  background: var(--color-primary);
  color: #fff;
}

:deep(.fc .fc-day-other .fc-daygrid-day-number) {
  color: #c2c6c3;
}

:deep(.fc .fc-daygrid-day-events) {
  min-height: 7px;
  margin: -2px 0 0;
}

:deep(.fc .fc-daygrid-event) {
  justify-content: center;
  margin: 0;
  color: transparent;
}

:deep(.fc .fc-daygrid-event-dot) {
  border-width: 3px;
  margin: 0;
}

:deep(.fc .fc-event-title) {
  display: none;
}

@media (max-width: 1320px) {
  :deep(.fc .fc-daygrid-day-frame) {
    min-height: 52px;
  }
}
</style>

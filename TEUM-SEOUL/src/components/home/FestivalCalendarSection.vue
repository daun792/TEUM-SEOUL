<script setup>
import { ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'

const calendarRef = ref(null)
const selectedDate = ref('')

const categoryClass = {
  공연: 'cat-performance',
  전시: 'cat-exhibition',
  전통: 'cat-tradition',
  체험: 'cat-experience',
  기타: 'cat-etc',
}

const events = [
  { title: '한강 불빛 축제', start: '2026-07-18', category: '공연' },
  { title: '서울숲 음악 페스티벌', start: '2026-07-19', category: '공연' },
  { title: '북촌 한옥 야행', start: '2026-07-24', category: '전통' },
  { title: '성수 아트 전시', start: '2026-07-25', category: '전시' },
  { title: '가족 체험 마켓', start: '2026-07-27', category: '체험' },
  { title: '야외 버스킹 데이', start: '2026-07-29', category: '기타' },
].map((item, index) => ({
  id: String(index + 1),
  title: item.title,
  start: item.start,
  allDay: true,
  display: 'list-item',
  classNames: [categoryClass[item.category] || 'cat-etc'],
  extendedProps: { category: item.category },
}))

const toDateString = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

const handleDateClick = (info) => {
  selectedDate.value = info.dateStr
  info.view.calendar.render()
}

const calendarOptions = {
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: 'prev',
    center: 'title',
    right: 'next',
  },
  height: 'auto',
  fixedWeekCount: false,
  events,
  dateClick: handleDateClick,
  dayCellClassNames: (arg) => {
    const day = toDateString(arg.date)
    return selectedDate.value === day ? ['selected-day'] : []
  },
}
</script>

<template>
  <section class="container calendar-section section-card">
    <div class="section-head">
      <h3>축제 캘린더</h3>
      <p>날짜를 선택해 이번 달 축제를 확인해보세요.</p>
    </div>

    <div class="legend">
      <span class="dot performance">공연</span>
      <span class="dot exhibition">전시</span>
      <span class="dot tradition">전통</span>
      <span class="dot experience">체험</span>
      <span class="dot etc">기타</span>
    </div>

    <FullCalendar ref="calendarRef" :options="calendarOptions" />
  </section>
</template>

<style scoped>
.calendar-section {
  padding: 18px;
  display: grid;
  gap: 14px;
}

.section-head h3 {
  margin: 0;
  font-size: 24px;
  color: #25453a;
}

.section-head p {
  margin: 6px 0 0;
  color: #5c776d;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dot {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f7fbf5;
  border: 1px solid var(--color-border);
  font-size: 13px;
  font-weight: 700;
  color: #315247;
}

.dot::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.performance::before {
  background: #63b94f;
}
.dot.exhibition::before {
  background: #f45b4f;
}
.dot.tradition::before {
  background: #ff8a3d;
}
.dot.experience::before {
  background: #a9e4ec;
}
.dot.etc::before {
  background: #b9dd5a;
}

/* FullCalendar 커스텀 */
:deep(.fc) {
  --fc-border-color: #e7e7df;
  --fc-button-text-color: #1f3d32;
  --fc-button-bg-color: #ffffff;
  --fc-button-border-color: #dfe5d7;
  --fc-button-hover-bg-color: #eef9e7;
  --fc-button-hover-border-color: #cfe4bf;
  --fc-button-active-bg-color: #e7f8de;
  --fc-button-active-border-color: #c3deb1;
  --fc-page-bg-color: #ffffff;
  --fc-neutral-bg-color: #fbfdf7;
  --fc-today-bg-color: #f4fde9;
  font-family: inherit;
}

:deep(.fc .fc-toolbar-title) {
  font-size: 1.05rem;
  color: #244438;
}

:deep(.fc .fc-button) {
  border-radius: 999px;
  box-shadow: none;
  padding: 0.35rem 0.7rem;
}

:deep(.fc .fc-daygrid-day-number) {
  color: #35574b;
  font-weight: 600;
}

:deep(.fc .selected-day .fc-daygrid-day-number) {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #63b94f;
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

:deep(.fc .fc-event) {
  border: 0;
  background: transparent;
  color: #35574b;
  font-size: 12px;
}

:deep(.fc .fc-daygrid-event-dot) {
  border-width: 4px;
  margin-right: 4px;
}

:deep(.fc .cat-performance .fc-daygrid-event-dot) {
  border-color: #63b94f;
}
:deep(.fc .cat-exhibition .fc-daygrid-event-dot) {
  border-color: #f45b4f;
}
:deep(.fc .cat-tradition .fc-daygrid-event-dot) {
  border-color: #ff8a3d;
}
:deep(.fc .cat-experience .fc-daygrid-event-dot) {
  border-color: #a9e4ec;
}
:deep(.fc .cat-etc .fc-daygrid-event-dot) {
  border-color: #b9dd5a;
}

@media (max-width: 768px) {
  .calendar-section {
    padding: 14px;
  }
}
</style>
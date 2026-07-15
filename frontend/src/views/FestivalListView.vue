<script setup>
import { computed, onMounted, ref } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import { useRouter } from 'vue-router'
import { getFestivalList } from '../services/festivalsApi'

const festivals = ref([])
const loading = ref(true)
const errorMessage = ref('')
const selectedDate = ref(new Date().toISOString().slice(0, 10))
const router = useRouter()

const events = computed(() =>
  festivals.value
    .filter((festival) => festival.start)
    .map((festival) => ({
      id: festival.id,
      title: festival.title,
      start: festival.start,
      end: festival.end || festival.start,
      allDay: true,
    })),
)

function includesSelectedDate(festival) {
  if (!festival.start) return false
  const selected = new Date(`${selectedDate.value}T00:00:00`)
  const start = new Date(`${festival.start}T00:00:00`)
  const end = new Date(`${festival.end || festival.start}T23:59:59`)
  return start <= selected && selected <= end
}

const selectedFestivals = computed(() => festivals.value.filter((festival) => includesSelectedDate(festival)))
const undatedFestivals = computed(() => festivals.value.filter((festival) => !festival.start && !festival.end))

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
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
    festivals.value = await getFestivalList({ page: 1, size: 60 })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '축제 데이터를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="container festival-list-page">
    <header class="page-head">
      <h1>축제 캘린더</h1>
      <p>월간 캘린더에서 날짜를 선택하고 축제 상세로 이동해보세요.</p>
    </header>

    <section v-if="loading" class="empty-box">축제 데이터를 불러오는 중입니다...</section>
    <section v-else-if="errorMessage" class="empty-box">{{ errorMessage }}</section>
    <section v-else-if="!festivals.length" class="empty-box">표시할 축제 데이터가 없습니다.</section>
    <section v-else class="calendar-wrap section-card" aria-label="축제 캘린더">
      <FullCalendar :options="calendarOptions" />
    </section>

    <section v-if="!loading && !errorMessage" class="selected-wrap">
      <h2>{{ selectedDate }} 축제</h2>
      <ul v-if="selectedFestivals.length" class="selected-list">
        <li v-for="festival in selectedFestivals" :key="festival.id" @click="router.push(`/festivals/${festival.id}`)">
          <strong>{{ festival.title }}</strong>
          <span>{{ festival.period }} | {{ festival.place }}</span>
        </li>
      </ul>
      <p v-else class="empty-day">선택한 날짜에 진행 중인 축제가 없습니다.</p>
    </section>

    <section v-if="!loading && !errorMessage && undatedFestivals.length" class="selected-wrap">
      <h2>날짜 정보가 없는 축제</h2>
      <p class="calendar-note">원본 데이터에 행사 날짜 필드가 없어 캘린더에 배치하지 못한 항목입니다.</p>
      <ul class="selected-list">
        <li v-for="festival in undatedFestivals" :key="festival.id + '-undated'" @click="router.push(`/festivals/${festival.id}`)">
          <strong>{{ festival.title }}</strong>
          <span>{{ festival.place }}</span>
        </li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.festival-list-page {
  padding: 28px 0 40px;
}

.page-head {
  margin-bottom: 18px;
}

h1 {
  margin: 0;
  font-size: 28px;
  letter-spacing: -0.03em;
  color: #233c31;
}

.page-head p {
  margin: 8px 0 0;
  color: #60756c;
}

.calendar-wrap {
  padding: 14px;
  border-radius: 16px;
}

.selected-wrap {
  margin-top: 14px;
}

.selected-wrap h2 {
  margin: 0 0 10px;
  color: #263d33;
  font-size: 20px;
}

.selected-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 8px;
}

.selected-list li {
  border: 1px solid #dde5d8;
  border-radius: 12px;
  padding: 10px 12px;
  display: grid;
  gap: 4px;
  cursor: pointer;
}

.selected-list strong {
  color: #2b4439;
}

.selected-list span {
  color: #61756b;
  font-size: 13px;
}

.empty-day {
  margin: 0;
  border: 1px dashed #d5ddd0;
  border-radius: 12px;
  padding: 14px;
  color: #63776c;
  font-weight: 700;
}

.calendar-note {
  margin: 0 0 8px;
  color: #64786d;
  font-size: 13px;
}

.empty-box {
  min-height: 160px;
  display: grid;
  place-items: center;
  border: 1px dashed #d5ddd0;
  border-radius: 14px;
  color: #64786d;
  font-weight: 700;
  background: #fbfdf8;
}

:deep(.fc .selected-day .fc-daygrid-day-number) {
  background: var(--color-primary);
  color: #fff;
}

@media (max-width: 1100px) {
  .calendar-wrap {
    overflow-x: auto;
  }
}

@media (max-width: 760px) {
  .festival-list-page {
    padding-top: 18px;
  }
}
</style>

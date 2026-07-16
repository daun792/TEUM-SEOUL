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
  <main class="festival-list-page">
    <section class="hero-shell">
      <div class="container hero-grid">
        <div class="hero-copy">
          <span class="eyebrow">축제 캘린더</span>
          <h1>매일 달라지는 서울의 축제를 한눈에 확인해보세요.</h1>
          <p>날짜를 고르면 해당 기간에 진행 중인 축제와 날짜 정보가 없는 축제를 함께 볼 수 있습니다.</p>
        </div>

        <div class="hero-illustration" aria-hidden="true">
          <div class="illustration-stage">
            <div class="illustration-placeholder illustration-1"></div>
            <div class="illustration-placeholder illustration-2"></div>
            <div class="illustration-placeholder illustration-3"></div>
          </div>
        </div>
      </div>
    </section>

    <div class="container content-grid">
      <section v-if="loading" class="empty-box section-card">축제 데이터를 불러오는 중입니다...</section>
      <section v-else-if="errorMessage" class="empty-box section-card">{{ errorMessage }}</section>
      <section v-else-if="!festivals.length" class="empty-box section-card">표시할 축제 데이터가 없습니다.</section>
      <section v-else class="calendar-panel section-card" aria-label="축제 캘린더">
        <FullCalendar :options="calendarOptions" />
      </section>

      <aside v-if="!loading && !errorMessage" class="selection-panel section-card">
        <header class="selection-head">
          <h2>{{ selectedDate }}의 축제</h2>
          <span class="selection-count">{{ selectedFestivals.length }}개</span>
        </header>

        <ul v-if="selectedFestivals.length" class="festival-list compact-list">
          <li v-for="festival in selectedFestivals" :key="festival.id" @click="router.push(`/festivals/${festival.id}`)">
            <div class="festival-thumb" aria-hidden="true"></div>
            <div class="festival-copy">
              <strong>{{ festival.title }}</strong>
              <span>{{ festival.period }} | {{ festival.place }}</span>
            </div>
          </li>
        </ul>
        <p v-else class="empty-day">선택한 날짜에 진행 중인 축제가 없습니다.</p>

        <footer class="selection-footer">
          <RouterLink to="/festivals">전체 축제 보기 <span aria-hidden="true">›</span></RouterLink>
        </footer>
      </aside>
    </div>

    <section v-if="!loading && !errorMessage && undatedFestivals.length" class="container undated-panel section-card">
      <h2>날짜 정보가 없는 축제</h2>
      <p class="calendar-note">원본 데이터에 행사 날짜 필드가 없어 캘린더에 배치하지 못한 항목입니다.</p>

      <ul class="festival-list undated-list">
        <li v-for="festival in undatedFestivals" :key="festival.id + '-undated'" @click="router.push(`/festivals/${festival.id}`)">
          <div class="festival-thumb muted" aria-hidden="true"></div>
          <div class="festival-copy">
            <strong>{{ festival.title }}</strong>
            <span>{{ festival.place }}</span>
          </div>
        </li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.festival-list-page {
  padding: 24px 0 40px;
  display: grid;
  gap: 16px;
  background:
    radial-gradient(circle at 86% 8%, rgba(181, 224, 91, 0.18), transparent 18%),
    linear-gradient(180deg, #fffef9 0%, #fbfaf4 100%);
}

.hero-shell {
  padding: 18px 0 6px;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(360px, 1fr);
  gap: 18px;
  align-items: center;
}

.hero-copy {
  display: grid;
  gap: 10px;
}

.eyebrow {
  width: fit-content;
  padding: 7px 12px;
  border-radius: var(--radius-pill);
  background: #eaf5dd;
  color: #4b7a29;
  font-size: 13px;
  font-weight: 850;
}

h1 {
  margin: 0;
  font-size: clamp(28px, 3vw, 40px);
  line-height: 1.18;
  letter-spacing: -0.04em;
  color: #21372d;
}

.hero-copy p {
  margin: 0;
  color: #60756c;
  font-size: 15px;
  line-height: 1.6;
}

.hero-illustration {
  display: flex;
  justify-content: center;
}

.illustration-stage {
  width: min(100%, 640px);
  min-height: 160px;
  display: grid;
  grid-template-columns: 1.2fr 0.9fr 0.7fr;
  gap: 12px;
  align-items: end;
}

.illustration-placeholder {
  min-height: 140px;
  border: 1px dashed #d7dfd0;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.7);
}

.illustration-1 { min-height: 170px; }
.illustration-2 { min-height: 122px; }
.illustration-3 { min-height: 150px; }

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(290px, 0.95fr);
  gap: 16px;
  align-items: start;
}

.calendar-panel,
.selection-panel,
.undated-panel {
  padding: 16px;
  border-radius: 20px;
}

.calendar-panel {
  min-height: 620px;
}

.selection-panel {
  min-height: 620px;
  display: flex;
  flex-direction: column;
}

.selection-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

.selection-head h2,
.undated-panel h2 {
  margin: 0;
  color: #263d33;
  font-size: 19px;
  letter-spacing: -0.03em;
}

.selection-count {
  padding: 5px 10px;
  border-radius: var(--radius-pill);
  background: #eef6e4;
  color: #4f7f2f;
  font-size: 12px;
  font-weight: 800;
}

.festival-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.compact-list {
  flex: 1;
  align-content: start;
}

.festival-list li {
  display: grid;
  grid-template-columns: 92px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  border: 1px solid #e2e6de;
  border-radius: 16px;
  padding: 10px;
  background: #fff;
  cursor: pointer;
}

.festival-list li:hover {
  background: #fbfdf8;
}

.festival-thumb {
  min-height: 78px;
  border-radius: 12px;
  border: 1px dashed #cfd7c9;
  background: linear-gradient(135deg, #f7faf3, #eef4e8);
}

.festival-thumb.muted {
  background: linear-gradient(135deg, #fafcf8, #f2f6ee);
}

.festival-copy {
  min-width: 0;
  display: grid;
  gap: 4px;
}

.festival-copy strong {
  color: #284137;
  font-size: 14px;
  line-height: 1.45;
}

.festival-copy span {
  color: #62756c;
  font-size: 12px;
  line-height: 1.45;
}

.selection-footer {
  margin-top: auto;
  padding-top: 12px;
}

.selection-footer a {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #4a7a2a;
  font-size: 13px;
  font-weight: 800;
}

.undated-panel {
  display: grid;
  gap: 10px;
}

.calendar-wrap {
  padding: 14px;
  border-radius: 16px;
}

.calendar-note {
  margin: 0;
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

.empty-day {
  margin: 0;
  border: 1px dashed #d5ddd0;
  border-radius: 12px;
  padding: 14px;
  color: #63776c;
  font-weight: 700;
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

:deep(.fc .fc-toolbar-title) {
  color: #263a30;
  font-size: 16px;
  font-weight: 850;
}

:deep(.fc .fc-button) {
  padding: 4px 8px;
  border-radius: 50%;
  box-shadow: none !important;
}

:deep(.fc .fc-daygrid-day-frame) {
  min-height: 58px;
}

:deep(.fc .fc-daygrid-day-number) {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  color: #4e5c54;
  font-size: 11px;
  font-weight: 750;
}

:deep(.fc .fc-day-other .fc-daygrid-day-number) {
  color: #c2c6c3;
}

@media (max-width: 1100px) {
  .hero-grid,
  .content-grid {
    grid-template-columns: 1fr;
  }

  .selection-panel,
  .calendar-panel {
    min-height: auto;
  }

  .illustration-stage {
    width: 100%;
  }

  .calendar-panel {
    overflow-x: auto;
  }
}

@media (max-width: 760px) {
  .festival-list-page {
    padding-top: 18px;
    gap: 12px;
  }

  .hero-shell {
    padding-top: 10px;
  }

  .calendar-panel,
  .selection-panel,
  .undated-panel {
    padding: 14px;
    border-radius: 18px;
  }

  .festival-list li {
    grid-template-columns: 72px minmax(0, 1fr);
    gap: 10px;
  }

  .festival-thumb {
    min-height: 62px;
  }

  .illustration-stage {
    grid-template-columns: 1fr 0.8fr;
  }

  .illustration-3 {
    display: none;
  }
}
</style>

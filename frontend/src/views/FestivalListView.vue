<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'
import koLocale from '@fullcalendar/core/locales/ko'
import { useRoute, useRouter } from 'vue-router'
import FestivalCard from '../components/festival/FestivalCard.vue'
import { getFestivalPage } from '../services/festivalsApi.js'
import { useFestivalQuery } from '../composables/useFestivalQuery.js'
import { addDaysIso, calendarRange, formatLocalDate, todayIso } from '../utils/dateRange.js'
import { getFestivalStatus } from '../utils/festivalTags.js'

const PAGE_SIZE = 24
const CALENDAR_PAGE_SIZE = 100
const SEARCH_DEBOUNCE_MS = 300

const route = useRoute()
const router = useRouter()
const searchInput = ref(String(route.query.q || ''))
const includePast = ref(route.query.includePast === '1')
const selectedDate = ref(todayIso())
const visibleRange = ref(null)
let searchTimer = null

const listQuery = useFestivalQuery(
  (params, options) => getFestivalPage(params, options),
  { initialData: { items: [], total: 0, page: 1, size: PAGE_SIZE, pages: 0 } },
)
const calendarQuery = useFestivalQuery(
  (params, options) => getFestivalPage(params, options),
  { initialData: { items: [], total: 0, page: 1, size: CALENDAR_PAGE_SIZE, pages: 0 } },
)

const viewMode = computed(() => (route.query.view === 'calendar' ? 'calendar' : 'list'))
const currentPage = computed(() => {
  const parsed = Number(route.query.page)
  return Number.isInteger(parsed) && parsed > 0 ? parsed : 1
})
const normalizedKeyword = computed(() => String(route.query.q || '').trim())

const listFestivals = computed(() => listQuery.data.value?.items || [])
const festivalCards = computed(() => listFestivals.value.map((festival) => ({
  ...festival,
  date: festival.period,
  status: getFestivalStatus(festival),
  priceType: /무료/.test(festival.title) ? '무료' : '정보 없음',
})))

const calendarFestivals = computed(() => calendarQuery.data.value?.items || [])
const calendarEvents = computed(() => calendarFestivals.value
  .filter((festival) => festival.start)
  .map((festival) => ({
    id: festival.id,
    title: festival.title,
    start: festival.start,
    end: addDaysIso(festival.end || festival.start, 1),
    allDay: true,
  })))

const selectedFestivals = computed(() => calendarFestivals.value.filter((festival) => {
  if (!festival.start) return false
  const end = festival.end || festival.start
  return festival.start <= selectedDate.value && selectedDate.value <= end
}))

function cleanQuery(query) {
  const cleaned = { ...query }
  for (const [key, value] of Object.entries(cleaned)) {
    if (value === undefined || value === null || value === '' || value === false) delete cleaned[key]
  }
  return cleaned
}

function updateRoute(patch) {
  const nextQuery = cleanQuery({ ...route.query, ...patch })
  const current = new URLSearchParams(cleanQuery(route.query)).toString()
  const next = new URLSearchParams(nextQuery).toString()
  if (current === next) return
  router.replace({ query: nextQuery })
}

function listParams() {
  return {
    q: normalizedKeyword.value || undefined,
    startDate: includePast.value ? undefined : todayIso(),
    page: currentPage.value,
    size: PAGE_SIZE,
  }
}

function loadList(options = {}) {
  return listQuery.run(listParams(), options)
}

function loadCalendar(options = {}) {
  if (!visibleRange.value) return Promise.resolve(null)
  return calendarQuery.run({
    q: normalizedKeyword.value || undefined,
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
  if (!unchanged) loadCalendar()
}

function setView(mode) {
  updateRoute({ view: mode === 'calendar' ? 'calendar' : undefined, page: undefined })
}

function togglePast() {
  updateRoute({ includePast: includePast.value ? '1' : undefined, page: undefined })
}

function goToPage(page) {
  const maxPage = Math.max(1, listQuery.data.value?.pages || 1)
  const nextPage = Math.min(maxPage, Math.max(1, page))
  updateRoute({ page: nextPage === 1 ? undefined : String(nextPage) })
}

watch(searchInput, (value) => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    const keyword = value.trim()
    if (keyword === normalizedKeyword.value) return
    updateRoute({ q: keyword || undefined, page: undefined })
  }, SEARCH_DEBOUNCE_MS)
})

watch(
  () => route.fullPath,
  () => {
    const routeKeyword = String(route.query.q || '')
    if (searchInput.value !== routeKeyword) searchInput.value = routeKeyword
    includePast.value = route.query.includePast === '1'
    if (viewMode.value === 'calendar') loadCalendar()
    else loadList()
  },
  { immediate: true },
)

onBeforeUnmount(() => {
  if (searchTimer) clearTimeout(searchTimer)
})

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  locale: koLocale,
  headerToolbar: {
    left: 'prev',
    center: 'title',
    right: 'today next',
  },
  events: calendarEvents.value,
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
  <main class="container festival-page">
    <header class="page-head">
      <div>
        <p class="eyebrow">서울 문화행사</p>
        <h1>행사 찾기</h1>
        <p>진행 중이거나 예정된 행사를 먼저 보고, 필요한 경우 지난 행사까지 검색할 수 있습니다.</p>
      </div>
      <div class="view-tabs" role="tablist" aria-label="행사 보기 방식">
        <button
          type="button"
          role="tab"
          :aria-selected="viewMode === 'list'"
          :class="{ active: viewMode === 'list' }"
          @click="setView('list')"
        >목록</button>
        <button
          type="button"
          role="tab"
          :aria-selected="viewMode === 'calendar'"
          :class="{ active: viewMode === 'calendar' }"
          @click="setView('calendar')"
        >캘린더</button>
      </div>
    </header>

    <section class="filter-card section-card" aria-label="행사 검색 및 필터">
      <label class="search-field">
        <span>행사명 또는 지역 검색</span>
        <input
          v-model="searchInput"
          type="search"
          placeholder="예: 클래식, 마포구, 한강"
          autocomplete="off"
        />
      </label>
      <label v-if="viewMode === 'list'" class="past-toggle">
        <input v-model="includePast" type="checkbox" @change="togglePast" />
        <span>지난 행사 포함</span>
      </label>
      <p class="filter-hint">
        {{ viewMode === 'list' && !includePast ? '오늘 진행 중인 행사와 예정 행사를 표시합니다.' : '선택한 조건의 행사를 표시합니다.' }}
      </p>
    </section>

    <template v-if="viewMode === 'list'">
      <section class="result-head" aria-live="polite">
        <strong>{{ listQuery.data.value?.total || 0 }}건</strong>
        <span v-if="listQuery.loading.value && !listQuery.waking.value">행사를 불러오는 중입니다.</span>
        <span v-else-if="listQuery.waking.value">서버를 깨우는 중입니다. 첫 요청은 최대 1분 정도 걸릴 수 있습니다.</span>
      </section>

      <section v-if="listQuery.error.value" class="state-card error-state" aria-live="assertive">
        <strong>행사 데이터를 불러오지 못했습니다.</strong>
        <p>{{ listQuery.error.value }}</p>
        <button type="button" @click="listQuery.retry">다시 시도</button>
      </section>

      <section v-else-if="festivalCards.length" class="festival-grid" :aria-busy="listQuery.loading.value">
        <FestivalCard v-for="festival in festivalCards" :key="festival.id" :festival="festival" />
      </section>

      <section v-else-if="!listQuery.loading.value" class="state-card empty-state" aria-live="polite">
        <strong>조건에 맞는 행사가 없습니다.</strong>
        <p>검색어를 바꾸거나 지난 행사 포함을 선택해 보세요.</p>
      </section>

      <nav v-if="(listQuery.data.value?.pages || 0) > 1" class="pagination" aria-label="행사 목록 페이지">
        <button
          type="button"
          :disabled="currentPage <= 1 || listQuery.loading.value"
          @click="goToPage(currentPage - 1)"
        >이전</button>
        <span>{{ currentPage }} / {{ listQuery.data.value.pages }}</span>
        <button
          type="button"
          :disabled="currentPage >= listQuery.data.value.pages || listQuery.loading.value"
          @click="goToPage(currentPage + 1)"
        >다음</button>
      </nav>
    </template>

    <template v-else>
      <section class="calendar-shell section-card" :aria-busy="calendarQuery.loading.value">
        <div class="calendar-status" aria-live="polite">
          <span v-if="calendarQuery.waking.value">서버를 깨우는 중입니다.</span>
          <span v-else-if="calendarQuery.loading.value">이 달의 행사를 불러오는 중입니다.</span>
          <button v-if="calendarQuery.error.value" type="button" @click="calendarQuery.retry">불러오기 재시도</button>
        </div>
        <FullCalendar :options="calendarOptions" />
        <p v-if="calendarQuery.data.value?.total > CALENDAR_PAGE_SIZE" class="calendar-note">
          이 달의 행사 {{ calendarQuery.data.value.total }}건 중 {{ CALENDAR_PAGE_SIZE }}건을 표시합니다. 검색어로 범위를 좁혀보세요.
        </p>
      </section>

      <section class="selected-wrap">
        <h2>{{ selectedDate }} 진행 행사</h2>
        <ul v-if="selectedFestivals.length" class="selected-list">
          <li
            v-for="festival in selectedFestivals"
            :key="festival.id"
            @click="router.push(`/festivals/${festival.id}`)"
          >
            <strong>{{ festival.title }}</strong>
            <span>{{ festival.period }} · {{ festival.place }}</span>
          </li>
        </ul>
        <p v-else class="state-card empty-day">선택한 날짜에 진행 중인 행사가 없습니다.</p>
      </section>
    </template>
  </main>
</template>

<style scoped>
.festival-page {
  padding: 28px 0 48px;
}

.page-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
}

.eyebrow {
  margin: 0 0 4px;
  color: var(--color-primary, #69a83a);
  font-size: 12px;
  font-weight: 850;
}

h1 {
  margin: 0;
  color: #233c31;
  font-size: 30px;
  letter-spacing: -0.04em;
}

.page-head p:not(.eyebrow) {
  margin: 8px 0 0;
  color: #60756c;
}

.view-tabs {
  display: inline-flex;
  padding: 4px;
  border: 1px solid #dce5d8;
  border-radius: 12px;
  background: #fff;
}

.view-tabs button {
  border: 0;
  border-radius: 9px;
  padding: 8px 14px;
  background: transparent;
  color: #607068;
  cursor: pointer;
  font-weight: 750;
}

.view-tabs button.active {
  background: #edf5e7;
  color: #2f6335;
}

.filter-card {
  display: grid;
  grid-template-columns: minmax(260px, 1fr) auto;
  align-items: end;
  gap: 12px 18px;
  padding: 16px;
  border-radius: 16px;
}

.search-field {
  display: grid;
  gap: 7px;
  color: #344a40;
  font-size: 12px;
  font-weight: 800;
}

.search-field input {
  width: 100%;
  border: 1px solid #d6dfd3;
  border-radius: 11px;
  padding: 11px 12px;
  color: #24372e;
  background: #fff;
  font: inherit;
  font-size: 14px;
}

.search-field input:focus-visible,
.view-tabs button:focus-visible,
.pagination button:focus-visible,
.state-card button:focus-visible {
  outline: 3px solid rgba(105, 168, 58, 0.25);
  outline-offset: 2px;
}

.past-toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 42px;
  color: #40564b;
  cursor: pointer;
  font-size: 13px;
  font-weight: 750;
}

.past-toggle input {
  width: 17px;
  height: 17px;
  accent-color: var(--color-primary, #69a83a);
}

.filter-hint {
  grid-column: 1 / -1;
  margin: 0;
  color: #75857c;
  font-size: 12px;
}

.result-head {
  min-height: 38px;
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 14px;
  color: #65766d;
  font-size: 13px;
}

.result-head strong {
  color: #2e4439;
  font-size: 15px;
}

.festival-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  transition: opacity 0.2s ease;
}

.festival-grid[aria-busy='true'] {
  opacity: 0.55;
}

.state-card {
  margin-top: 14px;
  border: 1px dashed #d5ddd0;
  border-radius: 14px;
  padding: 22px;
  text-align: center;
  color: #63776c;
  background: #fbfdf8;
}

.state-card strong {
  display: block;
  color: #334b40;
}

.state-card p {
  margin: 7px 0 0;
}

.state-card button,
.pagination button,
.calendar-status button {
  margin-top: 12px;
  border: 1px solid #cbd9c5;
  border-radius: 10px;
  padding: 8px 13px;
  background: #fff;
  color: #365a3f;
  cursor: pointer;
  font-weight: 750;
}

.error-state {
  border-color: #e7c8c2;
  background: #fff9f7;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin-top: 22px;
  color: #51665c;
  font-size: 13px;
  font-weight: 750;
}

.pagination button {
  margin-top: 0;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.calendar-shell {
  position: relative;
  margin-top: 14px;
  padding: 14px;
  border-radius: 16px;
}

.calendar-status {
  min-height: 24px;
  color: #66786f;
  font-size: 12px;
}

.calendar-status button {
  margin: 0 0 8px;
}

.calendar-note {
  margin: 10px 0 0;
  color: #6b7c73;
  font-size: 12px;
}

.selected-wrap {
  margin-top: 18px;
}

.selected-wrap h2 {
  margin: 0 0 10px;
  color: #263d33;
  font-size: 20px;
}

.selected-list {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.selected-list li {
  display: grid;
  gap: 4px;
  border: 1px solid #dde5d8;
  border-radius: 12px;
  padding: 11px 13px;
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
  margin-top: 0;
}

:deep(.fc .selected-day .fc-daygrid-day-number) {
  border-radius: 50%;
  background: var(--color-primary, #69a83a);
  color: #fff;
}

@media (max-width: 1100px) {
  .festival-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .festival-page {
    padding-top: 18px;
  }

  .page-head {
    align-items: stretch;
    flex-direction: column;
  }

  .view-tabs {
    align-self: flex-start;
  }

  .filter-card {
    grid-template-columns: 1fr;
  }

  .filter-hint {
    grid-column: auto;
  }

  .festival-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }

  :deep(.fc .fc-toolbar) {
    align-items: center;
  }

  :deep(.fc .fc-toolbar-title) {
    font-size: 16px;
  }

  :deep(.fc .fc-button) {
    padding: 5px 8px;
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .festival-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import { useRouter } from 'vue-router'

const router = useRouter()

const festivals = [
  {
    id: '1',
    title: '서울 여름 음악축제',
    start: '2026-07-20',
    end: '2026-07-22',
  },
  {
    id: '2',
    title: '한강 야간 문화축제',
    start: '2026-07-25',
  },
  {
    id: '3',
    title: '전통예술 거리축제',
    start: '2026-08-02',
  },
]

const calendarOptions = {
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  locale: 'ko',
  events: festivals,
  height: 'auto',
  eventClick: (info) => {
    router.push(`/festivals/${info.event.id}`)
  },
}
</script>

<template>
  <section>
    <h2>서울 축제 캘린더</h2>
    <p>축제를 클릭하면 상세 화면으로 이동합니다.</p>
    <FullCalendar :options="calendarOptions" />
  </section>
</template>

<style scoped>
section {
  max-width: 980px;
}
</style>
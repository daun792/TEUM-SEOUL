<script setup> 
import FullCalendar from '@fullcalendar/vue3' 
import dayGridPlugin from '@fullcalendar/daygrid' 
import { useRouter } from 'vue-router' 
import { festivals } from '../mocks/festivals' 
const router = useRouter() 
const calendarOptions = { plugins: [dayGridPlugin], initialView: 'dayGridMonth', locale: 'ko', events: festivals.map((f) => ({ id: f.id, title: f.title, start: f.start, end: f.end, })), height: 'auto', eventClick: (info) => { router.push('/festivals/' + info.event.id) }, } 
</script> 
<template> 
<section> 
<h2>서울 축제 캘린더</h2> 
<p>축제를 클릭하면 상세 화면으로 이동합니다.</p> 
<FullCalendar :options="calendarOptions" /> 
</section> 
</template> 
<style scoped> 
section { max-width: 980px; } 
</style>
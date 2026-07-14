<script setup>
defineProps({ course: { type: Object, required: true } })
</script>

<template>
  <section class="timeline-section">
    <div class="section-heading">
      <div>
        <span class="eyebrow">추천 일정</span>
        <h2>{{ course.phase === 'before' ? '공연 전에 돌아오는 코스' : '공연 후 가볍게 이어가는 코스' }}</h2>
      </div>
      <span class="time-badge">총 {{ course.total_minutes }}분</span>
    </div>

    <ol class="timeline">
      <li class="timeline-item performance-point">
        <div class="timeline-dot">공연</div>
        <div>
          <strong>{{ course.performance.name }}</strong>
          <p>{{ course.phase === 'before' ? '공연장 출발' : '공연 종료 후 출발' }}</p>
        </div>
      </li>
      <li v-for="(place, index) in course.places" :key="place.id" class="timeline-item">
        <div class="timeline-dot">{{ index + 1 }}</div>
        <div class="place-card">
          <img v-if="place.image_url" :src="place.image_url" :alt="place.name" />
          <div class="place-content">
            <div class="place-meta"><span>{{ place.category }}</span><span>{{ place.distance_from_previous_km }}km</span></div>
            <h3>{{ place.name }}</h3>
            <p>{{ place.address || '주소 정보 없음' }}</p>
            <p class="reason">{{ place.recommendation_reason }}</p>
            <div class="duration-row">
              <span>도보 약 {{ place.walk_minutes }}분</span>
              <span>체류 약 {{ place.stay_minutes }}분</span>
            </div>
          </div>
        </div>
      </li>
      <li v-if="course.phase === 'before'" class="timeline-item performance-point">
        <div class="timeline-dot">복귀</div>
        <div>
          <strong>{{ course.performance.name }}</strong>
          <p>도보 약 {{ course.return_walk_minutes }}분 · 공연 전 {{ course.buffer_minutes }}분 여유</p>
        </div>
      </li>
    </ol>

    <div class="summary-strip">
      <span>이동 {{ course.total_walk_minutes }}분</span>
      <span>체류 {{ course.total_stay_minutes }}분</span>
      <span>남는 여유 {{ course.available_minutes - course.total_minutes }}분</span>
    </div>
    <p v-if="course.relaxed" class="notice warning">선호 카테고리 안에서 시간에 맞는 장소가 없어 가까운 다른 유형을 포함했습니다.</p>
    <p class="notice">{{ course.notice }}</p>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../services/api'

const recentPosts = ref([])
const performances = ref([])

onMounted(async () => {
  const [postResult, performanceResult] = await Promise.allSettled([
    api.get('/api/posts', { params: { size: 3 } }),
    api.get('/api/performances', { params: { limit: 4 } }),
  ])
  if (postResult.status === 'fulfilled') recentPosts.value = postResult.value.data.items
  if (performanceResult.status === 'fulfilled') performances.value = performanceResult.value.data.items
})
</script>

<template>
  <main>
    <section class="hero section-shell">
      <div class="hero-copy">
        <span class="eyebrow">공연 전후 30분–3시간</span>
        <h1>남는 시간 말고,<br /><em>서울의 틈</em>을 만드세요.</h1>
        <p>공연과 남는 시간을 고르면 실제 서울 공공데이터에서 1~2곳의 짧은 코스를 구성합니다.</p>
        <div class="hero-actions">
          <RouterLink class="primary-button" to="/gap">틈 채우기 시작</RouterLink>
          <RouterLink class="text-link" to="/posts">다른 사람의 틈 보기 →</RouterLink>
        </div>
      </div>
      <div class="hero-visual" aria-label="틈서울 서비스 예시">
        <div class="floating-card first"><span>18:00</span><strong>문화시설</strong><small>도보 6분 · 체류 50분</small></div>
        <div class="time-orbit">90<small>분</small></div>
        <div class="floating-card second"><span>19:15</span><strong>공연장 복귀</strong><small>15분 여유 확보</small></div>
      </div>
    </section>

    <section class="section-shell steps-section">
      <div class="section-heading"><div><span class="eyebrow">HOW IT WORKS</span><h2>세 단계로 만드는 짧은 서울</h2></div></div>
      <div class="step-grid">
        <article><b>01</b><h3>공연 선택</h3><p>서울 축제·공연 데이터에서 관람할 행사를 선택합니다.</p></article>
        <article><b>02</b><h3>남는 시간 입력</h3><p>공연 전후와 30~180분, 선호 장소 유형을 고릅니다.</p></article>
        <article><b>03</b><h3>1~2곳 추천</h3><p>거리와 체류시간을 계산해 시간 안에 들어오는 코스를 제시합니다.</p></article>
      </div>
    </section>

    <section class="section-shell split-section">
      <div>
        <div class="section-heading"><div><span class="eyebrow">SEOUL EVENTS</span><h2>지금 데이터에 있는 공연</h2></div><RouterLink to="/gap">전체 검색 →</RouterLink></div>
        <div class="mini-list">
          <RouterLink v-for="item in performances" :key="item.id" :to="{ path: '/gap', query: { performanceId: item.id } }">
            <span class="category-dot"></span><span><strong>{{ item.name }}</strong><small>{{ item.address }}</small></span><b>→</b>
          </RouterLink>
        </div>
      </div>
      <div>
        <div class="section-heading"><div><span class="eyebrow">COMMUNITY</span><h2>최근 공유된 틈</h2></div><RouterLink to="/posts">전체 보기 →</RouterLink></div>
        <div v-if="recentPosts.length" class="mini-list">
          <RouterLink v-for="item in recentPosts" :key="item.id" :to="`/posts/${item.id}`">
            <span class="category-pill">{{ item.category }}</span><span><strong>{{ item.title }}</strong><small>조회 {{ item.view_count }} · 좋아요 {{ item.like_count }}</small></span><b>→</b>
          </RouterLink>
        </div>
        <div v-else class="empty-card">아직 등록된 후기가 없습니다. 첫 번째 틈을 공유해보세요.</div>
      </div>
    </section>
  </main>
</template>

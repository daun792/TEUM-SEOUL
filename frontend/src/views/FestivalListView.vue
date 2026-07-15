<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { getFestivalList } from '../mocks/festivals'

const festivals = ref([])

onMounted(async () => {
  festivals.value = await getFestivalList()
})
</script>

<template>
  <main class="container festival-list-page">
    <header class="page-head">
      <h1>축제 캘린더</h1>
      <p>서울의 축제를 확인하고 상세 정보로 이동해보세요.</p>
    </header>

    <section class="grid" aria-label="축제 목록">
      <RouterLink
        v-for="festival in festivals"
        :key="festival.id"
        class="festival-item"
        :to="`/festivals/${festival.id}`"
      >
        <div class="thumb" :class="{ placeholder: !festival.imageUrl }">
          <img v-if="festival.imageUrl" :src="festival.imageUrl" :alt="festival.title" />
          <span v-else>이미지 준비중</span>
        </div>

        <div class="body">
          <h2>{{ festival.title }}</h2>
          <p><strong>기간</strong> {{ festival.period }}</p>
          <p><strong>장소</strong> {{ festival.place }}</p>
        </div>
      </RouterLink>
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

.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.festival-item {
  display: block;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: #fff;
}

.thumb {
  height: 170px;
  background: #f7faf3;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb.placeholder {
  display: grid;
  place-items: center;
  color: #6c7e74;
  font-weight: 700;
}

.body {
  padding: 12px;
}

.body h2 {
  margin: 0 0 8px;
  color: #24372e;
  font-size: 16px;
}

.body p {
  margin: 4px 0 0;
  color: #5f7369;
  font-size: 13px;
}

@media (max-width: 1100px) {
  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .festival-list-page {
    padding-top: 18px;
  }

  .grid {
    grid-template-columns: 1fr;
  }
}
</style>

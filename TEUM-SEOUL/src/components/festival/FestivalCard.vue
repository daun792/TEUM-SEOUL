<script setup>
import { ref } from 'vue'

const props = defineProps({
  festival: {
    type: Object,
    required: true,
  },
})

const bookmarked = ref(false)

const toggleBookmark = () => {
  bookmarked.value = !bookmarked.value
}
</script>

<template>
  <article class="festival-card section-card">
    <div class="thumb-wrap">
  <img
    v-if="festival.imageUrl"
    :src="festival.imageUrl"
    :alt="festival.title"
    class="thumb"
  />
  <div v-else class="thumb placeholder">이미지 준비중</div>

  <span class="badge" :class="festival.status === '진행중' ? 'on' : 'soon'">
    {{ festival.status }}
  </span>
</div>

    <div class="body">
      <h4 class="title">{{ festival.title }}</h4>
      <p class="meta">{{ festival.date }}</p>
      <p class="meta">{{ festival.place }}</p>

      <div class="bottom">
        <span class="price-tag" :class="festival.priceType === '무료' ? 'free' : 'paid'">
          {{ festival.priceType }}
        </span>
        <button type="button" class="bookmark-btn" @click="toggleBookmark">
          {{ bookmarked ? '★' : '☆' }}
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.festival-card {
  overflow: hidden;
  min-width: 280px;
}

.thumb-wrap {
  position: relative;
  height: 170px;
}

.thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.badge {
  position: absolute;
  top: 10px;
  left: 10px;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
}

.badge.on {
  background: var(--color-primary);
}

.badge.soon {
  background: var(--color-orange);
}

.body {
  padding: 14px;
  display: grid;
  gap: 6px;
}

.title {
  margin: 0;
  font-size: 17px;
  color: #244438;
}

.meta {
  margin: 0;
  color: #5e786e;
  font-size: 14px;
}

.bottom {
  margin-top: 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.price-tag {
  border-radius: 999px;
  padding: 5px 10px;
  font-weight: 700;
  font-size: 12px;
}

.price-tag.free {
  background: #edfbe8;
  color: #2f7c2f;
}

.price-tag.paid {
  background: #fff1e6;
  color: #b35915;
}

.bookmark-btn {
  border: 1px solid var(--color-border);
  background: #fff;
  border-radius: 999px;
  width: 36px;
  height: 36px;
  cursor: pointer;
  font-size: 18px;
}

.placeholder {
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #eef7ea 0%, #f8fbf1 100%);
  color: #5f766d;
  font-weight: 700;
  font-size: 14px;
}
</style>
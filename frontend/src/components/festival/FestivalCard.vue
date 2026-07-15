<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  festival: {
    type: Object,
    required: true,
  },
})

const router = useRouter()
const bookmarked = ref(false)

const openFestival = () => {
  router.push(`/festivals/${props.festival.id}`)
}
</script>

<template>
  <article class="festival-card">
    <button type="button" class="card-hit" :aria-label="`${festival.title} 상세 보기`" @click="openFestival"></button>

    <div class="thumb-wrap asset-placeholder">
      <span class="badge" :class="festival.status === '진행중' ? 'on' : 'soon'">
        {{ festival.status }}
      </span>
    </div>

    <div class="body">
      <h4>{{ festival.title }}</h4>
      <p>{{ festival.date }}</p>
      <p>{{ festival.place }}</p>

      <div class="bottom">
        <span class="price-tag" :class="festival.priceType === '무료' ? 'free' : 'paid'">
          {{ festival.priceType }}
        </span>
        <button
          type="button"
          class="bookmark-btn"
          :aria-label="bookmarked ? '북마크 해제' : '북마크 추가'"
          @click.stop="bookmarked = !bookmarked"
        >
          {{ bookmarked ? '●' : '○' }}
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.festival-card {
  position: relative;
  min-width: 0;
  overflow: hidden;
  border: 1px solid #e3e5de;
  border-radius: 16px;
  background: #fff;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.festival-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(48, 70, 59, 0.1);
}

.card-hit {
  position: absolute;
  inset: 0;
  z-index: 1;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.thumb-wrap {
  height: 170px;
  border: 0;
  border-radius: 0;
}

.thumb-wrap::after {
  content: '축제 썸네일';
}

.badge {
  position: absolute;
  z-index: 2;
  top: 10px;
  left: 10px;
  padding: 5px 9px;
  border-radius: var(--radius-pill);
  color: #fff;
  font-size: 11px;
  font-weight: 850;
}

.badge.on {
  background: var(--color-primary);
}

.badge.soon {
  background: var(--color-orange);
}

.body {
  padding: 12px 12px 10px;
}

h4 {
  min-height: 42px;
  margin: 0 0 8px;
  color: #24372e;
  font-size: 14px;
  line-height: 1.45;
  letter-spacing: -0.03em;
}

p {
  margin: 3px 0 0;
  color: #69776f;
  font-size: 11.5px;
}

.bottom {
  position: relative;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.price-tag {
  padding: 4px 8px;
  border-radius: var(--radius-pill);
  font-size: 10px;
  font-weight: 850;
}

.price-tag.free {
  background: #ebf7dc;
  color: #4b952c;
}

.price-tag.paid {
  background: #fff0df;
  color: #c3661d;
}

.bookmark-btn {
  position: relative;
  z-index: 4;
  width: 28px;
  height: 28px;
  border: 0;
  background: transparent;
  color: #758078;
  cursor: pointer;
  font-size: 18px;
}

@media (max-width: 1320px) {
  .thumb-wrap {
    height: 200px;
  }
}

@media (max-width: 760px) {
  .festival-card {
    flex: 0 0 230px;
  }

  .thumb-wrap {
    height: 160px;
  }
}
</style>

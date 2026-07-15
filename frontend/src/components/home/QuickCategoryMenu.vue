<script setup>
import { computed } from 'vue'
import iconToday from '../../assets/icons/icon-today.svg'
import iconWeekend from '../../assets/icons/icon-weekend.svg'
import iconFree from '../../assets/icons/icon-free.svg'
import iconPerformance from '../../assets/icons/icon-performance.svg'
import iconExhibition from '../../assets/icons/icon-exhibition.svg'
import iconTradition from '../../assets/icons/icon-tradition.svg'
import iconOutdoor from '../../assets/icons/icon-outdoor.svg'

const props = defineProps({
  modelValue: {
    type: String,
    default: '전체',
  },
})

const emit = defineEmits(['update:modelValue'])

const categories = [
  { label: '전체', icon: iconToday },
  { label: '다가오는 축제', icon: iconWeekend },
  { label: '무료 축제', icon: iconFree },
  { label: '공연', icon: iconPerformance },
  { label: '전시', icon: iconExhibition },
  { label: '전통', icon: iconTradition },
  { label: '야외 행사', icon: iconOutdoor },
]

const activeCategory = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})
</script>

<template>
  <section class="container quick-wrap section-card" aria-label="빠른 카테고리">
    <div class="quick-scroll" role="tablist">
      <button
        v-for="item in categories"
        :key="item.label"
        type="button"
        class="quick-item"
        :class="{ active: activeCategory === item.label }"
        :aria-selected="activeCategory === item.label"
        @click="activeCategory = item.label"
      >
        <img :src="item.icon" alt="" class="category-icon" aria-hidden="true" />
        <span>{{ item.label }}</span>
      </button>
    </div>
  </section>
</template>

<style scoped>
.quick-wrap {
  padding: 0 18px;
  border-radius: 18px;
  box-shadow: var(--shadow-float);
}

.quick-scroll {
  display: grid;
  grid-template-columns: repeat(7, minmax(120px, 1fr));
  overflow-x: auto;
  scrollbar-width: none;
}

.quick-scroll::-webkit-scrollbar {
  display: none;
}

.quick-item {
  position: relative;
  min-height: 68px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 11px;
  border: 0;
  background: transparent;
  color: #28392f;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  white-space: nowrap;
}

.quick-item + .quick-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 18px;
  bottom: 18px;
  width: 1px;
  background: #ecece4;
}

.icon-placeholder {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  border: 1.5px dashed var(--color-orange);
  border-radius: 9px;
  color: var(--color-orange);
  font-size: 10px;
  font-weight: 900;
}

.quick-item.active {
  color: var(--color-primary-dark);
}

.quick-item.active .icon-placeholder {
  border-style: solid;
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  color: var(--color-primary-dark);
}

@media (max-width: 980px) {
  .quick-scroll {
    grid-template-columns: repeat(7, 130px);
  }
}

@media (max-width: 560px) {
  .quick-wrap {
    padding: 0 8px;
  }

  .quick-scroll {
    grid-template-columns: repeat(7, 112px);
  }

  .quick-item {
    min-height: 62px;
    gap: 7px;
    font-size: 12px;
  }

  .category-icon {
  width: 48px;
  height: 48px;
  flex: 0 0 auto;
}
}
</style>

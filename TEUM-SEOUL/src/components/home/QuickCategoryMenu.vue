<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '오늘',
  },
})

const emit = defineEmits(['update:modelValue'])

const categories = [
  { label: '오늘', icon: '01' },
  { label: '이번 주말', icon: '02' },
  { label: '무료 축제', icon: '03' },
  { label: '공연', icon: '04' },
  { label: '전시', icon: '05' },
  { label: '전통', icon: '06' },
  { label: '야외 행사', icon: '07' },
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
        <span class="icon-placeholder" aria-hidden="true">{{ item.icon }}</span>
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
}
</style>

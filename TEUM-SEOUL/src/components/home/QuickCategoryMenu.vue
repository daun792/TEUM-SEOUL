<script setup>
import { ref } from 'vue'

const categories = ['오늘', '이번 주말', '무료 축제', '공연', '전시', '전통', '야외 행사']
const activeCategory = ref(categories[0])

const selectCategory = (item) => {
activeCategory.value = item
}
</script>

<template> <section class="quick-wrap container section-card"> <h3 class="title">빠르게 찾아보기</h3>
  <div class="quick-scroll" role="tablist" aria-label="빠른 카테고리">
    <button
      v-for="item in categories"
      :key="item"
      type="button"
      class="chip"
      :class="{ active: activeCategory === item }"
      @click="selectCategory(item)"
    >
      {{ item }}
    </button>
  </div>
</section>
</template> <style scoped> .quick-wrap { padding: 16px; display: grid; gap: 10px; } .title { margin: 0; font-size: 16px; color: #2a4a3f; } .quick-scroll { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 2px; scrollbar-width: thin; } .quick-scroll::-webkit-scrollbar { height: 8px; } .quick-scroll::-webkit-scrollbar-thumb { background: #dbe6da; border-radius: 999px; } .chip { flex: 0 0 auto; border: 1px solid var(--color-border); background: #fff; color: #365549; border-radius: var(--radius-pill); padding: 8px 14px; font-weight: 700; cursor: pointer; transition: all 0.2s ease; } .chip:hover { border-color: var(--color-primary); } .chip:focus-visible { outline: 2px solid var(--color-sky); outline-offset: 2px; } .chip.active { background: var(--color-primary); border-color: var(--color-primary); color: #fff; } </style>
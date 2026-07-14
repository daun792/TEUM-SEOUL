<script setup>
import { ref, watch } from 'vue'
import api, { getErrorMessage } from '../../services/api'

const emit = defineEmits(['select'])
const query = ref('')
const results = ref([])
const loading = ref(false)
const error = ref('')
let timer

async function search() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/api/performances', { params: { q: query.value, limit: 12 } })
    results.value = data.items
  } catch (e) {
    error.value = getErrorMessage(e, '공연 목록을 불러오지 못했습니다.')
  } finally {
    loading.value = false
  }
}

watch(query, () => {
  clearTimeout(timer)
  timer = setTimeout(search, 250)
})
search()

function choose(item) {
  query.value = item.name
  results.value = []
  emit('select', item)
}
</script>

<template>
  <section class="performance-search">
    <label class="field">
      <span>공연·축제를 검색하세요</span>
      <div class="search-input">
        <span aria-hidden="true">⌕</span>
        <input v-model="query" type="search" placeholder="예: 문학주간, 대학로, 서울" autocomplete="off" />
      </div>
    </label>
    <p v-if="loading" class="muted">공연 데이터를 찾는 중입니다.</p>
    <p v-else-if="error" class="form-error">{{ error }}</p>
    <div v-else-if="results.length" class="search-results">
      <button v-for="item in results" :key="item.id" type="button" @click="choose(item)">
        <span>
          <strong>{{ item.name }}</strong>
          <small>{{ item.address || '주소 정보 없음' }}</small>
        </span>
        <span aria-hidden="true">→</span>
      </button>
    </div>
    <p v-else-if="query" class="empty-inline">검색 결과가 없습니다.</p>
  </section>
</template>

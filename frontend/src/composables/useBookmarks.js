import { ref } from 'vue'

const KEY = 'teumSeoulBookmarks'
const readInitial = () => {
  try {
    const value = JSON.parse(localStorage.getItem(KEY) || '[]')
    return Array.isArray(value) ? value.map(Number).filter(Number.isInteger) : []
  } catch {
    return []
  }
}

const ids = ref(readInitial())

export function useBookmarks() {
  const persist = () => localStorage.setItem(KEY, JSON.stringify(ids.value))
  const toggle = (postId) => {
    const normalized = Number(postId)
    ids.value = ids.value.includes(normalized)
      ? ids.value.filter((id) => id !== normalized)
      : [...ids.value, normalized]
    persist()
  }
  const isBookmarked = (postId) => ids.value.includes(Number(postId))
  const removeMissing = (existingIds) => {
    const valid = new Set(existingIds.map(Number))
    ids.value = ids.value.filter((id) => valid.has(id))
    persist()
  }
  return { ids, toggle, isBookmarked, removeMissing }
}

import { requestJson } from './apiBase'

function formatDate(value) {
  if (!value) return '날짜 정보 없음'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '날짜 정보 없음'
  return date.toLocaleDateString('ko-KR')
}

function mapPost(item) {
  return {
    id: String(item.id),
    category: item.category || '자유',
    title: item.title,
    content: item.content,
    author: item.author,
    festivalId: item.festival_id || null,
    createdAt: formatDate(item.created_at),
    createdAtRaw: item.created_at,
    updatedAtRaw: item.updated_at,
  }
}

export async function getPostList(params = {}) {
  const search = new URLSearchParams()
  if (params.page) search.set('page', String(params.page))
  if (params.size) search.set('size', String(params.size))
  if (params.q) search.set('q', params.q)
  if (params.keyword) search.set('keyword', params.keyword)
  if (params.category) search.set('category', params.category)
  if (params.festivalId) search.set('festival_id', params.festivalId)
  const query = search.toString()

  const payload = await requestJson(`/api/posts${query ? `?${query}` : ''}`)
  const items = Array.isArray(payload?.items) ? payload.items.map(mapPost) : []

  return {
    items,
    total: payload?.total || 0,
    page: payload?.page || 1,
    size: payload?.size || params.size || 20,
    pages: payload?.pages || 0,
  }
}

export async function getPostById(id) {
  const payload = await requestJson(`/api/posts/${encodeURIComponent(String(id))}`)
  return mapPost(payload)
}

export async function createPost({ category, title, content, author, password, festivalId }) {
  const payload = await requestJson('/api/posts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      category,
      title,
      content,
      author,
      password,
      festival_id: festivalId || null,
    }),
  })
  return mapPost(payload)
}

export async function updatePost(id, { category, title, content, password, festivalId }) {
  const payload = await requestJson(`/api/posts/${encodeURIComponent(String(id))}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      category,
      title,
      content,
      password,
      festival_id: festivalId || null,
    }),
  })
  return mapPost(payload)
}

export async function deletePost(id, password) {
  await requestJson(`/api/posts/${encodeURIComponent(String(id))}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })
}

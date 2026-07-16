import { requestJson } from './apiBase'

function toNumberOrNull(value) {
  if (value === null || value === undefined || value === '') return null
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : null
}

function formatPeriod(startDate, endDate) {
  if (startDate && endDate) {
    if (startDate === endDate) return startDate
    return `${startDate} ~ ${endDate}`
  }
  return startDate || endDate || '일정 정보 없음'
}

function mapFestival(item) {
  return {
    id: String(item.content_id ?? item.id),
    title: item.title || item.name || '제목 없음',
    name: item.name || item.title || '이름 없음',
    start: item.event_start_date || null,
    end: item.event_end_date || null,
    period: item.period || formatPeriod(item.event_start_date, item.event_end_date),
    place: item.address || item.addr1 || '장소 정보 없음',
    description: item.overview || `${item.category || '축제'} 관련 장소입니다.`,
    imageUrl: item.image_url || item.thumbnail_url || '',
    lat: toNumberOrNull(item.lat ?? item.latitude),
    lng: toNumberOrNull(item.lng ?? item.longitude),
    category: item.category || '축제공연행사',
  }
}

function mapNearbyPlace(item) {
  return {
    id: String(item.content_id ?? item.id),
    title: item.title || item.name || '장소명 없음',
    category: item.category || '기타',
    address: item.address || item.addr1 || '주소 정보 없음',
    lat: toNumberOrNull(item.lat ?? item.latitude),
    lng: toNumberOrNull(item.lng ?? item.longitude),
    distanceKm: toNumberOrNull(item.distance_km),
  }
}

export async function getFestivalList(params = {}) {
  const search = new URLSearchParams()
  if (params.page) search.set('page', String(params.page))
  if (params.size) search.set('size', String(params.size))
  if (params.q) search.set('q', params.q)
  const query = search.toString()

  const payload = await requestJson(`/api/festivals${query ? `?${query}` : ''}`)
  return Array.isArray(payload?.items) ? payload.items.map(mapFestival) : []
}

export async function getFestivalById(id) {
  const payload = await requestJson(`/api/festivals/${encodeURIComponent(String(id))}`)
  return payload ? mapFestival(payload) : null
}

export async function getFestivalNearby(id, params = {}) {
  const search = new URLSearchParams()
  if (params.radiusKm) search.set('radius_km', String(params.radiusKm))
  if (params.categories?.length) search.set('categories', params.categories.join(','))
  if (params.limit) search.set('limit', String(params.limit))
  const query = search.toString()

  const payload = await requestJson(
    `/api/festivals/${encodeURIComponent(String(id))}/nearby${query ? `?${query}` : ''}`,
  )

  return {
    items: Array.isArray(payload?.items) ? payload.items.map(mapNearbyPlace) : [],
    total: payload?.total || 0,
  }
}

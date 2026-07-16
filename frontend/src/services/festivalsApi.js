import { requestJson } from './apiBase'
const toNumberOrNull = (value) => {
  if (value === null || value === undefined || value === '') return null
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : null
}
const formatPeriod = (start, end) => start && end ? (start === end ? start : `${start} ~ ${end}`) : start || end || '일정 정보 없음'
function mapFestival(item) {
  return {
    id: String(item.content_id ?? item.id), title: item.title || item.name || '제목 없음',
    name: item.name || item.title || '이름 없음', start: item.event_start_date || null,
    end: item.event_end_date || null, period: item.period || formatPeriod(item.event_start_date, item.event_end_date),
    place: item.address || item.addr1 || '장소 정보 없음', description: item.overview || `${item.category || '축제'} 관련 장소입니다.`,
    imageUrl: item.image_url || item.thumbnail_url || '', lat: toNumberOrNull(item.lat ?? item.latitude),
    lng: toNumberOrNull(item.lng ?? item.longitude), category: item.category || '축제공연행사',
  }
}
function mapNearbyPlace(item) {
  return {
    id: String(item.content_id ?? item.id), title: item.title || item.name || '장소명 없음',
    category: item.category || '기타', address: item.address || item.addr1 || '주소 정보 없음',
    lat: toNumberOrNull(item.lat ?? item.latitude), lng: toNumberOrNull(item.lng ?? item.longitude),
    distanceKm: toNumberOrNull(item.distance_km),
  }
}
export async function getFestivalList(params = {}) {
  const search = new URLSearchParams()
  if (params.page) search.set('page', String(params.page))
  if (params.size) search.set('size', String(params.size))
  if (params.q) search.set('q', params.q)
  if (params.startDate) search.set('start_date', params.startDate)
  if (params.endDate) search.set('end_date', params.endDate)
  const query = search.toString()
  const payload = await requestJson(`/api/festivals${query ? `?${query}` : ''}`)
  return Array.isArray(payload?.items) ? payload.items.map(mapFestival) : []
}
export async function getAllActiveFestivals(params = {}) {
  const all = []
  for (let page = 1; ; page += 1) {
    const items = await getFestivalList({ ...params, page, size: 100 })
    all.push(...items)
    if (items.length < 100) break
  }
  const today = new Date().toISOString().slice(0, 10)
  return all.filter((festival) => !festival.end || festival.end >= today)
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
  const payload = await requestJson(`/api/festivals/${encodeURIComponent(String(id))}/nearby${query ? `?${query}` : ''}`)
  return { items: Array.isArray(payload?.items) ? payload.items.map(mapNearbyPlace) : [], total: payload?.total || 0 }
}

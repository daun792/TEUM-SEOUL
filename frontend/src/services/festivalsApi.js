import { requestJson } from './apiBase'

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
    lat: item.lat ?? item.latitude ?? null,
    lng: item.lng ?? item.longitude ?? null,
    category: item.category || '축제공연행사',
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

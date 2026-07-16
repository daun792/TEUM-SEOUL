import { requestJson } from './apiBase'

function toFestival(item) {
  return {
    id: item.id,
    title: item.title,
    category: item.category,
    period: item.period || '일정 정보 없음',
    place: item.address || item.addr1 || '위치 정보 없음',
    address: item.address || item.addr1 || '',
    imageUrl: item.image_url || item.thumbnail_url || '',
    lat: item.latitude,
    lng: item.longitude,
    telephone: item.telephone || '',
    eventStartDate: item.event_start_date,
    eventEndDate: item.event_end_date,
  }
}

function toPlace(item) {
  return {
    id: item.id,
    title: item.title,
    type: item.category || '기타',
    lat: item.latitude,
    lng: item.longitude,
    address: item.address || item.addr1 || '',
    distanceKm: item.distance_km,
  }
}

export async function listFestivals(options = {}) {
  const params = new URLSearchParams()
  const page = options.page || 1
  const size = options.size || 50

  params.set('page', String(page))
  params.set('size', String(size))

  if (options.q) params.set('q', options.q)
  if (options.startDate) params.set('start_date', options.startDate)
  if (options.endDate) params.set('end_date', options.endDate)

  const payload = await requestJson(`/api/festivals?${params.toString()}`, options)
  return {
    ...payload,
    items: (payload.items || []).map(toFestival),
  }
}

export async function getFestivalById(contentId, options = {}) {
  const payload = await requestJson(`/api/festivals/${contentId}`, options)
  return toFestival(payload)
}

export async function getNearbyPlaces(contentId, options = {}) {
  const params = new URLSearchParams()
  if (typeof options.radiusKm === 'number') params.set('radius_km', String(options.radiusKm))
  if (typeof options.limit === 'number') params.set('limit', String(options.limit))
  if (options.categories) params.set('categories', options.categories)

  const query = params.toString()
  const payload = await requestJson(`/api/festivals/${contentId}/nearby${query ? `?${query}` : ''}`, options)
  return {
    ...payload,
    items: (payload.items || []).map(toPlace),
  }
}

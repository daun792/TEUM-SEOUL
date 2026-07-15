import { requestJson } from './apiBase'

function mapPlace(item) {
  return {
    id: String(item.content_id ?? item.id),
    name: item.name || item.title || '장소명 없음',
    title: item.title || item.name || '장소명 없음',
    type: item.category || '기타',
    lat: item.lat ?? item.latitude ?? null,
    lng: item.lng ?? item.longitude ?? null,
    address: item.address || item.addr1 || '',
    distanceKm: item.distance_km ?? null,
    contentTypeId: item.content_type_id || null,
  }
}

export async function getPlaces(params = {}) {
  const search = new URLSearchParams()
  if (params.page) search.set('page', String(params.page))
  if (params.size) search.set('size', String(params.size))
  if (params.q) search.set('q', params.q)
  if (params.category) search.set('category', params.category)
  if (params.contentTypeId) search.set('content_type_id', params.contentTypeId)
  if (typeof params.lat === 'number') search.set('lat', String(params.lat))
  if (typeof params.lng === 'number') search.set('lng', String(params.lng))
  if (typeof params.radiusKm === 'number') search.set('radius_km', String(params.radiusKm))

  const query = search.toString()
  const payload = await requestJson(`/api/places${query ? `?${query}` : ''}`)

  return {
    items: Array.isArray(payload?.items) ? payload.items.map(mapPlace) : [],
    total: payload?.total || 0,
    page: payload?.page || 1,
    size: payload?.size || params.size || 50,
    pages: payload?.pages || 0,
  }
}

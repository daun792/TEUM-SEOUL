import { requestJson } from './apiBase.js'

const DEFAULT_CACHE_TTL_MS = 60_000

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

export function mapFestival(item) {
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

function positiveInteger(value, fallback) {
  const parsed = Number(value)
  return Number.isInteger(parsed) && parsed > 0 ? parsed : fallback
}

export function buildFestivalPath(params = {}) {
  const search = new URLSearchParams()
  const keyword = String(params.q || '').trim()

  if (keyword) search.set('q', keyword)
  if (params.startDate) search.set('start_date', String(params.startDate))
  if (params.endDate) search.set('end_date', String(params.endDate))
  if (params.page) search.set('page', String(positiveInteger(params.page, 1)))
  if (params.size) search.set('size', String(positiveInteger(params.size, 20)))

  const query = search.toString()
  return `/api/festivals${query ? `?${query}` : ''}`
}

function normalizePage(payload, params = {}) {
  const items = Array.isArray(payload?.items) ? payload.items.map(mapFestival) : []
  const size = positiveInteger(payload?.size, positiveInteger(params.size, 20))
  const total = Math.max(0, Number(payload?.total) || 0)
  return {
    items,
    total,
    page: positiveInteger(payload?.page, positiveInteger(params.page, 1)),
    size,
    pages: Math.max(0, Number(payload?.pages) || Math.ceil(total / size)),
  }
}

export function createFestivalApiClient(
  requester = requestJson,
  { now = () => Date.now(), ttlMs = DEFAULT_CACHE_TTL_MS } = {},
) {
  const cache = new Map()
  const inFlight = new Map()

  async function loadPage(path, params, signal) {
    const options = signal ? { signal } : {}
    const payload = await requester(path, options)
    const result = normalizePage(payload, params)
    cache.set(path, { expiresAt: now() + ttlMs, result })
    return result
  }

  function getFestivalPage(params = {}, options = {}) {
    const path = buildFestivalPath(params)
    const forceRefresh = options.forceRefresh === true

    if (!forceRefresh) {
      const cached = cache.get(path)
      if (cached && cached.expiresAt > now()) return Promise.resolve(cached.result)
      if (cached) cache.delete(path)

      if (!options.signal && inFlight.has(path)) return inFlight.get(path)
    }

    const promise = loadPage(path, params, options.signal)

    if (!options.signal) {
      inFlight.set(path, promise)
      promise.finally(() => {
        if (inFlight.get(path) === promise) inFlight.delete(path)
      }).catch(() => {})
    }

    return promise
  }

  async function getFestivalList(params = {}, options = {}) {
    const page = await getFestivalPage(params, options)
    return page.items
  }

  function clearFestivalCache() {
    cache.clear()
    inFlight.clear()
  }

  return { getFestivalPage, getFestivalList, clearFestivalCache }
}

const festivalClient = createFestivalApiClient()

export const getFestivalPage = festivalClient.getFestivalPage
export const getFestivalList = festivalClient.getFestivalList
export const clearFestivalCache = festivalClient.clearFestivalCache

export async function getFestivalById(id, options = {}) {
  const payload = await requestJson(`/api/festivals/${encodeURIComponent(String(id))}`, options)
  return payload ? mapFestival(payload) : null
}

export async function getFestivalNearby(id, params = {}, options = {}) {
  const search = new URLSearchParams()
  if (params.radiusKm) search.set('radius_km', String(params.radiusKm))
  if (params.categories?.length) search.set('categories', params.categories.join(','))
  if (params.limit) search.set('limit', String(params.limit))
  const query = search.toString()

  const payload = await requestJson(
    `/api/festivals/${encodeURIComponent(String(id))}/nearby${query ? `?${query}` : ''}`,
    options,
  )

  return {
    items: Array.isArray(payload?.items) ? payload.items.map(mapNearbyPlace) : [],
    total: payload?.total || 0,
  }
}

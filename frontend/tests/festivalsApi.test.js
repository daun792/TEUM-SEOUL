import test from 'node:test'
import assert from 'node:assert/strict'
import { createFestivalApiClient } from '../src/services/festivalsApi.js'

function payload(overrides = {}) {
  return {
    items: [
      {
        content_id: 'SC1',
        title: '서울 문화행사',
        event_start_date: '2026-07-16',
        event_end_date: '2026-07-18',
        address: '서울특별시 마포구',
        latitude: 37.5,
        longitude: 126.9,
      },
    ],
    total: 31,
    page: 2,
    size: 24,
    pages: 2,
    ...overrides,
  }
}

test('serializes search, date range, and pagination in a stable order', async () => {
  const calls = []
  const client = createFestivalApiClient(async (path, options) => {
    calls.push({ path, options })
    return payload()
  })

  await client.getFestivalPage({
    q: '  클래식 ',
    startDate: '2026-07-16',
    endDate: '2026-10-14',
    page: 2,
    size: 24,
  })

  assert.equal(
    calls[0].path,
    '/api/festivals?q=%ED%81%B4%EB%9E%98%EC%8B%9D&start_date=2026-07-16&end_date=2026-10-14&page=2&size=24',
  )
})

test('returns mapped items with pagination metadata', async () => {
  const client = createFestivalApiClient(async () => payload())
  const result = await client.getFestivalPage({ page: 2, size: 24 })

  assert.equal(result.total, 31)
  assert.equal(result.page, 2)
  assert.equal(result.pages, 2)
  assert.deepEqual(result.items[0], {
    id: 'SC1',
    title: '서울 문화행사',
    name: '서울 문화행사',
    start: '2026-07-16',
    end: '2026-07-18',
    period: '2026-07-16 ~ 2026-07-18',
    place: '서울특별시 마포구',
    description: '축제 관련 장소입니다.',
    imageUrl: '',
    lat: 37.5,
    lng: 126.9,
    category: '축제공연행사',
  })
})

test('shares an identical in-flight request when no AbortSignal is supplied', async () => {
  let resolveRequest
  let callCount = 0
  const requester = () => {
    callCount += 1
    return new Promise((resolve) => { resolveRequest = resolve })
  }
  const client = createFestivalApiClient(requester)

  const first = client.getFestivalPage({ page: 1, size: 24 })
  const second = client.getFestivalPage({ page: 1, size: 24 })
  assert.equal(callCount, 1)

  resolveRequest(payload({ page: 1 }))
  assert.deepEqual(await first, await second)
})

test('reuses a successful response within the 60-second TTL', async () => {
  let now = 1_000
  let callCount = 0
  const client = createFestivalApiClient(
    async () => {
      callCount += 1
      return payload({ page: 1 })
    },
    { now: () => now, ttlMs: 60_000 },
  )

  await client.getFestivalPage({ page: 1 })
  now += 59_999
  await client.getFestivalPage({ page: 1 })
  assert.equal(callCount, 1)

  now += 2
  await client.getFestivalPage({ page: 1 })
  assert.equal(callCount, 2)
})

test('forceRefresh bypasses a cached response', async () => {
  let callCount = 0
  const client = createFestivalApiClient(async () => {
    callCount += 1
    return payload({ page: 1 })
  })

  await client.getFestivalPage({ page: 1 })
  await client.getFestivalPage({ page: 1 }, { forceRefresh: true })
  assert.equal(callCount, 2)
})

test('does not cache rejected requests and forwards AbortSignal', async () => {
  const controller = new AbortController()
  const seenSignals = []
  let callCount = 0
  const client = createFestivalApiClient(async (_path, options) => {
    callCount += 1
    seenSignals.push(options.signal)
    if (callCount === 1) throw new Error('temporary')
    return payload({ page: 1 })
  })

  await assert.rejects(
    client.getFestivalPage({ page: 1 }, { signal: controller.signal }),
    /temporary/,
  )
  await client.getFestivalPage({ page: 1 }, { signal: controller.signal })

  assert.equal(callCount, 2)
  assert.equal(seenSignals[0], controller.signal)
  assert.equal(seenSignals[1], controller.signal)
})

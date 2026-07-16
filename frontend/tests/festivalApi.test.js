import test from 'node:test'
import assert from 'node:assert/strict'

import { getNearbyPlaces, listFestivals } from '../src/services/festivalApi.js'

test('listFestivals maps backend payload to frontend fields', async () => {
  const fetchImpl = async () => ({
    ok: true,
    async json() {
      return {
        items: [
          {
            id: 'festival-1',
            title: '서울 여름 음악축제',
            category: '축제공연행사',
            period: '2026-07-20 ~ 2026-07-22',
            address: '서울특별시 중구 세종대로 110',
            image_url: 'https://example.com/festival.jpg',
            latitude: 37.5663,
            longitude: 126.9779,
            event_start_date: '2026-07-20',
            event_end_date: '2026-07-22',
          },
        ],
        total: 1,
        page: 1,
        size: 50,
        pages: 1,
      }
    },
  })

  const payload = await listFestivals({ fetchImpl, baseUrl: 'https://api.example.com' })

  assert.equal(payload.items[0].title, '서울 여름 음악축제')
  assert.equal(payload.items[0].place, '서울특별시 중구 세종대로 110')
  assert.equal(payload.items[0].lat, 37.5663)
})

test('getNearbyPlaces keeps distance and category fields', async () => {
  const fetchImpl = async () => ({
    ok: true,
    async json() {
      return {
        festival_id: 'festival-1',
        radius_km: 2,
        total: 1,
        items: [
          {
            id: 'place-1',
            title: '덕수궁',
            category: '관광지',
            latitude: 37.5658,
            longitude: 126.9751,
            distance_km: 0.321,
          },
        ],
      }
    },
  })

  const payload = await getNearbyPlaces('festival-1', {
    fetchImpl,
    baseUrl: 'https://api.example.com',
    radiusKm: 2,
  })

  assert.equal(payload.items[0].type, '관광지')
  assert.equal(payload.items[0].distanceKm, 0.321)
})

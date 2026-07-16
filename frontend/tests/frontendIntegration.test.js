import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'

async function source(path) {
  return readFile(new URL(path, import.meta.url), 'utf8')
}

test('festival list uses upcoming defaults, debounced search, explicit past toggle, and pagination', async () => {
  const text = await source('../src/views/FestivalListView.vue')
  assert.match(text, /SEARCH_DEBOUNCE_MS\s*=\s*300/)
  assert.match(text, /PAGE_SIZE\s*=\s*24/)
  assert.match(text, /지난 행사 포함/)
  assert.match(text, /startDate:\s*includePast\.value\s*\?\s*undefined\s*:\s*todayIso\(\)/)
  assert.match(text, /getFestivalPage/)
  assert.match(text, /datesSet/)
  assert.match(text, /retry/)
  assert.doesNotMatch(text, /size:\s*60/)
  assert.doesNotMatch(text, /2026-07-18/)
})

test('home list requests a 90-day active and upcoming window with explicit request states', async () => {
  const text = await source('../src/components/home/WeeklyFestivalSection.vue')
  assert.match(text, /addDaysIso\(startDate,\s*90\)/)
  assert.match(text, /startDate/)
  assert.match(text, /endDate/)
  assert.match(text, /waking/)
  assert.match(text, /retry/)
})

test('home calendar loads its visible range and has no hard-coded 2026 date', async () => {
  const text = await source('../src/components/home/FestivalCalendarSection.vue')
  assert.match(text, /datesSet/)
  assert.match(text, /calendarRange/)
  assert.match(text, /startDate/)
  assert.match(text, /endDate/)
  assert.doesNotMatch(text, /2026-07-18/)
  assert.doesNotMatch(text, /size:\s*300/)
})

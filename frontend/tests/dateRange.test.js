import test from 'node:test'
import assert from 'node:assert/strict'
import {
  addDaysIso,
  calendarRange,
  formatLocalDate,
  monthRange,
  todayIso,
} from '../src/utils/dateRange.js'

test('formatLocalDate keeps the local calendar date', () => {
  const localDate = new Date(2026, 6, 16, 23, 30)
  assert.equal(formatLocalDate(localDate), '2026-07-16')
})

test('todayIso accepts an injected clock', () => {
  assert.equal(todayIso(new Date(2026, 6, 16, 8, 0)), '2026-07-16')
})

test('addDaysIso builds an upcoming 90-day window', () => {
  assert.equal(addDaysIso('2026-07-16', 90), '2026-10-14')
})

test('monthRange handles leap-year February', () => {
  assert.deepEqual(monthRange(new Date(2028, 1, 12)), {
    startDate: '2028-02-01',
    endDate: '2028-02-29',
  })
})

test('calendarRange converts FullCalendar exclusive end to inclusive API end', () => {
  assert.deepEqual(
    calendarRange(new Date(2026, 5, 28), new Date(2026, 7, 9)),
    { startDate: '2026-06-28', endDate: '2026-08-08' },
  )
})

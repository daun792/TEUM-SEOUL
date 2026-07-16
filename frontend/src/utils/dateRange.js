function pad2(value) {
  return String(value).padStart(2, '0')
}

export function formatLocalDate(date) {
  if (!(date instanceof Date) || Number.isNaN(date.getTime())) {
    throw new TypeError('date must be a valid Date')
  }
  return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}`
}

export function todayIso(now = new Date()) {
  return formatLocalDate(now)
}

function parseIsoDate(isoDate) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(isoDate || ''))
  if (!match) throw new TypeError('isoDate must use YYYY-MM-DD')
  const [, year, month, day] = match
  const date = new Date(Number(year), Number(month) - 1, Number(day))
  if (
    date.getFullYear() !== Number(year)
    || date.getMonth() !== Number(month) - 1
    || date.getDate() !== Number(day)
  ) {
    throw new RangeError('isoDate is not a valid calendar date')
  }
  return date
}

export function addDaysIso(isoDate, days) {
  const date = parseIsoDate(isoDate)
  date.setDate(date.getDate() + Number(days))
  return formatLocalDate(date)
}

export function monthRange(date = new Date()) {
  if (!(date instanceof Date) || Number.isNaN(date.getTime())) {
    throw new TypeError('date must be a valid Date')
  }
  const start = new Date(date.getFullYear(), date.getMonth(), 1)
  const end = new Date(date.getFullYear(), date.getMonth() + 1, 0)
  return { startDate: formatLocalDate(start), endDate: formatLocalDate(end) }
}

export function calendarRange(start, exclusiveEnd) {
  if (!(start instanceof Date) || Number.isNaN(start.getTime())) {
    throw new TypeError('start must be a valid Date')
  }
  if (!(exclusiveEnd instanceof Date) || Number.isNaN(exclusiveEnd.getTime())) {
    throw new TypeError('exclusiveEnd must be a valid Date')
  }
  const inclusiveEnd = new Date(exclusiveEnd)
  inclusiveEnd.setDate(inclusiveEnd.getDate() - 1)
  return {
    startDate: formatLocalDate(start),
    endDate: formatLocalDate(inclusiveEnd),
  }
}

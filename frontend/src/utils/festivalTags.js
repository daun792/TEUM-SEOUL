function parseDate(value) {
  if (!value) return null
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? null : date
}

function getThisWeekendRange(today) {
  const day = today.getDay()
  const saturdayDiff = (6 - day + 7) % 7
  const sundayDiff = (7 - day + 7) % 7

  const saturday = new Date(today)
  saturday.setDate(today.getDate() + saturdayDiff)
  saturday.setHours(0, 0, 0, 0)

  const sunday = new Date(today)
  sunday.setDate(today.getDate() + sundayDiff)
  sunday.setHours(23, 59, 59, 999)

  return { saturday, sunday }
}

export function getFestivalStatus(festival) {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const start = parseDate(festival.start)
  const end = parseDate(festival.end || festival.start)

  if (!start || !end) return '예정'
  if (today < start) return '예정'
  if (today > end) return '종료'
  return '진행중'
}

export function getFestivalTags(festival) {
  const tags = new Set()
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const start = parseDate(festival.start)
  const end = parseDate(festival.end || festival.start)
  const title = String(festival.title || '')

  tags.add('전체')

  if (start && start > now) {
    tags.add('다가오는 축제')
  }

  if (start && end) {
    const { saturday, sunday } = getThisWeekendRange(now)
    if (start <= sunday && end >= saturday) {
      tags.add('이번 주말')
    }
  }

  if (/무료/.test(title)) tags.add('무료 축제')
  if (/공연|콘서트|뮤직|음악/.test(title)) tags.add('공연')
  if (/전시|아트|미술/.test(title)) tags.add('전시')
  if (/전통|한옥|궁|민속/.test(title)) tags.add('전통')
  if (/야외|한강|공원|광장/.test(title)) tags.add('야외 행사')

  return [...tags]
}

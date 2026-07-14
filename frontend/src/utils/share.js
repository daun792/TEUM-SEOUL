export function buildShareUrl(course, origin = window.location.origin) {
  const query = new URLSearchParams({
    performanceId: String(course.performance.id),
    phase: course.phase,
    minutes: String(course.available_minutes),
    category: course.preferred_category,
    placeIds: course.places.map((place) => place.id).join(','),
  })
  return `${origin}/course/shared?${query.toString()}`
}

export async function shareCourse(course, origin = window.location.origin) {
  const url = buildShareUrl(course, origin)
  const data = {
    title: '틈서울 초단기 코스',
    text: `${course.performance.name} 전후 코스를 확인해보세요.`,
    url,
  }
  if (navigator.share) {
    await navigator.share(data)
    return 'shared'
  }
  await navigator.clipboard.writeText(url)
  return 'copied'
}

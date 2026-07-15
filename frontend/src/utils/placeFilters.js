export const MAP_FILTERS = ['전체', '축제', '관광지', '문화시설', '쇼핑', '체험', '반경 2km']

export function toApiCategory(filter) {
  if (filter === '전체') return null
  if (filter === '축제') return '축제'
  if (filter === '반경 2km') return null
  if (filter === '체험') return '체험'
  return filter
}

export function placeTypeLabel(place) {
  if (!place?.type) return '기타'
  if (place.type === '축제공연행사') return '축제'
  if (place.type === '레포츠') return '체험'
  return place.type
}

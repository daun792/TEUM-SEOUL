export const festivals = [
  {
    id: '1',
    title: '서울 여름 음악축제',
    name: '서울 여름 음악축제',
    start: '2026-07-20',
    end: '2026-07-22',
    period: '2026-07-20 ~ 2026-07-22',
    place: '서울광장',
    description: '도심에서 즐기는 야외 음악 페스티벌',
    imageUrl: 'https://picsum.photos/900/420?random=11',
    lat: 37.5663,
    lng: 126.9779,
  },
  {
    id: '2',
    title: '한강 야간 문화축제',
    name: '한강 야간 문화축제',
    start: '2026-07-25',
    period: '2026-07-25',
    place: '여의도 한강공원',
    description: '한강 야경과 함께하는 문화 공연',
    imageUrl: 'https://picsum.photos/900/420?random=12',
    lat: 37.5288,
    lng: 126.9326,
  },
  {
    id: '3',
    title: '전통예술 거리축제',
    name: '전통예술 거리축제',
    start: '2026-08-02',
    period: '2026-08-02',
    place: '인사동 거리',
    description: '전통 공연과 공예 체험이 있는 거리 축제',
    imageUrl: 'https://picsum.photos/900/420?random=13',
    lat: 37.5742,
    lng: 126.985,
  },
]

export const getFestivalList = async () => {
return festivals
}

export const getFestivalById = async (id) => {
return festivals.find((item) => item.id === String(id)) || null
}
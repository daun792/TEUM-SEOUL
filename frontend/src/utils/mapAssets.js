import L from 'leaflet'
import filterAll from '../assets/ui/filter-icons/filter-all.png'
import filterFestival from '../assets/ui/filter-icons/filter-festival.png'
import filterPerformance from '../assets/ui/filter-icons/filter-performance.png'
import filterExhibition from '../assets/ui/filter-icons/filter-exhibition.png'
import filterExperience from '../assets/ui/filter-icons/filter-experience.png'
import filterTradition from '../assets/ui/filter-icons/filter-tradition.png'
import filterOutdoor from '../assets/ui/filter-icons/filter-outdoor.png'
import filterTour from '../assets/ui/filter-icons/filter-tour.png'
import filterCulture from '../assets/ui/filter-icons/filter-culture.png'
import filterShopping from '../assets/ui/filter-icons/filter-shopping.png'
import markerDefault from '../assets/ui/map-markers/marker-default.png'
import markerFestival from '../assets/ui/map-markers/marker-festival.png'
import markerPerformance from '../assets/ui/map-markers/marker-performance.png'
import markerExhibition from '../assets/ui/map-markers/marker-exhibition.png'
import markerExperience from '../assets/ui/map-markers/marker-experience.png'
import markerTradition from '../assets/ui/map-markers/marker-tradition.png'
import markerOutdoor from '../assets/ui/map-markers/marker-outdoor.png'
import markerTour from '../assets/ui/map-markers/marker-tour.png'
import markerCulture from '../assets/ui/map-markers/marker-culture.png'
import markerShopping from '../assets/ui/map-markers/marker-shopping.png'

const aliases = { 축제공연행사:'축제', 레포츠:'체험', 기타:'전체' }
export const filterIcons = { 전체:filterAll,축제:filterFestival,공연:filterPerformance,전시:filterExhibition,체험:filterExperience,전통:filterTradition,'야외 행사':filterOutdoor,관광지:filterTour,문화시설:filterCulture,쇼핑:filterShopping }
const markerImages = { 전체:markerDefault,축제:markerFestival,공연:markerPerformance,전시:markerExhibition,체험:markerExperience,전통:markerTradition,'야외 행사':markerOutdoor,관광지:markerTour,문화시설:markerCulture,쇼핑:markerShopping }
export const assetType = (type) => aliases[type] || type || '전체'
export const filterIconFor = (type) => filterIcons[assetType(type)] || filterAll
export const leafletIconFor = (type) => L.icon({ iconUrl:markerImages[assetType(type)]||markerDefault,iconSize:[36,45],iconAnchor:[18,44],popupAnchor:[0,-40] })

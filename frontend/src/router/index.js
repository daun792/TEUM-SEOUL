import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FestivalListView from '../views/FestivalListView.vue'
import FestivalDetailView from '../views/FestivalDetailView.vue'
import MapView from '../views/MapView.vue'
import BoardListView from '../views/BoardListView.vue'
import BoardDetailView from '../views/BoardDetailView.vue'
import BoardWriteView from '../views/BoardWriteView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/festivals', name: 'festival-list', component: FestivalListView },
  { path: '/festivals/:id', name: 'festival-detail', component: FestivalDetailView, props: true },
  { path: '/map', name: 'map', component: MapView },
  { path: '/board', name: 'board-list', component: BoardListView },
  { path: '/board/write', name: 'board-write', component: BoardWriteView },
  { path: '/board/edit/:id', name: 'board-edit', component: BoardWriteView, props: true },
  { path: '/board/:id', name: 'board-detail', component: BoardDetailView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router

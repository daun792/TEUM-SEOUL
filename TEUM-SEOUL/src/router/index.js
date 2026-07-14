import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import FestivalDetailView from '../views/FestivalDetailView.vue'
import BoardListView from '../views/BoardListView.vue'
import BoardDetailView from '../views/BoardDetailView.vue'
import BoardWriteView from '../views/BoardWriteView.vue'
import AboutView from '../views/AboutView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/festivals/:id',
    name: 'festival-detail',
    component: FestivalDetailView,
    props: true,
  },
  {
    path: '/board',
    name: 'board-list',
    component: BoardListView,
  },
  {
    path: '/board/:id',
    name: 'board-detail',
    component: BoardDetailView,
    props: true,
  },
  {
    path: '/board/write',
    name: 'board-write',
    component: BoardWriteView,
  },
  {
    path: '/board/edit/:id',
    name: 'board-edit',
    component: BoardWriteView,
    props: true,
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
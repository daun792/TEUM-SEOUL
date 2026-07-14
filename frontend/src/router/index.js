import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/gap', component: () => import('../views/GapFormView.vue') },
  { path: '/course/result', component: () => import('../views/CourseResultView.vue') },
  { path: '/course/shared', component: () => import('../views/CourseResultView.vue'), props: { shared: true } },
  { path: '/posts', component: () => import('../views/PostListView.vue') },
  { path: '/posts/new', component: () => import('../views/PostFormView.vue') },
  { path: '/posts/:id', component: () => import('../views/PostDetailView.vue') },
  { path: '/posts/:id/edit', component: () => import('../views/PostFormView.vue') },
  { path: '/bookmarks', component: () => import('../views/BookmarksView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

export default router

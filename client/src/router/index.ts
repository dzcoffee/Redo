import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import MainLayout from '@/views/MainLayout.vue'

const subRoutes: RouteRecordRaw[] = [
  { path: '/memo', name: 'Memo', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'memo/create', name: 'MemoCreate', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'memo/edit', name: 'MemoEdit', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'memo/:id', name: 'MemoView', component: () => import('@/views/memo/MainPage.vue') },
  { path: '/quiz', name: 'Quiz', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'quiz/create', name: 'QuizCreate', component: MainLayout },
  { path: 'quiz/game', name: 'QuizGame', component: MainLayout },
  { path: 'quiz/archive', name: 'QuizArchive', component: MainLayout }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainLayout,
      children: subRoutes
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginPage.vue') // Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: MainLayout // SignUp
    },
    {
      name: 'NotFound',
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router

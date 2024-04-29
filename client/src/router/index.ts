import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import LayoutPage from '@/views/LayoutPage.vue'

const subRoutes: RouteRecordRaw[] = [
  { path: '/memo', name: 'Memo', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'memo/create', name: 'MemoCreate', component: () => import('@/views/memo/MemoCreatePage.vue') },
  { path: 'memo/edit', name: 'MemoEdit', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'memo/:id', name: 'MemoView', component: () => import('@/views/memo/MemoPage.vue') },
  { path: '/quiz', name: 'Quiz', component: () => import('@/views/quiz/QuizSettingPage.vue') },
  { path: 'quiz/create', name: 'QuizCreate', component: LayoutPage },
  { path: 'quiz/game', name: 'QuizGame', component: () => import('@/views/quiz/QuizPage.vue') },
  { path: 'quiz/archive', name: 'QuizArchive', component: LayoutPage }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LayoutPage,
      children: subRoutes,
      redirect: '/memo'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginPage.vue') // Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/SignUpPage.vue')
    },
    {
      name: 'NotFound',
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import LayoutPage from '@/views/LayoutPage.vue'
import { useAuthStore } from '@/stores/authStore'

const subRoutes: RouteRecordRaw[] = [
  { path: '/memo', name: 'Memo', component: () => import('@/views/memo/MainPage.vue') },
  {
    path: 'memo/create',
    name: 'MemoCreate',
    component: () => import('@/views/memo/MemoCreatePage.vue')
  },
  { path: 'memo/edit', name: 'MemoEdit', component: () => import('@/views/memo/MainPage.vue') },
  { path: 'memo/:id', name: 'MemoView', component: () => import('@/views/memo/MemoPage.vue') },
  { path: '/quiz', name: 'Quiz', component: () => import('@/views/quiz/QuizSettingPage.vue') },
  { path: 'quiz/game', name: 'QuizGame', component: () => import('@/views/quiz/QuizPage.vue') }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LayoutPage,
      children: subRoutes,
      redirect: '/login',
      meta: { requiresAuth: true }
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

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  if (to.matched.some((record) => record.meta.requiresAuth) && !authStore.isAuthenticated) {
    router.replace('/login')
    next()
  } else {
    next()
  }
})

export default router

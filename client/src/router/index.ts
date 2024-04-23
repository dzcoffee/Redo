import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const subRoutes: RouteRecordRaw[] = [
  { path: '/memo', name: 'Memo', component: HomeView },
  { path: 'memo/create', name: 'MemoCreate', component: HomeView },
  { path: 'memo/edit', name: 'MemoEdit', component: HomeView },
  { path: 'memo/:id', name: 'MemoView', component: HomeView },
  { path: '/quiz', name: 'Quiz', component: HomeView },
  { path: 'quiz/create', name: 'QuizCreate', component: HomeView },
  { path: 'quiz/game', name: 'QuizGame', component: HomeView },
  { path: 'quiz/archive', name: 'QuizArchive', component: HomeView }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: subRoutes
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/MainPage.vue') // Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: HomeView // SignUp
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      name: 'NotFound',
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router

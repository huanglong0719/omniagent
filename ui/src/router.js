import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('./pages/Dashboard.vue')
  },
  {
    path: '/skills',
    name: 'Skills',
    component: () => import('./pages/Skills.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('./pages/Settings.vue')
  },
  {
    path: '/monitoring',
    name: 'Monitoring',
    component: () => import('./pages/Monitoring.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
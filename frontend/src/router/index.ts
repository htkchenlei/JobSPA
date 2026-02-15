import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../components/Layout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: Layout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('../views/Dashboard.vue')
        },
        {
          path: 'project-management',
          name: 'projectManagement',
          component: () => import('../views/ProjectManagement.vue')
        },
        {
          path: 'advanced-search',
          name: 'advancedSearch',
          component: () => import('../views/AdvancedSearch.vue')
        },
        {
          path: 'statistics',
          name: 'statistics',
          component: () => import('../views/Statistics.vue')
        },
        {
          path: 'todos',
          name: 'todos',
          component: () => import('../views/Todos.vue')
        },
        {
          path: 'file-management',
          name: 'fileManagement',
          component: () => import('../views/FileManagement.vue')
        },

        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/Settings.vue')
        },
        {
          path: 'api-documentation',
          name: 'apiDocumentation',
          component: () => import('../views/ApiDocumentation.vue')
        },
        {
          path: 'work-log',
          name: 'workLog',
          component: () => import('../views/WorkLog.vue')
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  
  // 检查用户是否已登录（通过localStorage中的token）
  const isLoggedIn = localStorage.getItem('token') !== null
  
  if (requiresAuth && !isLoggedIn) {
    // 需要认证但未登录，重定向到登录页面
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    // 已登录但尝试访问登录页面，重定向到仪表板
    next('/dashboard')
  } else {
    // 其他情况，正常导航
    next()
  }
})

export default router
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
          path: 'work-log',
          name: 'workLog',
          component: () => import('../views/WorkLog.vue')
        },
        {
          path: 'bid-tool',
          name: 'bidTool',
          component: () => import('../views/BidTool.vue')
        },

      ]
    }
  ]
})

// 检查token是否过期
function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp < Date.now() / 1000
  } catch (error) {
    return true
  }
}

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)
  
  // 检查用户是否已登录（通过sessionStorage中的token）
  const token = sessionStorage.getItem('token')
  const isLoggedIn = token !== null && !isTokenExpired(token)
  
  if (requiresAuth && !isLoggedIn) {
    // 需要认证但未登录或token已过期，重定向到登录页面
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('user')
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
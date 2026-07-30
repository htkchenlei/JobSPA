<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="logo">
        <div class="logo-icon-wrapper">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <transition name="fade">
          <span v-if="!sidebarCollapsed" class="logo-text">JobSPA</span>
        </transition>
      </div>
      <nav class="menu">
        <router-link to="/dashboard" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="7" height="7" rx="2" stroke="currentColor" stroke-width="2"/>
              <rect x="14" y="3" width="7" height="7" rx="2" stroke="currentColor" stroke-width="2"/>
              <rect x="3" y="14" width="7" height="7" rx="2" stroke="currentColor" stroke-width="2"/>
              <rect x="14" y="14" width="7" height="7" rx="2" stroke="currentColor" stroke-width="2"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">仪表盘</span>
          </transition>
        </router-link>
        
        <router-link to="/project-management" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <rect x="9" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="2"/>
              <path d="M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M9 16H13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">项目管理</span>
          </transition>
        </router-link>
        
        <router-link to="/advanced-search" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="11" cy="11" r="6" stroke="currentColor" stroke-width="2"/>
              <path d="M20 20L15.5 15.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">高级查询</span>
          </transition>
        </router-link>
        
        <router-link to="/statistics" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 20V10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M12 20V4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M6 20V14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">统计分析</span>
          </transition>
        </router-link>
        
        <router-link to="/todos" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="4" y="4" width="16" height="16" rx="3" stroke="currentColor" stroke-width="2"/>
              <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">待办事项</span>
          </transition>
        </router-link>
        
        <router-link to="/file-management" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 7V17C4 19.2091 5.79086 21 8 21H16C18.2091 21 20 19.2091 20 17V9C20 7.89543 19.1046 7 18 7H13L11 5H6C4.89543 5 4 5.89543 4 7Z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">文件管理</span>
          </transition>
        </router-link>

        <router-link to="/work-log" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="4" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
              <path d="M16 2V6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M8 2V6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M3 10H21" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="16" r="2" stroke="currentColor" stroke-width="2"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">工作日志</span>
          </transition>
        </router-link>
        
        <router-link to="/bid-tool" class="menu-item">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="12" r="1" fill="currentColor"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">投标工具</span>
          </transition>
        </router-link>
        
        <div class="menu-divider"></div>
        
        <div class="menu-item user-profile" @click="changePassword">
          <span class="menu-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="2"/>
              <path d="M4 20C4 16.6863 7.13401 14 11 14H13C16.866 14 20 16.6863 20 20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </span>
          <transition name="fade">
            <span v-if="!sidebarCollapsed" class="menu-text">{{ userName }}</span>
          </transition>
        </div>
      </nav>
    </aside>
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <header class="header">
        <div class="header-left">
          <button class="toggle-sidebar" @click="toggleSidebar">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 6H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M4 12H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M4 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <h2>{{ currentRouteName }}</h2>
        </div>
        <div class="header-right">
          <button class="btn btn-secondary" @click="logout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 17L21 12L16 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>登出</span>
          </button>
        </div>
      </header>
      <div class="content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const sidebarCollapsed = ref(false)

// 获取用户名
const userName = computed(() => {
  const userStr = sessionStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      return user.username || '用户'
    } catch (e) {
      return '用户'
    }
  }
  return '用户'
})

// 计算当前路由名称
const currentRouteName = computed(() => {
    const routeMap: Record<string, string> = {
      '/dashboard': '仪表盘',
      '/project-management': '项目管理',
      '/advanced-search': '高级查询',
      '/statistics': '统计分析',
      '/todos': '待办事项',
      '/file-management': '文件管理',
      '/work-log': '工作日志',
      '/bid-tool': '投标工具',
      '/settings': '个人设置'
    }
    return routeMap[route.path] || '仪表盘'
  })

// 切换侧边栏
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// 修改密码
const changePassword = () => {
  router.push('/settings')
}

// 登出
const logout = () => {
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 侧边栏样式 - 马卡龙风格 */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #A8E6CF 0%, #88D8B0 50%, #7DD3C0 100%);
  color: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 4px 0 20px rgba(168, 230, 207, 0.3);
  position: relative;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, transparent, rgba(255,255,255,0.3), transparent);
}

.sidebar.collapsed {
  width: 80px;
}

.logo {
  padding: 24px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.logo-icon-wrapper {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  backdrop-filter: blur(10px);
}

.logo-icon {
  width: 24px;
  height: 24px;
  color: white;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.menu {
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 12px;
  gap: 12px;
  position: relative;
  overflow: hidden;
}

.menu-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0);
  transition: all 0.3s ease;
  border-radius: 12px;
}

.menu-item:hover {
  color: white;
}

.menu-item:hover::before {
  background: rgba(255, 255, 255, 0.15);
}

.menu-item.router-link-active {
  background: linear-gradient(135deg, #FF9A8B 0%, #FFB7B2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 154, 139, 0.4);
}

.menu-item.router-link-active::before {
  display: none;
}

.menu-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-icon svg {
  width: 100%;
  height: 100%;
  stroke: currentColor;
}

.menu-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.menu-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.2);
  margin: 12px 16px;
}

/* 用户资料样式 */
.user-profile {
  cursor: pointer;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: linear-gradient(135deg, #FFF9F5 0%, #FFF5EE 100%);
}

.header {
  background: white;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.04);
  border-bottom: 1px solid rgba(168, 230, 207, 0.2);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.toggle-sidebar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #A8E6CF 0%, #88D8B0 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
}

.toggle-sidebar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(168, 230, 207, 0.4);
}

.toggle-sidebar svg {
  width: 20px;
  height: 20px;
}

.header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #5D5A6D;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>

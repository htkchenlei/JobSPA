<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="logo">
        <h1>
          <img src="/workspace.svg" alt="Logo" class="logo-icon">
          JobSPA
        </h1>
      </div>
      <nav class="menu">
        <router-link to="/dashboard" class="menu-item">
          <span class="menu-icon">📊</span>
          <span class="menu-text">仪表盘</span>
        </router-link>
        <router-link to="/project-management" class="menu-item">
          <span class="menu-icon">📄</span>
          <span class="menu-text">项目管理</span>
        </router-link>
        <router-link to="/advanced-search" class="menu-item">
          <span class="menu-icon">🔍</span>
          <span class="menu-text">高级查询</span>
        </router-link>
        <router-link to="/statistics" class="menu-item">
          <span class="menu-icon">📈</span>
          <span class="menu-text">统计分析</span>
        </router-link>
        <router-link to="/todos" class="menu-item">
          <span class="menu-icon">✅</span>
          <span class="menu-text">待办事项</span>
        </router-link>
        <router-link to="/file-management" class="menu-item">
          <span class="menu-icon">📁</span>
          <span class="menu-text">文件管理</span>
        </router-link>

        <router-link to="/work-log" class="menu-item">
          <span class="menu-icon">📅</span>
          <span class="menu-text">工作日志</span>
        </router-link>
        <router-link to="/bid-tool" class="menu-item">
          <span class="menu-icon">🎯</span>
          <span class="menu-text">投标工具</span>
        </router-link>
        <div class="menu-item user-profile" @click="changePassword">
          <span class="menu-icon">👤</span>
          <span class="menu-text">{{ userName }}</span>
        </div>
      </nav>
    </aside>
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <header class="header">
        <div class="header-left">
          <button class="toggle-sidebar" @click="toggleSidebar">
            ☰
          </button>
          <h2>{{ currentRouteName }}</h2>
        </div>
        <div class="header-right">
          <button class="btn btn-secondary" @click="logout">
            登出
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
import { ref, computed, onMounted } from 'vue'
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
  // 跳转到设置页面
  router.push('/settings')
}

// 登出
const logout = () => {
  // 清除sessionStorage中的token和用户信息
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  // 跳转到登录页面
  router.push('/login')
}


</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 250px;
  background-color: #2c3e50;
  color: white;
  transition: width 0.3s ease;
  overflow: hidden;
}

.sidebar.collapsed {
  width: 80px;
}

.logo {
  padding: 20px;
  border-bottom: 1px solid #34495e;
}

.logo h1 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.logo-icon {
  width: 16px;
  height: 16px;
  margin-right: 8px;
}

.menu {
  padding: 20px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.menu-item:hover {
  background-color: #34495e;
}

.menu-item.router-link-active {
  background-color: #3498db;
}

.menu-icon {
  font-size: 18px;
  margin-right: 12px;
  width: 20px;
  text-align: center;
}

.menu-text {
  font-size: 14px;
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  background-color: white;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-sidebar {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
}

.header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
}

/* 用户个人资料样式 */
.user-profile {
  cursor: pointer;
}

/* 按钮样式 */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-decoration: none;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}

.btn-primary:hover {
  background-color: #2980b9;
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.4);
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
  box-shadow: 0 2px 4px rgba(149, 165, 166, 0.3);
}

.btn-secondary:hover {
  background-color: #7f8c8d;
  box-shadow: 0 4px 8px rgba(149, 165, 166, 0.4);
}

.btn-success {
  background-color: #27ae60;
  color: white;
  box-shadow: 0 2px 4px rgba(39, 174, 96, 0.3);
}

.btn-success:hover {
  background-color: #229954;
  box-shadow: 0 4px 8px rgba(39, 174, 96, 0.4);
}

.btn-info {
  background-color: #1abc9c;
  color: white;
  box-shadow: 0 2px 4px rgba(26, 188, 156, 0.3);
}

.btn-info:hover {
  background-color: #16a085;
  box-shadow: 0 4px 8px rgba(26, 188, 156, 0.4);
}

/* 头部右侧样式 */
.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f5f5;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h4 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #e9ecef;
}
</style>
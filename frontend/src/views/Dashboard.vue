<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>仪表盘</h1>
      <p>欢迎回来！这里是您的工作概览</p>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <!-- 项目总数 -->
      <div class="stat-card project-card">
        <div class="stat-content">
          <p class="stat-label">项目总数</p>
          <h3 class="stat-value">{{ projectStats.total }}</h3>
          <p class="stat-detail">
            <span>{{ projectStats.inProgress }}</span> 个进行中
          </p>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
      </div>
      
      
      <!-- 今日活动 -->
      <div class="stat-card activity-card">
        <div class="stat-content">
          <p class="stat-label">今日活动</p>
          <h3 class="stat-value">{{ todayActivities.length }}</h3>
          <p class="stat-detail">
            <span>{{ workLogStats.weekly }}</span> 本周工作日志
          </p>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>
      
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-section">
      <!-- 项目进度图表 -->
      <div class="chart-container full-width">
        <div class="chart-header">
          <h3>项目进度</h3>
          <div class="chart-period">最近30天</div>
        </div>
        <div class="chart-content">
          <canvas ref="projectChart"></canvas>
        </div>
      </div>
    </div>
    
    <!-- 最近活动 -->
    <div class="recent-activities">
      <div class="activities-header">
        <h3>最近活动</h3>
        <button class="view-all-btn" @click="goToProjectManagement">查看全部</button>
      </div>
      <div class="activities-list">
        <div v-if="recentActivities.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>暂无最近活动</p>
        </div>
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="activity-content">
            <p class="activity-text">{{ activity.content }}</p>
            <p class="activity-time">{{ activity.time }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import router from '../router'

// 项目统计数据
const projectStats = ref({
  total: 0,
  inProgress: 0
})

// 工作日志统计数据
const workLogStats = ref({
  weekly: 0
})

// 今日活动
const todayActivities = ref<string[]>([])

// 最近活动
const recentActivities = ref<any[]>([])

// 图表引用
const projectChart = ref<HTMLCanvasElement | null>(null)
const projectChartInstance = ref<Chart | null>(null)

// 项目阶段映射
const STAGE_MAP = {
  '立项中': [1, 2],
  '已立项': [3, 4, 5],
  '招投标': [6, 7, 8],
  '已中标': [9, 10, 11],
  '已完成': [12, 13]
}

// 获取项目统计数据
const fetchProjectStats = async () => {
  try {
    const response = await fetch('/api/projects/')
    if (response.ok) {
      const projects = await response.json()
      projectStats.value.total = projects.length
      projectStats.value.inProgress = projects.filter((p: any) => p.stage < 12).length
      return projects
    }
    return []
  } catch (error) {
    console.error('获取项目统计数据失败:', error)
    return []
  }
}

// 获取认证头
const getAuthHeader = () => {
  const token = sessionStorage.getItem('token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

// 获取今日活动
const fetchTodayActivities = async () => {
  try {
    const response = await fetch('/api/work-log/today-activities', {
      headers: getAuthHeader()
    })
    if (response.ok) {
      const activities = await response.json()
      todayActivities.value = activities
    } else if (response.status === 401) {
      // 未授权访问，使用默认数据
      console.warn('获取今日活动失败: 未授权访问')
      todayActivities.value = []
    }
  } catch (error) {
    console.error('获取今日活动失败:', error)
    // 出错时使用默认数据
    todayActivities.value = []
  }
}

// 获取最近更新记录
const fetchRecentUpdates = async () => {
    try {
        const response = await fetch('/api/projects/latest-updates')
        if (response.ok) {
            const updates = await response.json()
            recentActivities.value = updates.map((update: any) => ({
                id: update.id,
                time: update.update_date && update.update_time ? `${update.update_date} ${update.update_time}` : '未知时间',
                content: `[${update.project_name}] ${update.update_content}`
            }))
        }
    } catch (error) {
        console.error('获取最近更新失败:', error)
        recentActivities.value = []
    }
}

// 跳转到项目管理页面
const goToProjectManagement = () => {
    router.push('/project-management')
}

// 初始化项目图表
const initProjectChart = (projects: any[]) => {
  if (!projectChart.value) return
  
  // 统计各阶段项目数量
  const stageCounts = {
    '立项中': 0,
    '已立项': 0,
    '招投标': 0,
    '已中标': 0,
    '已完成': 0
  }
  
  // 遍历项目，统计各阶段数量
  projects.forEach(project => {
    const stage = project.stage
    for (const [stageName, stageValues] of Object.entries(STAGE_MAP)) {
      if (stageValues.includes(stage)) {
        stageCounts[stageName as keyof typeof stageCounts]++
        break
      }
    }
  })
  
  // 准备图表数据
  const labels = Object.keys(stageCounts)
  const data = Object.values(stageCounts)
  
  projectChartInstance.value = new Chart(projectChart.value, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '项目数量',
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 206, 86, 0.7)',
            'rgba(75, 192, 192, 0.7)',
            'rgba(153, 102, 255, 0.7)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)'
          ],
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          ticks: {
            precision: 0
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  })
}

// 初始化数据
onMounted(async () => {
  const projects = await fetchProjectStats()
  await fetchTodayActivities()
  await fetchRecentUpdates()
  
  // 初始化图表
  setTimeout(() => {
    initProjectChart(projects)
  }, 100)
})
</script>

<style scoped>
/* 仪表盘容器 - 马卡龙风格 */
.dashboard {
  padding: 0;
  min-height: 100%;
}

/* 页面标题 */
.page-header {
  margin-bottom: 28px;
  animation: fadeIn 0.4s ease;
}

.page-header h1 {
  font-size: 26px;
  font-weight: 700;
  color: #5D5A6D;
  margin-bottom: 8px;
}

.page-header p {
  font-size: 15px;
  color: #8B8899;
  margin: 0;
}

/* 统计卡片 - 马卡龙撞色 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 28px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  animation: fadeIn 0.5s ease;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 20px 20px 0 0;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

/* 项目卡片 - 薄荷绿 */
.project-card::before {
  background: linear-gradient(90deg, #A8E6CF, #7DD3C0);
}

.project-card .stat-icon {
  background: linear-gradient(135deg, #A8E6CF, #7DD3C0);
  box-shadow: 0 4px 15px rgba(168, 230, 207, 0.4);
}

/* 活动卡片 - 天蓝 */
.activity-card::before {
  background: linear-gradient(90deg, #7EC8E3, #6BB8D3);
}

.activity-card .stat-icon {
  background: linear-gradient(135deg, #7EC8E3, #6BB8D3);
  box-shadow: 0 4px 15px rgba(126, 200, 227, 0.4);
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 13px;
  color: #8B8899;
  margin-bottom: 8px;
  font-weight: 500;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #5D5A6D;
  margin-bottom: 8px;
  line-height: 1;
}

.stat-detail {
  font-size: 13px;
  color: #8B8899;
  margin: 0;
}

.stat-detail span {
  font-weight: 600;
  color: #5D5A6D;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon svg {
  width: 26px;
  height: 26px;
}

/* 图表区域 */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 20px;
  margin-bottom: 28px;
}

.chart-container {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  animation: fadeIn 0.6s ease;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  margin: 0;
}

.chart-period {
  font-size: 12px;
  color: #8B8899;
  background: linear-gradient(135deg, #FFF5EE, #FFF9F5);
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 500;
}

.chart-container.full-width {
  grid-column: 1 / -1;
  max-width: 600px;
  margin: 0 auto;
}

.chart-content {
  height: 250px;
}

/* 最近活动 */
.recent-activities {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  animation: fadeIn 0.7s ease;
}

.activities-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activities-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  margin: 0;
}

.view-all-btn {
  font-size: 13px;
  color: #FF9A8B;
  background: linear-gradient(135deg, rgba(255, 154, 139, 0.1), rgba(255, 183, 178, 0.1));
  border: none;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.view-all-btn:hover {
  background: linear-gradient(135deg, rgba(255, 154, 139, 0.2), rgba(255, 183, 178, 0.2));
  transform: translateX(2px);
}

.activities-list {
  max-height: 320px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #F0E6E3;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.1), transparent);
  margin-left: -12px;
  margin-right: -12px;
  padding-left: 12px;
  padding-right: 12px;
  border-radius: 12px;
}

.activity-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.3), rgba(168, 230, 207, 0.1));
  color: #7DD3C0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 14px;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  color: #5D5A6D;
  margin-bottom: 4px;
  font-weight: 500;
}

.activity-time {
  font-size: 12px;
  color: #8B8899;
  margin: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #8B8899;
}

.empty-state svg {
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 14px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
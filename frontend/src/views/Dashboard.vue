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
      
      <!-- 待办事项 -->
      <div class="stat-card todo-card">
        <div class="stat-content">
          <p class="stat-label">待办事项</p>
          <h3 class="stat-value">{{ todoStats.pending }}</h3>
          <p class="stat-detail">
            <span>{{ Math.round((todoStats.completed / (todoStats.pending + todoStats.completed || 1)) * 100) }}%</span> 完成率
          </p>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
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
      
      <!-- 文件管理 -->
      <div class="stat-card file-card">
        <div class="stat-content">
          <p class="stat-label">文件管理</p>
          <h3 class="stat-value">{{ fileStats.total }}</h3>
          <p class="stat-detail">
            <span>{{ fileStats.folders }}</span> 个文件夹
          </p>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
          </svg>
        </div>
      </div>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-section">
      <!-- 项目进度图表 -->
      <div class="chart-container">
        <div class="chart-header">
          <h3>项目进度</h3>
          <div class="chart-period">最近30天</div>
        </div>
        <div class="chart-content">
          <canvas ref="projectChart"></canvas>
        </div>
      </div>
      
      <!-- 待办事项完成情况图表 -->
      <div class="chart-container">
        <div class="chart-header">
          <h3>待办事项完成情况</h3>
          <div class="chart-period">本月</div>
        </div>
        <div class="chart-content">
          <canvas ref="todoChart"></canvas>
        </div>
      </div>
    </div>
    
    <!-- 最近活动 -->
    <div class="recent-activities">
      <div class="activities-header">
        <h3>最近活动</h3>
        <button class="view-all-btn">查看全部</button>
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
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

// 项目统计数据
const projectStats = ref({
  total: 0,
  inProgress: 0
})

// 待办事项统计数据
const todoStats = ref({
  pending: 0,
  completed: 0
})

// 工作日志统计数据
const workLogStats = ref({
  weekly: 0
})

// 文件统计数据
const fileStats = ref({
  total: 0,
  folders: 0
})

// 今日活动
const todayActivities = ref<string[]>([])

// 最近活动
const recentActivities = ref([
  { id: 1, time: '2026-02-16 14:30', content: '更新了项目进度' },
  { id: 2, time: '2026-02-16 13:15', content: '添加了新的待办事项' },
  { id: 3, time: '2026-02-16 11:00', content: '生成了今日工作日志' },
  { id: 4, time: '2026-02-16 10:00', content: '上传了新文件' }
])

// 图表引用
const projectChart = ref<HTMLCanvasElement | null>(null)
const todoChart = ref<HTMLCanvasElement | null>(null)
const projectChartInstance = ref<Chart | null>(null)
const todoChartInstance = ref<Chart | null>(null)

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
  const token = localStorage.getItem('token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

// 获取待办事项统计数据
const fetchTodoStats = async () => {
  try {
    const response = await fetch('/api/todos/', {
      headers: getAuthHeader()
    })
    if (response.ok) {
      const todos = await response.json()
      todoStats.value.pending = todos.filter((t: any) => !t.is_finished).length
      todoStats.value.completed = todos.filter((t: any) => t.is_finished).length
    } else if (response.status === 401) {
      // 未授权访问，使用默认数据
      console.warn('获取待办事项统计数据失败: 未授权访问')
      todoStats.value.pending = 0
      todoStats.value.completed = 0
    }
  } catch (error) {
    console.error('获取待办事项统计数据失败:', error)
    // 出错时使用默认数据
    todoStats.value.pending = 0
    todoStats.value.completed = 0
  }
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

// 获取文件统计数据
const fetchFileStats = async () => {
  try {
    const response = await fetch('/api/files/', {
      headers: getAuthHeader()
    })
    if (response.ok) {
      const fileSystem = await response.json()
      // 简单统计文件和文件夹数量
      let totalFiles = 0
      let totalFolders = 0
      
      const countFiles = (node: any) => {
        if (node.type === 'folder') {
          totalFolders++
          if (node.children) {
            node.children.forEach((child: any) => countFiles(child))
          }
        } else {
          totalFiles++
        }
      }
      
      countFiles(fileSystem)
      fileStats.value.total = totalFiles
      fileStats.value.folders = totalFolders
    } else if (response.status === 401) {
      // 未授权访问，使用默认数据
      console.warn('获取文件统计数据失败: 未授权访问')
      fileStats.value.total = 0
      fileStats.value.folders = 0
    }
  } catch (error) {
    console.error('获取文件统计数据失败:', error)
    // 出错时使用默认数据
    fileStats.value.total = 0
    fileStats.value.folders = 0
  }
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

// 初始化待办事项图表
const initTodoChart = () => {
  if (!todoChart.value) return
  
  todoChartInstance.value = new Chart(todoChart.value, {
    type: 'doughnut',
    data: {
      labels: ['已完成', '待完成'],
      datasets: [
        {
          data: [todoStats.value.completed, todoStats.value.pending],
          backgroundColor: ['#10b981', '#f59e0b'],
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      },
      cutout: '70%'
    }
  })
}

// 更新待办事项图表
const updateTodoChart = () => {
  if (!todoChartInstance.value) return
  
  todoChartInstance.value.data.datasets[0].data = [todoStats.value.completed, todoStats.value.pending]
  todoChartInstance.value.update()
}

// 监听待办事项数据变化，更新图表
watch(
  () => [todoStats.value.pending, todoStats.value.completed],
  () => {
    updateTodoChart()
  }
)

// 初始化数据
onMounted(async () => {
  const projects = await fetchProjectStats()
  await fetchTodoStats()
  await fetchTodayActivities()
  await fetchFileStats()
  
  // 初始化图表
  setTimeout(() => {
    initProjectChart(projects)
    initTodoChart()
  }, 100)
})
</script>

<style scoped>
/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* 仪表盘容器 */
.dashboard {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 页面标题 */
.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 16px;
  color: #666;
  margin: 0;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.project-card {
  border-left: 4px solid #3b82f6;
}

.todo-card {
  border-left: 4px solid #8b5cf6;
}

.activity-card {
  border-left: 4px solid #10b981;
}

.file-card {
  border-left: 4px solid #f59e0b;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.stat-detail {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.stat-detail span {
  font-weight: bold;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.project-card .stat-icon {
  background-color: #3b82f6;
}

.todo-card .stat-icon {
  background-color: #8b5cf6;
}

.activity-card .stat-icon {
  background-color: #10b981;
}

.file-card .stat-icon {
  background-color: #f59e0b;
}

/* 图表区域 */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.chart-period {
  font-size: 12px;
  color: #666;
}

.chart-content {
  height: 250px;
}

/* 最近活动 */
.recent-activities {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activities-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activities-header h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.view-all-btn {
  font-size: 12px;
  color: #3b82f6;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.view-all-btn:hover {
  text-decoration: underline;
}

.activities-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ebf5ff;
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
  font-weight: 500;
}

.activity-time {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #666;
}

.empty-state svg {
  margin-bottom: 15px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .chart-content {
    height: 200px;
  }
}
</style>
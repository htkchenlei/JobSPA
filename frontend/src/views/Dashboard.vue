<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>仪表盘</h1>
      <p>欢迎回来！这里是您的工作概览</p>
    </div>

    <!-- 统计卡片 - 4列 -->
    <div class="stats-cards">
      <div class="stat-card card-mint" @click="goToProjectList()">
        <div class="stat-content">
          <p class="stat-label">项目总数</p>
          <h3 class="stat-value">{{ projectStats.total }}</h3>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
      </div>

      <div class="stat-card card-sky" @click="goToProjectList()">
        <div class="stat-content">
          <p class="stat-label">进行中</p>
          <h3 class="stat-value">{{ projectStats.inProgress }}</h3>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
      </div>

      <div class="stat-card card-coral" @click="goToProjectList('completed')">
        <div class="stat-content">
          <p class="stat-label">已完成</p>
          <h3 class="stat-value">{{ projectStats.completed }}</h3>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>

      <div class="stat-card card-lavender" @click="goToWorkLog">
        <div class="stat-content">
          <p class="stat-label">本月日志</p>
          <h3 class="stat-value">{{ workLogStats.monthly }}</h3>
        </div>
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 主内容区 - 左右分栏 -->
    <div class="main-content">
      <!-- 左侧：项目阶段分布 -->
      <div class="content-card chart-card">
        <div class="card-header">
          <h3>项目阶段分布</h3>
          <div class="card-badge">{{ projectStats.total }} 个项目</div>
        </div>
        <div class="chart-wrapper">
          <canvas ref="projectChart"></canvas>
        </div>
      </div>

      <!-- 右侧：最近更新 -->
      <div class="content-card updates-card">
        <div class="card-header">
          <h3>最近更新</h3>
          <button class="view-all-btn" @click="goToProjectManagement">查看全部</button>
        </div>
        <div class="updates-list">
          <div v-if="recentActivities.length === 0" class="empty-state">
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>暂无最近更新</p>
          </div>
          <div v-for="activity in recentActivities.slice(0, 8)" :key="activity.id" class="update-item">
            <div class="update-dot"></div>
            <div class="update-content">
              <p class="update-text">{{ activity.content }}</p>
              <p class="update-time">{{ activity.time }}</p>
            </div>
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

const projectStats = ref({ total: 0, inProgress: 0, completed: 0 })
const workLogStats = ref({ monthly: 0 })
const recentActivities = ref<any[]>([])

const projectChart = ref<HTMLCanvasElement | null>(null)
const projectChartInstance = ref<Chart | null>(null)

const STAGE_MAP = {
  '立项中': [1, 2],
  '已立项': [3, 4, 5],
  '招投标': [6, 7, 8],
  '已中标': [9, 10, 11],
  '已完成': [12, 13]
}

const getAuthHeader = () => {
  const token = sessionStorage.getItem('token')
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}

const fetchProjectStats = async () => {
  try {
    const response = await fetch('/api/projects/')
    if (response.ok) {
      const projects = await response.json()
      projectStats.value.total = projects.length
      projectStats.value.inProgress = projects.filter((p: any) => p.stage < 12).length
      projectStats.value.completed = projects.filter((p: any) => p.stage >= 12).length
      return projects
    }
    return []
  } catch (error) {
    console.error('获取项目数据失败:', error)
    return []
  }
}

const fetchWorkLogStats = async () => {
  // “本月日志”统计的是本月手动录入的项目进展（project_progress）条数，
  // 而不是 AI 生成的 work_log 记录
  try {
    const response = await fetch('/api/projects/monthly-progress-count', { headers: getAuthHeader() })
    if (response.ok) {
      const data = await response.json()
      if (data && typeof data.count === 'number') {
        workLogStats.value.monthly = data.count
        return
      }
    }
    // 后端未同步新接口时退回旧的 AI 日志月度统计，避免接口缺失导致报错
    const fallback = await fetch('/api/work-log/monthly-count', { headers: getAuthHeader() })
    if (fallback.ok) {
      const data = await fallback.json()
      if (data && typeof data.count === 'number') {
        workLogStats.value.monthly = data.count
      }
    }
  } catch (error) {
    console.error('获取本月日志统计失败:', error)
  }
}

const fetchRecentUpdates = async () => {
  try {
    const response = await fetch('/api/projects/latest-updates')
    if (response.ok) {
      const updates = await response.json()
      recentActivities.value = updates.map((u: any) => ({
        id: u.id,
        time: u.update_date && u.update_time ? `${u.update_date} ${u.update_time}` : '',
        content: `[${u.project_name}] ${u.update_content}`
      }))
    }
  } catch (error) {
    console.error('获取最近更新失败:', error)
    recentActivities.value = []
  }
}

const goToProjectManagement = () => {
  router.push('/project-management')
}

// 跳转到项目管理页；view = 'completed' 时直接展示已完成项目
const goToProjectList = (view?: string) => {
  if (view === 'completed') {
    router.push({ path: '/project-management', query: { view: 'completed' } })
  } else {
    router.push('/project-management')
  }
}

// 跳转到工作日志页
const goToWorkLog = () => {
  router.push('/work-log')
}

const initProjectChart = (projects: any[]) => {
  if (!projectChart.value) return

  const stageCounts: Record<string, number> = {
    '立项中': 0, '已立项': 0, '招投标': 0, '已中标': 0, '已完成': 0
  }

  projects.forEach((project) => {
    for (const [stageName, stageValues] of Object.entries(STAGE_MAP)) {
      if (stageValues.includes(project.stage)) {
        stageCounts[stageName]++
        break
      }
    }
  })

  const labels = Object.keys(stageCounts)
  const data = Object.values(stageCounts)

  projectChartInstance.value = new Chart(projectChart.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: '项目数量',
        data,
        backgroundColor: [
          'rgba(255, 107, 107, 0.7)',
          'rgba(78, 163, 224, 0.7)',
          'rgba(255, 179, 71, 0.7)',
          'rgba(79, 195, 163, 0.7)',
          'rgba(162, 129, 255, 0.7)',
        ],
        borderColor: [
          'rgba(255, 107, 107, 1)',
          'rgba(78, 163, 224, 1)',
          'rgba(255, 179, 71, 1)',
          'rgba(79, 195, 163, 1)',
          'rgba(162, 129, 255, 1)',
        ],
        borderWidth: 1,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0, 0, 0, 0.04)' },
          ticks: { precision: 0 }
        },
        x: {
          grid: { display: false },
          ticks: { font: { size: 12 } }
        }
      }
    }
  })
}

onMounted(async () => {
  const projects = await fetchProjectStats()
  await fetchWorkLogStats()
  await fetchRecentUpdates()
  setTimeout(() => initProjectChart(projects), 100)
})
</script>

<style scoped>
.dashboard {
  padding: 0;
  min-height: 100%;
  animation: fadeIn 0.4s ease;
}

/* ---- 页面标题 ---- */
.page-header {
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: #3D3A4B;
  margin-bottom: 4px;
}
.page-header p {
  font-size: 14px;
  color: #9693A6;
  margin: 0;
}

/* ---- 统计卡片 ---- */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

@media (max-width: 900px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 20px 22px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0EBF5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
}
.stat-label {
  font-size: 12px;
  color: #9693A6;
  margin-bottom: 6px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.stat-value {
  font-size: 30px;
  font-weight: 700;
  color: #3D3A4B;
  margin: 0;
  line-height: 1;
}
.stat-icon {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}
.stat-icon svg {
  width: 22px;
  height: 22px;
}

/* 卡片配色 */
.card-mint .stat-icon  { background: linear-gradient(135deg, #80D6B8, #5EC2A0); box-shadow: 0 4px 12px rgba(128, 214, 184, 0.35); }
.card-sky .stat-icon   { background: linear-gradient(135deg, #6CB4EE, #4D9FDE); box-shadow: 0 4px 12px rgba(108, 180, 238, 0.35); }
.card-coral .stat-icon { background: linear-gradient(135deg, #FF8A80, #F76D6D); box-shadow: 0 4px 12px rgba(255, 138, 128, 0.35); }
.card-lavender .stat-icon { background: linear-gradient(135deg, #B39DDB, #9575CD); box-shadow: 0 4px 12px rgba(179, 157, 219, 0.35); }

/* ---- 主内容区 ---- */
.main-content {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 16px;
}

@media (max-width: 1000px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

.content-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0EBF5;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 22px;
  border-bottom: 1px solid #F5F1F9;
}
.card-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #3D3A4B;
  margin: 0;
}
.card-badge {
  font-size: 11px;
  color: #7C64CC;
  background: linear-gradient(135deg, #F0EBFF, #F8F5FF);
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
}
.view-all-btn {
  font-size: 12px;
  color: #7C64CC;
  background: none;
  border: 1px solid #E0D8F5;
  cursor: pointer;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: 600;
  transition: all 0.2s ease;
}
.view-all-btn:hover {
  background: #7C64CC;
  color: white;
  border-color: #7C64CC;
}

/* ---- 图表 ---- */
.chart-card {
  min-height: 360px;
}
.chart-wrapper {
  padding: 16px 22px 8px;
  height: 310px;
}

/* ---- 更新列表 ---- */
.updates-card {
  min-height: 360px;
}
.updates-list {
  padding: 8px 16px;
  max-height: 330px;
  overflow-y: auto;
}

.update-item {
  display: flex;
  align-items: flex-start;
  padding: 10px 8px;
  border-radius: 10px;
  transition: background 0.15s ease;
}
.update-item:hover {
  background: #F9F7FC;
}

.update-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #B39DDB, #9575CD);
  margin-top: 5px;
  margin-right: 10px;
  flex-shrink: 0;
}
.update-content {
  flex: 1;
  min-width: 0;
}
.update-text {
  font-size: 13px;
  color: #3D3A4B;
  margin-bottom: 3px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.update-time {
  font-size: 11px;
  color: #B0ACC1;
  margin: 0;
}

/* ---- 空状态 ---- */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #C0BFCB;
}
.empty-state svg {
  margin-bottom: 12px;
  opacity: 0.4;
}
.empty-state p {
  font-size: 13px;
}

/* ---- 动画 ---- */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ==================== 移动端适配 ==================== */
@media (max-width: 600px) {
  .page-header {
    margin-bottom: 14px;
  }

  .page-header h1 {
    font-size: 20px;
  }

  .page-header p {
    font-size: 13px;
  }

  .stats-cards {
    gap: 10px;
    margin-bottom: 14px;
  }

  .stat-card {
    padding: 14px 12px;
    border-radius: 12px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
  }

  .stat-icon svg {
    width: 18px;
    height: 18px;
  }

  .stat-label {
    font-size: 11px;
  }

  .main-content {
    gap: 12px;
  }

  .content-card {
    border-radius: 12px;
  }

  .card-header {
    padding: 14px 16px;
  }

  .chart-wrapper {
    padding: 10px 12px 6px;
    height: 230px;
  }

  .chart-card,
  .updates-card {
    min-height: 280px;
  }

  .updates-list {
    padding: 4px 10px;
  }
}
</style>

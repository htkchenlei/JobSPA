<template>
  <div class="dashboard">
    <h3>仪表盘</h3>
    <div class="dashboard-cards">
      <!-- 项目相关卡片 -->
      <div class="card">
        <div class="card-title">项目总数</div>
        <div class="card-value">{{ projectStats.total }}</div>
      </div>
      <div class="card">
        <div class="card-title">进行中项目</div>
        <div class="card-value">{{ projectStats.inProgress }}</div>
      </div>
      
      <!-- 待办事项相关卡片 -->
      <div class="card">
        <div class="card-title">待办事项</div>
        <div class="card-value">{{ todoStats.pending }}</div>
      </div>
      <div class="card">
        <div class="card-title">已完成任务</div>
        <div class="card-value">{{ todoStats.completed }}</div>
      </div>
      
      <!-- 工作日志相关卡片 -->
      <div class="card">
        <div class="card-title">今日活动</div>
        <div class="card-value">{{ todayActivities.length }}</div>
      </div>
      <div class="card">
        <div class="card-title">本周工作日志</div>
        <div class="card-value">{{ workLogStats.weekly }}</div>
      </div>
      
      <!-- 文件管理相关卡片 -->
      <div class="card">
        <div class="card-title">文件总数</div>
        <div class="card-value">{{ fileStats.total }}</div>
      </div>
      <div class="card">
        <div class="card-title">文件夹数量</div>
        <div class="card-value">{{ fileStats.folders }}</div>
      </div>
    </div>
    
    <!-- 最近活动 -->
    <div class="recent-activities">
      <h4>最近活动</h4>
      <div class="activity-list">
        <div v-if="recentActivities.length === 0" class="empty-state">
          暂无最近活动
        </div>
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-time">{{ activity.time }}</div>
          <div class="activity-content">{{ activity.content }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

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
  { id: 1, time: '2026-02-15 14:30', content: '更新了项目进度' },
  { id: 2, time: '2026-02-15 13:15', content: '添加了新的待办事项' },
  { id: 3, time: '2026-02-15 11:00', content: '生成了今日工作日志' },
  { id: 4, time: '2026-02-15 10:00', content: '上传了新文件' }
])

// 获取项目统计数据
const fetchProjectStats = async () => {
  try {
    const response = await fetch('/api/projects/')
    if (response.ok) {
      const projects = await response.json()
      projectStats.value.total = projects.length
      projectStats.value.inProgress = projects.filter((p: any) => p.stage < 12).length
    }
  } catch (error) {
    console.error('获取项目统计数据失败:', error)
  }
}

// 获取待办事项统计数据
const fetchTodoStats = async () => {
  try {
    const response = await fetch('/api/todos/')
    if (response.ok) {
      const todos = await response.json()
      todoStats.value.pending = todos.filter((t: any) => !t.is_finished).length
      todoStats.value.completed = todos.filter((t: any) => t.is_finished).length
    }
  } catch (error) {
    console.error('获取待办事项统计数据失败:', error)
  }
}

// 获取今日活动
const fetchTodayActivities = async () => {
  try {
    const response = await fetch('/api/work-log/today-activities')
    if (response.ok) {
      const activities = await response.json()
      todayActivities.value = activities
    }
  } catch (error) {
    console.error('获取今日活动失败:', error)
  }
}

// 获取文件统计数据
const fetchFileStats = async () => {
  try {
    const response = await fetch('/api/files/')
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
    }
  } catch (error) {
    console.error('获取文件统计数据失败:', error)
  }
}

// 初始化数据
onMounted(async () => {
  await fetchProjectStats()
  await fetchTodoStats()
  await fetchTodayActivities()
  await fetchFileStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 500;
}

h4 {
  margin-top: 30px;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 500;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.card {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 14px;
  color: #6c757d;
  margin-bottom: 10px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #343a40;
}

.recent-activities {
  margin-top: 30px;
}

.activity-list {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  font-size: 12px;
  color: #6c757d;
  min-width: 120px;
}

.activity-content {
  flex: 1;
  font-size: 14px;
  color: #343a40;
  margin-left: 15px;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #6c757d;
  font-style: italic;
}
</style>
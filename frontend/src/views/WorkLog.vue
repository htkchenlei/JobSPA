<template>
  <div class="work-log">
    <h1>工作日志</h1>
    
    <div class="work-log-content">
      <!-- 左侧日历 -->
      <div class="left-section">
        <div class="calendar-container">
          <div class="calendar-header">
            <button class="btn btn-secondary" @click="prevMonth">&lt; 上个月</button>
            <h2>{{ currentYear }}年{{ currentMonth + 1 }}月</h2>
            <button class="btn btn-secondary" @click="nextMonth">下个月 &gt;</button>
          </div>
          
          <div class="calendar-weekdays">
            <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
          </div>
          
          <div class="calendar-days">
            <!-- 上个月的日期 -->
            <div v-for="day in prevMonthDays" :key="`prev-${day}`" class="calendar-day other-month">{{ day }}</div>
            
            <!-- 当月的日期 -->
        <div 
          v-for="day in currentMonthDays" 
          :key="`current-${day}`" 
          class="calendar-day"
          :class="{
            'today': isToday(day), 
            'has-log': hasLog(day),
            'future-day': isFutureDay(day),
            'selected': day === selectedDate
          }"
          @click="!isFutureDay(day) && selectDate(day)"
        >
          {{ day }}
          <div v-if="isToday(day)" class="today-indicator"></div>
        </div>
            
            <!-- 下个月的日期 -->
            <div v-for="day in nextMonthDays" :key="`next-${day}`" class="calendar-day other-month">{{ day }}</div>
          </div>
        </div>
        
        <!-- 生成日志按钮 -->
        <div v-if="selectedDate && isToday(selectedDate)" class="generate-log-container">
          <button class="btn btn-primary" @click="generateLog" :disabled="isGenerating">
            {{ isGenerating ? '生成中...' : (selectedLog ? '重新生成今日日志' : '生成今日日志') }}
          </button>
        </div>
      </div>
      
      <!-- 右侧内容 -->
      <div class="right-section">
        <!-- 活动记录 -->
        <div v-if="currentActivities.length > 0" class="prompt-content">
          <h3>今日活动记录</h3>
          <div class="prompt-section">
            <ul class="activities-list">
              <li v-for="(activity, index) in currentActivities" :key="index">{{ activity }}</li>
            </ul>
          </div>
        </div>
        
        <!-- 已选择的日志 -->
        <div v-if="selectedLog" class="log-content">
          <h3>{{ selectedLog.date }} 工作日志</h3>
          <div class="log-text">{{ selectedLog.content }}</div>
        </div>
        
        <!-- 生成的日志 -->
        <div v-if="generatedLog" class="log-content">
          <h3>{{ new Date().toISOString().split('T')[0] }} 工作日志</h3>
          <div class="log-text">{{ generatedLog }}</div>
          <div class="log-actions">
            <button class="btn btn-primary" @click="saveLog">保存日志</button>
          </div>
        </div>
        
        <!-- 未选择日期时的提示 -->
        <div v-else-if="!selectedDate && currentActivities.length === 0" class="empty-state">
          <p>请选择一个日期查看或生成工作日志</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

// 日历相关
const currentDate = ref(new Date())
const selectedDate = ref<number | null>(null)
const selectedLog = ref<any>(null)
const generatedLog = ref<string | null>(null)
const isGenerating = ref(false)
const currentPrompt = ref('')
const currentActivities = ref<string[]>([])



// 工作日志数据
const workLogs = ref<any[]>([])

// 计算属性
const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth())
const weekdays = ['日', '一', '二', '三', '四', '五', '六']

// 获取当月第一天
const firstDayOfMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value, 1)
})

// 获取当月最后一天
const lastDayOfMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0)
})

// 获取当月第一天是星期几
const startDay = computed(() => {
  return firstDayOfMonth.value.getDay()
})

// 获取当月的天数
const daysInMonth = computed(() => {
  return lastDayOfMonth.value.getDate()
})

// 上个月的日期
const prevMonthDays = computed(() => {
  const days = []
  const prevMonthLastDay = new Date(currentYear.value, currentMonth.value, 0).getDate()
  for (let i = startDay.value - 1; i >= 0; i--) {
    days.push(prevMonthLastDay - i)
  }
  return days
})

// 当月的日期
const currentMonthDays = computed(() => {
  const days = []
  for (let i = 1; i <= daysInMonth.value; i++) {
    days.push(i)
  }
  return days
})

// 下个月的日期
const nextMonthDays = computed(() => {
  const days = []
  const totalDays = prevMonthDays.value.length + currentMonthDays.value.length
  const remainingDays = 42 - totalDays // 6x7日历
  for (let i = 1; i <= remainingDays; i++) {
    days.push(i)
  }
  return days
})

// 方法
const prevMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

const isToday = (day: number) => {
  const today = new Date()
  return today.getFullYear() === currentYear.value && 
         today.getMonth() === currentMonth.value && 
         today.getDate() === day
}

const isFutureDay = (day: number) => {
  const selectedDateObj = new Date(currentYear.value, currentMonth.value, day)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return selectedDateObj > today
}

const hasLog = (day: number) => {
  const dateStr = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  return workLogs.value.some(log => log.date === dateStr)
}

const selectDate = async (day: number) => {
  // 检查是否是今天或以前的日期
  const selectedDateObj = new Date(currentYear.value, currentMonth.value, day)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  if (selectedDateObj > today) {
    return // 今天以后的日期不可选择
  }
  
  selectedDate.value = day
  const dateStr = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  selectedLog.value = workLogs.value.find(log => log.date === dateStr) || null
  generatedLog.value = null
  
  // 检查是否是今天
  const isTodaySelected = isToday(day)
  if (isTodaySelected) {
    // 如果选择的是今天，自动获取并显示今天的活动记录
    const activities = await getTodayActivities()
    currentActivities.value = activities
    
    // 构建提示词但不显示，只在生成日志时使用
    if (activities.length > 0) {
      currentPrompt.value = `假设你是一位售前工程师，为了向公司展示项目进度和工作进度，请根据以下今天的活动记录，生成一份工作日志，字数不少于40字：\n${activities.join('\n')}`
    }
  } else {
    // 不是今天，清空提示词和活动
    currentPrompt.value = ''
    currentActivities.value = []
  }
}

// 获取今天的活动
const getTodayActivities = async () => {
  try {
    // 调用后端API获取今天的项目更新信息
    const response = await fetch('/api/work-log/today-activities')
    const activities = await response.json()
    
    return activities
  } catch (error) {
    console.error('获取活动失败:', error)
    return []
  }
}

// 调用大模型API生成日志
const generateLog = async () => {
  isGenerating.value = true
  try {
    // 获取当前登录用户ID
    let currentUserId = 1 // 默认值
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        currentUserId = user.id || 1
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
    
    // 检查是否有活动记录
    if (currentActivities.value.length === 0) {
      // 生成活动记录
      const generateResponse = await fetch('/api/work-log/generate-activities', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: currentUserId })
      })
      
      if (generateResponse.ok) {
        const generateData = await generateResponse.json()
        currentActivities.value = generateData.activities
        
        // 构建提示词
        if (currentActivities.value.length > 0) {
          currentPrompt.value = `假设你是一位售前工程师，为了向公司展示项目进度和工作进度，请根据以下今天的活动记录，生成一份工作日志，字数不少于40字：\n${currentActivities.value.join('\n')}`
        } else {
          console.log('今天没有活动记录')
          return
        }
      } else {
        console.error('生成活动记录失败:', await generateResponse.text())
        return
      }
    }
    
    // 从localStorage获取AI设置
    const aiSettingsStr = localStorage.getItem('aiSettings')
    let model = 'deepseek' // 默认模型
    let apiKey = ''
    if (aiSettingsStr) {
      const aiSettings = JSON.parse(aiSettingsStr)
      model = aiSettings.defaultModel || 'deepseek'
      apiKey = aiSettings.apiKeys?.[model] || ''
    }
    
    // 调用大模型API
    const response = await fetch('/api/ai/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: model,
        prompt: currentPrompt.value,
        max_tokens: 500,
        api_key: apiKey
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      generatedLog.value = data.content
      // 清除selectedLog，这样按钮会显示"生成今日日志"
      selectedLog.value = null
    } else {
      console.error('生成日志失败:', await response.text())
    }
  } catch (error) {
    console.error('生成日志失败:', error)
  } finally {
    isGenerating.value = false
  }
}

// 保存日志
const saveLog = async () => {
  if (!generatedLog.value) return
  
  try {
    // 获取当前登录用户ID
    let currentUserId = 1 // 默认值
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        currentUserId = user.id || 1
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
    
    // 保存日志到数据库
    const saveResponse = await fetch('/api/work-log/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: currentUserId,
        work_log_by_ai: generatedLog.value,
        today_activities: currentActivities.value.join('\n')
      })
    })
    
    if (saveResponse.ok) {
      console.log('日志保存成功')
      
      // 更新本地状态
      const today = new Date().toISOString().split('T')[0]
      const newLog = {
        date: today,
        content: generatedLog.value
      }
      
      // 检查是否已存在今天的日志
      const existingLogIndex = workLogs.value.findIndex(log => log.date === today)
      if (existingLogIndex > -1) {
        workLogs.value[existingLogIndex] = newLog
      } else {
        workLogs.value.push(newLog)
      }
      selectedLog.value = newLog
      generatedLog.value = null
    } else {
      console.error('保存日志失败:', await saveResponse.text())
    }
  } catch (error) {
    console.error('保存日志时发生错误:', error)
  }
}

// 初始化
onMounted(async () => {
  // 设置今天为选中日期
  const today = new Date()
  selectedDate.value = today.getDate()
  
  try {
    // 获取当前登录用户ID
    let currentUserId = 1 // 默认值
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        currentUserId = user.id || 1
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
    
    // 自动获取今天的活动记录
    const activities = await getTodayActivities()
    currentActivities.value = activities
    
    // 构建提示词但不显示，只在生成日志时使用
    if (activities.length > 0) {
      currentPrompt.value = `假设你是一位售前工程师，为了向公司展示项目进度和工作进度，请根据以下今天的活动记录，生成一份工作日志，字数不少于40字：\n${activities.join('\n')}`
    }
    
    // 加载今天的工作日志
    const todayStr = today.toISOString().split('T')[0]
    const logResponse = await fetch(`/api/work-log/date/${todayStr}`)
    
    if (logResponse.ok) {
      const logData = await logResponse.json()
      if (logData.work_log_by_ai) {
        selectedLog.value = {
          date: todayStr,
          content: logData.work_log_by_ai
        }
      }
    }
    
    // 加载所有工作日志
    const logsResponse = await fetch(`/api/work-log/user/${currentUserId}`)
    if (logsResponse.ok) {
      const logsData = await logsResponse.json()
      workLogs.value = logsData.map((log: any) => ({
        date: log.log_date,
        content: log.work_log_by_ai
      }))
    }
  } catch (error) {
    console.error('初始化工作日志失败:', error)
  }
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理工作
})
</script>

<style scoped>
.work-log {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 40px;
}

/* 主内容布局 */
.work-log-content {
  display: flex;
  gap: 20px;
}

/* 左侧部分 */
.left-section {
  flex: 0 0 350px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 右侧部分 */
.right-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 日历样式 */
.calendar-container {
  background-color: white;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.calendar-header h2 {
  margin: 0;
  color: #333;
  font-size: 14px;
}

.calendar-header .btn {
  padding: 4px 8px;
  font-size: 12px;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
  margin-bottom: 3px;
}

.weekday {
  text-align: center;
  font-weight: bold;
  color: #555;
  padding: 3px;
  font-size: 10px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  font-size: 12px;
  min-height: 30px;
  max-height: 40px;
}

.calendar-day:hover {
  background-color: #f0f0f0;
}

.calendar-day.other-month {
  color: #ccc;
}

.calendar-day.future-day {
  color: #ccc;
  cursor: not-allowed;
}

.calendar-day.future-day:hover {
  background-color: transparent;
}

.calendar-day.today {
  background-color: #3498db;
  color: white;
  font-weight: bold;
}

.calendar-day.selected {
  background-color: #9b59b6;
  color: white;
  font-weight: bold;
}

.calendar-day.has-log {
  background-color: #27ae60;
  color: white;
}

.today-indicator {
  position: absolute;
  bottom: 4px;
  width: 6px;
  height: 6px;
  background-color: #ff6b6b;
  border-radius: 50%;
}

/* 生成日志按钮 */
.generate-log-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

/* 日志内容 */
.log-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* AI内容区域 */
.ai-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 提示词内容 */
.prompt-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 空状态 */
.empty-state {
  background-color: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #666;
}

.log-content h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 15px;
}

.log-text {
  line-height: 1.6;
  color: #555;
  white-space: pre-wrap;
}

.log-actions {
  margin-top: 20px;
  text-align: right;
}

/* 模型选择 */
.model-selector {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.model-selector h3 {
  color: #333;
  margin-top: 0;
  margin-bottom: 15px;
}

.model-options {
  display: flex;
  gap: 20px;
}

.model-option {
  display: flex;
  align-items: center;
  gap: 5px;
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

.btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
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
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.prompt-section {
  margin-bottom: 20px;
}

.prompt-section h4 {
  margin: 0 0 10px 0;
  color: #555;
}

.activities-list {
  list-style-type: disc;
  padding-left: 20px;
  margin: 0;
}

.activities-list li {
  margin-bottom: 8px;
  color: #666;
  line-height: 1.4;
}

.prompt-text {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #3498db;
  font-family: monospace;
  white-space: pre-wrap;
  line-height: 1.4;
  color: #333;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #e9ecef;
}
</style>
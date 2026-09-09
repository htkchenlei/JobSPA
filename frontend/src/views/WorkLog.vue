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
            'has-activities': hasActivities(day),
            'future-day': isFutureDay(day),
            'selected': day === selectedDate
          }"
          :title="getDayTooltip(day)"
          @click="!isFutureDay(day) && selectDate(day)"
        >
          {{ day }}
          <div v-if="isToday(day)" class="today-indicator"></div>
          <div v-if="hasLog(day)" class="log-indicator"></div>
        </div>
            
            <!-- 下个月的日期 -->
            <div v-for="day in nextMonthDays" :key="`next-${day}`" class="calendar-day other-month">{{ day }}</div>
          </div>

          <!-- 日历图例 -->
          <div class="calendar-legend">
            <span class="legend-item legend-today">今天</span>
            <span class="legend-item legend-log">已生成 AI 日志</span>
            <span class="legend-item legend-activities">仅有项目进展</span>
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
          <h3>{{ selectedDate ? (isToday(selectedDate) ? '今日活动记录' : `${currentYear}年${currentMonth + 1}月${selectedDate}日活动记录`) : '活动记录' }}</h3>
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
import { useRoute } from 'vue-router'

const route = useRoute()

// 日历相关
const currentDate = ref(new Date())
const selectedDate = ref<number | null>(null)
const selectedLog = ref<any>(null)
const generatedLog = ref<string | null>(null)
const isGenerating = ref(false)
const currentPrompt = ref('')
const currentActivities = ref<string[]>([])

// 存储每天的活动记录，格式：{ '2026-03-20': ['活动1', '活动2'] }
const dailyActivities = ref<Record<string, string[]>>({})

// 缓存“每月有项目进展的日期”，来自后端缓存接口，避免逐日查询数据库
const progressDaysByMonth = ref<Record<string, { day: number; count: number }[]>>({})

// 生成 YYYY-MM 月份键
const getMonthKey = (year: number, month: number) =>
  `${year}-${String(month + 1).padStart(2, '0')}`

// 获取某天在当月是否有项目进展（读缓存）
const getDayProgress = (day: number) => {
  const key = getMonthKey(currentYear.value, currentMonth.value)
  const days = progressDaysByMonth.value[key] || []
  return days.find(d => d.day === day) || null
}



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
const prevMonth = async () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
  await loadProgressDaysOfMonth()
}

const nextMonth = async () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
  await loadProgressDaysOfMonth()
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

// 检查某一天是否有项目进展（读月份缓存，不再逐日查库）
const hasActivities = (day: number) => {
  return !!getDayProgress(day)
}

// 单元格 hover 提示，明确区分 AI 日志与项目进展
const getDayTooltip = (day: number) => {
  const dateStr = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  const log = workLogs.value.find((l: any) => l.date === dateStr)
  const meta = getDayProgress(day)
  const hasAiLog = !!(log && log.content)
  if (hasAiLog) {
    const isAutoFilled = typeof log.content === 'string' && log.content.startsWith('【系统补齐')
    const tag = isAutoFilled ? '系统补齐自项目进展' : '已生成 AI 工作日志'
    return meta
      ? `${dateStr} · ${tag}（另有 ${meta.count} 条项目进展）`
      : `${dateStr} · ${tag}`
  }
  if (meta) {
    return `${dateStr} · ${meta.count} 条项目进展（未生成工作日志）`
  }
  return dateStr
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
  
  console.log(`选择日期: ${dateStr}`)
  
  // 从已加载的活动记录中获取当天的活动
  let activities = dailyActivities.value[dateStr] || []
  
  // 如果没有活动记录，尝试从API获取
  if (activities.length === 0) {
    console.log(`从API获取${dateStr}的活动记录`)
    activities = await getDateActivities(dateStr)
    // 保存到dailyActivities中
    if (activities.length > 0) {
      dailyActivities.value[dateStr] = activities
    }
  } else {
    console.log(`从本地获取${dateStr}的活动记录:`, activities)
  }
  
  currentActivities.value = activities
  
  // 构建提示词但不显示，只在生成日志时使用
  if (activities.length > 0) {
    const isTodaySelected = isToday(day)
    const datePrompt = isTodaySelected ? '今天' : dateStr
    currentPrompt.value = `假设你是一位售前工程师，为了向公司展示项目进度和工作进度，请根据以下${datePrompt}的活动记录，生成一份工作日志，字数不少于40字：\n${activities.join('\n')}`
  } else {
    currentPrompt.value = ''
  }

  // 按日期加载该日的工作日志（跨当前登录用户，与仪表盘跳转逻辑一致）
  await loadLogOfDate(dateStr)
}

// 防止快速切换日期时旧请求覆盖新结果
let logFetchSeq = 0

// 按日期查询当天工作日志（无则置空）
const loadLogOfDate = async (dateStr: string) => {
  const seq = ++logFetchSeq
  try {
    const resp = await fetch(`/api/work-log/date/${dateStr}`)
    if (seq !== logFetchSeq) return
    if (!resp.ok) {
      selectedLog.value = null
      return
    }
    const data = await resp.json()
    if (seq !== logFetchSeq) return
    if (data && data.work_log_by_ai) {
      selectedLog.value = { date: dateStr, content: data.work_log_by_ai }
    } else {
      selectedLog.value = null
    }
  } catch (e) {
    if (seq === logFetchSeq) selectedLog.value = null
  }
}

// 获取指定日期的活动（按顺序尝试多个后端接口，并对非 JSON 响应做容错，
// 避免部署版本不一致时拿到 SPA 兜底的 HTML 引发 SyntaxError）
const getDateActivities = async (dateStr: string) => {
  const urls = [
    `/api/projects/date-progress/${dateStr}`,
    `/api/work-log/date-activities/${dateStr}`
  ]
  for (const url of urls) {
    try {
      const response = await fetch(url)
      if (!response.ok) continue
      const ct = response.headers.get('content-type') || ''
      if (!ct.includes('application/json')) continue
      const data = await response.json()
      return Array.isArray(data) ? data : []
    } catch (error) {
      console.error(`通过${url}获取${dateStr}活动失败:`, error)
    }
  }
  return []
}

let monthCacheWarned = false

// 加载当月“有项目进展的日期”：只依赖后端缓存接口（/api/projects/month-days）。
// 缓存文件命中的情况下后端毫秒级返回，日历颜色立即出现。
// 注意：绝不在此做“逐日请求”兜底——那会让老后端下颜色等几十秒才出现。
const loadProgressDaysOfMonth = async () => {
  const key = getMonthKey(currentYear.value, currentMonth.value)
  if (progressDaysByMonth.value[key]) return

  try {
    const response = await fetch(
      `/api/projects/month-days?year=${currentYear.value}&month=${currentMonth.value + 1}`
    )
    const ct = response.headers.get('content-type') || ''
    if (!response.ok || !ct.includes('application/json')) {
      if (!monthCacheWarned) {
        monthCacheWarned = true
        console.warn(
          `缓存接口 /api/projects/month-days 不可用，日历进度标记不可用。` +
          `请确认后端已更新 project_routes.py 并重启服务。`
        )
      }
      progressDaysByMonth.value = { ...progressDaysByMonth.value, [key]: [] }
      return
    }
    const data = await response.json()
    progressDaysByMonth.value = {
      ...progressDaysByMonth.value,
      [key]: Array.isArray(data.days) ? data.days : []
    }
  } catch (error) {
    if (!monthCacheWarned) {
      monthCacheWarned = true
      console.warn(`加载${key}进展日期失败，请检查后端服务:`, error)
    }
    progressDaysByMonth.value = { ...progressDaysByMonth.value, [key]: [] }
  }
}

// 调用大模型API生成日志
const generateLog = async () => {
  isGenerating.value = true
  try {
    console.log('开始生成日志')
    // 获取当前登录用户ID
    let currentUserId = 1 // 默认值
    const userStr = sessionStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        currentUserId = user.id || 1
        console.log('获取到用户ID:', currentUserId)
      } catch (e) {
        console.error('解析用户信息失败:', e)
      }
    }
    
    // 检查是否有活动记录
    if (currentActivities.value.length === 0) {
      console.log('没有活动记录，开始生成')
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
        console.log('生成的活动记录:', currentActivities.value)
        
        // 构建提示词
        if (currentActivities.value.length > 0) {
          currentPrompt.value = `假设你是一位售前工程师，为了向公司展示项目进度和工作进度，请根据以下今天的活动记录，生成一份工作日志，字数不少于40字：\n${currentActivities.value.join('\n')}`
          console.log('构建的提示词:', currentPrompt.value)
        } else {
          console.log('今天没有活动记录')
          return
        }
      } else {
        console.error('生成活动记录失败:', await generateResponse.text())
        return
      }
    } else {
      console.log('已有活动记录:', currentActivities.value)
      console.log('当前提示词:', currentPrompt.value)
    }
    
    // 从localStorage获取AI设置
    const aiSettingsStr = localStorage.getItem('aiSettings')
    let model = 'deepseek' // 默认模型
    let apiKey = ''
    if (aiSettingsStr) {
      const aiSettings = JSON.parse(aiSettingsStr)
      model = aiSettings.defaultModel || 'deepseek'
      apiKey = aiSettings.apiKeys?.[model] || ''
      console.log('获取到AI设置:', { model, apiKey: apiKey ? '已设置' : '未设置' })
    } else {
      console.log('未找到AI设置，使用默认值')
    }
    
    // 调用大模型API
    console.log('开始调用大模型API')
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
    
    console.log('API调用响应状态:', response.status)
    if (response.ok) {
      const data = await response.json()
      console.log('API调用成功，返回数据:', data)
      generatedLog.value = data.content
      // 清除selectedLog，这样按钮会显示"生成今日日志"
      selectedLog.value = null
    } else {
      const errorText = await response.text()
      console.error('生成日志失败:', errorText)
    }
  } catch (error) {
    console.error('生成日志失败:', error)
  } finally {
    isGenerating.value = false
    console.log('生成日志过程结束')
  }
}

// 保存日志
const saveLog = async () => {
  if (!generatedLog.value) return
  
  try {
    // 获取当前登录用户ID
    let currentUserId = 1 // 默认值
    const userStr = sessionStorage.getItem('user')
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
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]

  // 支持从 URL 直接指定日期（仪表盘日历点击某天跳转而来）：/work-log?date=YYYY-MM-DD
  const paramDate = typeof route.query.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(route.query.date)
    ? route.query.date
    : null

  // 目标日期：有 ?date 则用该日期并定位到对应月份，否则定位今天
  let targetDateStr = todayStr
  if (paramDate) {
    targetDateStr = paramDate
    const [y, m, d] = paramDate.split('-').map(Number)
    currentDate.value = new Date(y, m - 1, 1)
    selectedDate.value = d
  } else {
    selectedDate.value = today.getDate()
  }
  const isTodayTarget = targetDateStr === todayStr

  // 获取当前登录用户ID
  let currentUserId = 1 // 默认值
  const userStr = sessionStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      currentUserId = user.id || 1
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }

  // 并行初始化：日历颜色只等缓存接口一次请求，不被活动/AI日志串行拖慢
  await Promise.all([
    // ① 目标月份有进展的日期（渲染日历底色）
    loadProgressDaysOfMonth(),

    // ② 目标日期的活动记录 + 提示词
    (async () => {
      try {
        const activities = await getDateActivities(targetDateStr)
        currentActivities.value = activities
        if (activities.length > 0) {
          currentPrompt.value = `假设你是一位售前工程师，为了向公司展示项目进度和工作进度，请根据以下${isTodayTarget ? '今天的' : targetDateStr + '的'}活动记录，生成一份工作日志，字数不少于40字：\n${activities.join('\n')}`
        }
      } catch (e) {
        console.error('获取目标日期活动失败:', e)
      }
    })(),

    // ③ 目标日期的工作日志 + 全部 AI 日志（hasLog 深绿标记）
    (async () => {
      try {
        await loadLogOfDate(targetDateStr)
        const logsResponse = await fetch(`/api/work-log/user/${currentUserId}`)
        if (logsResponse.ok) {
          const logsData = await logsResponse.json()
          workLogs.value = logsData.map((log: any) => ({
            date: log.log_date,
            content: log.work_log_by_ai
          }))
        }
      } catch (e) {
        console.error('加载工作日志失败:', e)
      }
    })()
  ])
})

// 组件卸载时清理
onUnmounted(() => {
  // 清理工作
})
</script>

<style scoped>
/* 工作日志页面 - 马卡龙风格 */
.work-log {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
}

.work-log h1 {
  text-align: left;
  color: #5D5A6D;
  margin-bottom: 24px;
  font-size: 22px;
  font-weight: 700;
}

/* 主内容布局 */
.work-log-content {
  display: flex;
  gap: 24px;
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

/* 日历样式 - 马卡龙风格 */
.calendar-container {
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  width: 100%;
  position: relative;
}

.calendar-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #7EC8E3, #6BB8D3);
  border-radius: 20px 20px 0 0;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.calendar-header h2 {
  margin: 0;
  color: #5D5A6D;
  font-size: 16px;
  font-weight: 600;
}

.calendar-header .btn {
  padding: 8px 14px;
  font-size: 12px;
  border-radius: 10px;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 4px;
}

.weekday {
  text-align: center;
  font-weight: 600;
  color: #8B8899;
  padding: 8px 4px;
  font-size: 11px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  font-size: 13px;
  min-height: 36px;
  max-height: 46px;
  color: #5D5A6D;
  font-weight: 500;
}

.calendar-day:hover {
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.3), rgba(168, 230, 207, 0.1));
  transform: scale(1.05);
}

.calendar-day.other-month {
  color: #D4C4F0;
}

.calendar-day.future-day {
  color: #D4C4F0;
  cursor: not-allowed;
}

.calendar-day.future-day:hover {
  background: transparent;
  transform: none;
}

.calendar-day.today {
  background: linear-gradient(135deg, #7EC8E3, #6BB8D3);
  color: white;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(126, 200, 227, 0.4);
}

.calendar-day.selected {
  background: linear-gradient(135deg, #C3B1E1, #B19FD0);
  color: white;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(195, 177, 225, 0.4);
}

.calendar-day.has-log {
  background: linear-gradient(135deg, #A8E6CF, #7DD3C0);
  color: white;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(168, 230, 207, 0.4);
}

.calendar-day.has-activities {
  background: linear-gradient(135deg, #F1F8F1, #E8F5E8);
  color: #5D5A6D;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(168, 230, 207, 0.2);
}

.calendar-day.selected {
  background: linear-gradient(135deg, #A78ED1, #9575C9);
  color: white;
  font-weight: 700;
  box-shadow: 0 6px 16px rgba(195, 177, 225, 0.5);
}

.today-indicator {
  position: absolute;
  bottom: 4px;
  width: 6px;
  height: 6px;
  background-color: white;
  border-radius: 50%;
  opacity: 0.8;
}

.log-indicator {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, #FF9A8B, #FFB7B2);
  border-radius: 50%;
  opacity: 0.9;
}

/* 日历图例 */
.calendar-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 12px;
  font-size: 11px;
  color: #8B8899;
  justify-content: center;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.legend-item::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 4px;
  background: #fff;
  border: 1px solid #F0E6E3;
}

.legend-today::before {
  background: linear-gradient(135deg, #7EC8E3, #6BB8D3);
  border-color: transparent;
}

.legend-log::before {
  background: linear-gradient(135deg, #A8E6CF, #7DD3C0);
  border-color: transparent;
}

.legend-activities::before {
  background: linear-gradient(135deg, #F1F8F1, #E8F5E8);
  border-color: #D4EAD8;
}

/* 生成日志按钮 */
.generate-log-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

/* 日志内容 */
.log-content {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  position: relative;
}

.log-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #FF9A8B, #FFB7B2);
  border-radius: 20px 20px 0 0;
}

/* AI内容区域 */
.ai-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 提示词内容 */
.prompt-content {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  position: relative;
}

.prompt-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #A8E6CF, #C3B1E1);
  border-radius: 20px 20px 0 0;
}

/* 空状态 */
.empty-state {
  background: white;
  border-radius: 20px;
  padding: 60px 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  text-align: center;
  color: #8B8899;
  position: relative;
}

.empty-state::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #FFEAA7, #FDCB6E);
  border-radius: 20px 20px 0 0;
}

.log-content h3,
.prompt-content h3 {
  color: #5D5A6D;
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
}

.log-text {
  line-height: 1.8;
  color: #5D5A6D;
  white-space: pre-wrap;
  font-size: 14px;
}

.log-actions {
  margin-top: 20px;
  text-align: right;
}

/* 模型选择 */
.model-selector {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  position: relative;
}

.model-selector::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #C3B1E1, #D4C4F0);
  border-radius: 20px 20px 0 0;
}

.model-selector h3 {
  color: #5D5A6D;
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
}

.model-options {
  display: flex;
  gap: 20px;
}

.model-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #5D5A6D;
}

/* 按钮样式 - 马卡龙风格 */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary {
  background: linear-gradient(135deg, #A8E6CF, #7DD3C0);
  color: white;
  box-shadow: 0 4px 12px rgba(168, 230, 207, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(168, 230, 207, 0.5);
}

.btn-secondary {
  background: linear-gradient(135deg, #C3B1E1, #B19FD0);
  color: white;
  box-shadow: 0 4px 12px rgba(195, 177, 225, 0.4);
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(195, 177, 225, 0.5);
}

.btn:disabled {
  background: #D4C4F0;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

/* 弹窗样式 - 马卡龙风格 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(93, 90, 109, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 20px;
  width: 80%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border: 1px solid #F0E6E3;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.1), rgba(195, 177, 225, 0.1));
}

.modal-header h3 {
  margin: 0;
  color: #5D5A6D;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: rgba(255, 154, 139, 0.1);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 20px;
  color: #FF9A8B;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 154, 139, 0.2);
  transform: rotate(90deg);
}

.modal-body {
  padding: 24px;
}

.prompt-section {
  margin-bottom: 20px;
}

.prompt-section h4 {
  margin: 0 0 12px 0;
  color: #5D5A6D;
  font-size: 14px;
  font-weight: 600;
}

.activities-list {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.activities-list li {
  margin-bottom: 12px;
  color: #5D5A6D;
  line-height: 1.6;
  padding: 12px 16px;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.1), rgba(195, 177, 225, 0.05));
  border-radius: 12px;
  border-left: 3px solid #A8E6CF;
  font-size: 13px;
}

.prompt-text {
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.1), rgba(195, 177, 225, 0.05));
  padding: 16px;
  border-radius: 12px;
  border-left: 3px solid #7EC8E3;
  font-family: monospace;
  white-space: pre-wrap;
  line-height: 1.6;
  color: #5D5A6D;
  font-size: 13px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 20px 24px;
  border-top: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.05), rgba(195, 177, 225, 0.05));
}

/* ==================== 移动端适配 ==================== */
@media (max-width: 860px) {
  .work-log-content {
    flex-direction: column;
  }

  .left-section {
    flex: 1 1 auto;
    width: 100%;
  }

  .right-section {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .work-log {
    padding: 0;
  }

  .calendar-container {
    padding: 12px;
  }

  .calendar-header {
    flex-wrap: wrap;
    gap: 6px;
    justify-content: center;
  }

  .calendar-header h2 {
    order: -1;
    width: 100%;
    text-align: center;
    font-size: 15px;
  }

  .calendar-header .btn {
    padding: 6px 10px;
    font-size: 11px;
  }

  .calendar-day {
    min-height: 30px;
    max-height: 40px;
    font-size: 12px;
    border-radius: 8px;
  }

  .calendar-weekdays,
  .calendar-days {
    gap: 2px;
  }

  .log-content,
  .prompt-content,
  .model-selector {
    padding: 16px;
    border-radius: 16px;
  }

  .empty-state {
    padding: 40px 16px;
  }

  .activities-list li {
    padding: 10px 12px;
  }

  .modal {
    width: 95%;
  }
}
</style>
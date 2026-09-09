<template>
  <div class="month-calendar">
    <div class="calendar-header">
      <button class="cal-nav-btn" @click="prevMonth" title="上个月">&lt;</button>
      <h4>{{ currentYear }}年{{ currentMonth + 1 }}月</h4>
      <button class="cal-nav-btn" @click="nextMonth" title="下个月">&gt;</button>
    </div>

    <div class="calendar-weekdays">
      <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
    </div>

    <div class="calendar-days">
      <div v-for="day in prevMonthDays" :key="`prev-${day}`" class="calendar-day other-month">{{ day }}</div>
      <div
        v-for="day in currentMonthDays"
        :key="`cur-${day}`"
        class="calendar-day"
        :class="{
          'today': isToday(day),
          'has-log': hasAiLog(day),
          'has-activities': hasProgress(day) && !hasAiLog(day),
          'future-day': isFutureDay(day),
          'selected': day === selectedDate
        }"
        :title="getDayTooltip(day)"
        @click="selectDay(day)"
      >
        {{ day }}
        <div v-if="isToday(day)" class="today-indicator"></div>
        <div v-if="hasAiLog(day)" class="log-indicator"></div>
      </div>
      <div v-for="day in nextMonthDays" :key="`next-${day}`" class="calendar-day other-month">{{ day }}</div>
    </div>

    <div v-if="showLegend" class="calendar-legend">
      <span class="legend-item legend-today">今天</span>
      <span class="legend-item legend-log">已生成 AI 日志</span>
      <span class="legend-item legend-activities">仅有项目进展</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 复用与工作日志页相同的配色与数据源（/api/projects/month-days 缓存接口）
const props = withDefaults(defineProps<{
  /** 初始选中的日期，格式 YYYY-MM-DD（可选） */
  initialDate?: string
  /** 是否显示图例，默认显示 */
  showLegend?: boolean
}>(), { showLegend: true })

const emit = defineEmits<{ (e: 'select', date: string): void }>()

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

const today = new Date()
const currentDate = ref<Date>(new Date(today.getFullYear(), today.getMonth(), 1))
const selectedDate = ref<number | null>(null)

// 当月“有进展的日期”，来自后端 JSON 缓存
const progressDaysByMonth = ref<Record<string, { day: number; count: number }[]>>({})
// 当前用户“已生成 AI 日志”的日期（深绿）
const aiLogDates = ref<string[]>([])

if (props.initialDate && /^\d{4}-\d{2}-\d{2}$/.test(props.initialDate)) {
  const [y, m, d] = props.initialDate.split('-').map(Number)
  currentDate.value = new Date(y, m - 1, 1)
  selectedDate.value = d
}

const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth())

const firstDayOfMonth = computed(() => new Date(currentYear.value, currentMonth.value, 1))
const lastDayOfMonth = computed(() => new Date(currentYear.value, currentMonth.value + 1, 0))
const startDay = computed(() => firstDayOfMonth.value.getDay())
const daysInMonth = computed(() => lastDayOfMonth.value.getDate())

const prevMonthDays = computed(() => {
  const days: number[] = []
  const prevLast = new Date(currentYear.value, currentMonth.value, 0).getDate()
  for (let i = startDay.value - 1; i >= 0; i--) days.push(prevLast - i)
  return days
})

const currentMonthDays = computed(() => {
  const days: number[] = []
  for (let i = 1; i <= daysInMonth.value; i++) days.push(i)
  return days
})

const nextMonthDays = computed(() => {
  const days: number[] = []
  const total = prevMonthDays.value.length + currentMonthDays.value.length
  for (let i = 1; i <= 42 - total; i++) days.push(i)
  return days
})

const getMonthKey = (year: number, month: number) => `${year}-${String(month + 1).padStart(2, '0')}`

const dateStrOf = (day: number) =>
  `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`

const getDayProgress = (day: number) => {
  const key = getMonthKey(currentYear.value, currentMonth.value)
  const list = progressDaysByMonth.value[key] || []
  return list.find(d => d.day === day) || null
}

const hasProgress = (day: number) => !!getDayProgress(day)

const hasAiLog = (day: number) => aiLogDates.value.includes(dateStrOf(day))

const isToday = (day: number) => {
  const t = new Date()
  return t.getFullYear() === currentYear.value &&
         t.getMonth() === currentMonth.value &&
         t.getDate() === day
}

const isFutureDay = (day: number) => {
  const d = new Date(currentYear.value, currentMonth.value, day)
  const t = new Date()
  t.setHours(0, 0, 0, 0)
  return d > t
}

const getDayTooltip = (day: number) => {
  const dateStr = dateStrOf(day)
  const meta = getDayProgress(day)
  const ai = hasAiLog(day)
  if (ai) {
    return meta
      ? `${dateStr} · 已生成 AI 工作日志（另有 ${meta.count} 条项目进展）`
      : `${dateStr} · 已生成 AI 工作日志`
  }
  if (meta) return `${dateStr} · ${meta.count} 条项目进展`
  return dateStr
}

const prevMonth = async () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
  selectedDate.value = null
  await loadProgressDaysOfMonth()
}

const nextMonth = async () => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
  selectedDate.value = null
  await loadProgressDaysOfMonth()
}

const selectDay = (day: number) => {
  if (isFutureDay(day)) return
  selectedDate.value = day
  emit('select', dateStrOf(day))
}

// 只依赖 month-days 缓存接口（后端读 JSON 缓存文件，命中毫秒返回）
const loadProgressDaysOfMonth = async () => {
  const key = getMonthKey(currentYear.value, currentMonth.value)
  if (progressDaysByMonth.value[key]) return
  try {
    const resp = await fetch(
      `/api/projects/month-days?year=${currentYear.value}&month=${currentMonth.value + 1}`
    )
    const ct = resp.headers.get('content-type') || ''
    if (!resp.ok || !ct.includes('application/json')) return
    const data = await resp.json()
    progressDaysByMonth.value = {
      ...progressDaysByMonth.value,
      [key]: Array.isArray(data.days) ? data.days : []
    }
  } catch (e) {
    console.error('加载月份进展日期失败:', e)
  }
}

// 加载当前用户已生成 AI 日志的日期（用于深绿标记）
const fetchAiLogDates = async () => {
  try {
    let uid = 1
    const userStr = sessionStorage.getItem('user')
    if (userStr) {
      try { uid = JSON.parse(userStr).id || 1 } catch { /* ignore */ }
    }
    const resp = await fetch(`/api/work-log/user/${uid}`)
    if (resp.ok) {
      const data = await resp.json()
      aiLogDates.value = (Array.isArray(data) ? data : [])
        .map((l: any) => l.log_date)
        .filter((v: unknown) => typeof v === 'string')
    }
  } catch (e) {
    console.error('加载 AI 日志日期失败:', e)
  }
}

onMounted(() => {
  loadProgressDaysOfMonth()
  fetchAiLogDates()
})
</script>

<style scoped>
/* ===== 日历主体（与工作日志页一致，可嵌入任何卡片） ===== */
.month-calendar {
  width: 100%;
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}

.calendar-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: #5D5A6D;
  white-space: nowrap;
}

.cal-nav-btn {
  background: linear-gradient(135deg, #C3B1E1, #B19FD0);
  color: #fff;
  border: none;
  border-radius: 8px;
  width: 26px;
  height: 26px;
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(195, 177, 225, 0.3);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.cal-nav-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(195, 177, 225, 0.45);
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 3px;
  margin-bottom: 3px;
}

.weekday {
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  color: #8B8899;
  padding: 2px 0;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  /* 让 6 行日期平分父容器剩余高度，无论卡片高度多少都能完整显示 */
  grid-auto-rows: 1fr;
  gap: 3px;
  flex: 1;
  min-height: 0;
}

.calendar-day {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #5D5A6D;
  position: relative;
  cursor: pointer;
  transition: transform 0.15s ease, background 0.15s ease;
  min-height: 22px;
  /* 由 grid-auto-rows 平分空间，不依赖宽度算高度 */
}

.calendar-day:hover {
  transform: scale(1.06);
}

.calendar-day.other-month,
.calendar-day.future-day {
  color: #D4C4F0;
  cursor: not-allowed;
}

.calendar-day.other-month:hover,
.calendar-day.future-day:hover {
  transform: none;
}

.calendar-day.today {
  background: linear-gradient(135deg, #7EC8E3, #6BB8D3);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(126, 200, 227, 0.35);
}

.calendar-day.has-log {
  background: linear-gradient(135deg, #A8E6CF, #7DD3C0);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(168, 230, 207, 0.35);
}

.calendar-day.has-activities {
  background: linear-gradient(135deg, #F1F8F1, #E8F5E8);
  color: #5D5A6D;
  font-weight: 600;
}

.calendar-day.selected {
  outline: 2px solid #B19FD0;
  outline-offset: 1px;
}

.today-indicator {
  position: absolute;
  bottom: 2px;
  width: 5px;
  height: 5px;
  background: #fff;
  border-radius: 50%;
  opacity: 0.85;
}

.log-indicator {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 5px;
  height: 5px;
  background: linear-gradient(135deg, #FF9A8B, #FFB7B2);
  border-radius: 50%;
}

/* 图例 */
.calendar-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 8px;
  font-size: 10px;
  color: #8B8899;
  justify-content: center;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.legend-item::before {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 3px;
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
</style>

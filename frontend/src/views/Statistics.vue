<template>
  <div class="statistics">
    <div class="statistics-header">
      <h3>项目统计分析</h3>
      <div class="year-filter">
        <span class="year-filter-label">统计年份</span>
        <select v-model="selectedYear" class="year-select" aria-label="统计年份">
          <option value="all">所有年份</option>
          <option v-for="y in yearOptions" :key="y" :value="y">{{ y }} 年</option>
        </select>
        <span class="filter-count">共 {{ filteredCount }} 个项目</span>
      </div>
    </div>

    <!-- 图表容器 -->
    <div class="charts-container">
      <!-- 各省份项目数量分布 -->
      <div class="chart-card">
        <h4>各省份项目数量分布</h4>
        <div class="chart">
          <canvas ref="provinceCountChart"></canvas>
        </div>
      </div>
      
      <!-- 各省份项目金额分布 -->
      <div class="chart-card">
        <h4>各省份项目金额分布</h4>
        <div class="chart">
          <canvas ref="provinceAmountChart"></canvas>
        </div>
      </div>
      
      <!-- 各阶段项目数量 -->
      <div class="chart-card">
        <h4>各阶段项目数量</h4>
        <div class="chart">
          <canvas ref="stageCountChart"></canvas>
        </div>
      </div>
      
      <!-- 月度新增项目趋势 -->
      <div class="chart-card">
        <h4>月度新增项目趋势</h4>
        <div class="chart">
          <canvas ref="monthlyTrendChart"></canvas>
        </div>
      </div>
      
      <!-- 项目规模分布 -->
      <div class="chart-card">
        <h4>项目规模分布</h4>
        <div class="chart">
          <canvas ref="scaleDistributionChart"></canvas>
        </div>
      </div>
      
      <!-- 项目完成金额统计 -->
      <div class="chart-card">
        <h4>项目完成金额统计</h4>
        <div class="chart">
          <canvas ref="maintenanceTrendChart"></canvas>
        </div>
      </div>

      <!-- 周日志数量统计 -->
      <div class="chart-card">
        <h4>周日志数量（{{ weekLogTitle }}）</h4>
        <div class="chart">
          <canvas ref="weekLogChart"></canvas>
        </div>
      </div>

      <!-- 月日志数量统计 -->
      <div class="chart-card">
        <h4>月日志数量（{{ monthLogTitle }}）</h4>
        <div class="chart">
          <canvas ref="monthLogChart"></canvas>
        </div>
      </div>
    </div>
    
    <!-- 表格容器 -->
    <div class="tables-container">
      <!-- 销售额统计数据 -->
      <div class="table-card">
        <h4>销售额统计数据</h4>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>省份</th>
                <th>省份统计(万元)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in salesStatistics" :key="index">
                <td>{{ item.province }}</td>
                <td>{{ item.amount }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- 各阶段统计 -->
      <div class="table-card">
        <h4>各阶段统计</h4>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>阶段</th>
                <th>各阶段统计</th>
                <th>项目数量</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in stageStatistics" :key="index">
                <td>{{ item.stage }}</td>
                <td>{{ item.stageText }}</td>
                <td>{{ item.count }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import Chart from 'chart.js/auto'
import * as echarts from 'echarts'

// 年份筛选（默认为本年度，'all' 表示所有年份；按项目创建日期 start_date 归年）
const currentYear = new Date().getFullYear()
const selectedYear = ref<number | string>(currentYear)
const yearOptions = ref<number[]>([])

// 图表引用
const provinceCountChart = ref(null)
const provinceAmountChart = ref(null)
const stageCountChart = ref(null)
const monthlyTrendChart = ref(null)
const scaleDistributionChart = ref(null)
const maintenanceTrendChart = ref(null)
const weekLogChart = ref(null)
const monthLogChart = ref(null)

// 数据
const projects = ref([])
const salesStatistics = ref([])
const stageStatistics = ref([])

// 图表实例缓存（切换年份时先销毁再重建）
const chartInstances: Record<string, any> = {}

const createChart = (key: string, canvas: any, config: any) => {
  if (!canvas) return
  if (chartInstances[key]) {
    chartInstances[key].destroy()
  }
  chartInstances[key] = new Chart(canvas.getContext('2d'), config)
}

const destroyAllCharts = () => {
  Object.keys(chartInstances).forEach(key => {
    if (chartInstances[key]) {
      chartInstances[key].destroy()
      delete chartInstances[key]
    }
  })
}

// 按所选年份过滤项目（以项目创建日期 start_date 为时间点）
const filteredProjects = computed(() => {
  if (selectedYear.value === 'all') return projects.value
  const year = Number(selectedYear.value)
  return projects.value.filter((p: any) => {
    if (!p.start_date) return false
    return parseInt(String(p.start_date).substring(0, 4)) === year
  })
})

const filteredCount = computed(() => filteredProjects.value.length)

const weekLogTitle = computed(() => {
  if (selectedYear.value === 'all' || Number(selectedYear.value) === currentYear) return '近12周'
  return `${selectedYear.value}年末12周`
})

const monthLogTitle = computed(() => {
  if (selectedYear.value === 'all') return '近12个月'
  return `${selectedYear.value}年1-12月`
})

// 项目阶段映射（统一 5 档）
const stages = {
  '立项中': [1],
  '已立项': [2],
  '招投标': [3],
  '已中标': [4],
  '已完成': [5]
}

// 从API获取项目数据
const fetchProjects = async () => {
  try {
    const response = await fetch('/api/projects/')
    const data = await response.json()
    projects.value = data
    buildYearOptions(data)
    return data
  } catch (error) {
    console.error('获取项目数据失败:', error)
    return []
  }
}

// 依据项目创建日期生成可选年份（降序），并保证当前年份存在
const buildYearOptions = (projectData) => {
  const yearSet = new Set<number>()
  projectData.forEach((p: any) => {
    if (p.start_date) {
      const y = parseInt(String(p.start_date).substring(0, 4))
      if (!isNaN(y)) yearSet.add(y)
    }
  })
  yearSet.add(currentYear)
  yearOptions.value = Array.from(yearSet).sort((a, b) => b - a)
}

// 计算各省份项目数量分布
const calculateProvinceCountDistribution = (projectData) => {
  const provinceCount = {}
  
  projectData.forEach(project => {
    if (project.province) {
      provinceCount[project.province] = (provinceCount[project.province] || 0) + 1
    }
  })
  
  return provinceCount
}

// 计算各省份项目金额分布
const calculateProvinceAmountDistribution = (projectData) => {
  const provinceAmount = {}
  
  projectData.forEach(project => {
    if (project.province && project.scale) {
      const amount = parseFloat(project.scale) || 0
      provinceAmount[project.province] = (provinceAmount[project.province] || 0) + amount
    }
  })
  
  return provinceAmount
}

// 计算各阶段项目数量
const calculateStageCount = (projectData) => {
  const stageCount = {
    '立项中': 0,
    '已立项': 0,
    '招投标': 0,
    '已中标': 0,
    '已完成': 0
  }
  
  projectData.forEach(project => {
    if (project.stage) {
      const stageNum = parseInt(project.stage)
      
      for (const [stageName, stageValues] of Object.entries(stages)) {
        if (stageValues.includes(stageNum)) {
          stageCount[stageName]++
          break
        }
      }
    }
  })
  
  return stageCount
}

// 计算月度新增项目趋势（指定年份时补齐该年 1-12 月）
const calculateMonthlyTrend = (projectData, year) => {
  const monthlyTrend = {}
  
  if (year !== 'all') {
    for (let m = 1; m <= 12; m++) {
      monthlyTrend[`${year}-${m.toString().padStart(2, '0')}`] = 0
    }
  }
  
  projectData.forEach(project => {
    if (project.start_date) {
      const month = project.start_date.substring(0, 7) // 提取年月，格式：YYYY-MM
      monthlyTrend[month] = (monthlyTrend[month] || 0) + 1
    }
  })
  
  // 按月份排序
  const sortedMonths = Object.keys(monthlyTrend).sort()
  const sortedTrend = {}
  sortedMonths.forEach(month => {
    sortedTrend[month] = monthlyTrend[month]
  })
  
  return sortedTrend
}

// 计算项目规模分布
const calculateScaleDistribution = (projectData) => {
  const scaleDistribution = {
    '0-100': 0,
    '100-500': 0,
    '500-1000': 0,
    '1000+': 0
  }
  
  projectData.forEach(project => {
    if (project.scale) {
      const amount = parseFloat(project.scale) || 0
      
      if (amount <= 100) {
        scaleDistribution['0-100']++
      } else if (amount <= 500) {
        scaleDistribution['100-500']++
      } else if (amount <= 1000) {
        scaleDistribution['500-1000']++
      } else {
        scaleDistribution['1000+']++
      }
    }
  })
  
  return scaleDistribution
}

// 计算销售额统计数据
const calculateSalesStatistics = (projectData) => {
  const provinceAmount = {}
  
  projectData.forEach(project => {
    if (project.province && project.scale) {
      const amount = parseFloat(project.scale) || 0
      provinceAmount[project.province] = (provinceAmount[project.province] || 0) + amount
    }
  })
  
  // 转换为数组并排序
  return Object.entries(provinceAmount)
    .map(([province, amount]) => ({ province, amount: (amount as number).toFixed(2) }))
    .sort((a, b) => parseFloat(b.amount) - parseFloat(a.amount))
}

// 计算各阶段统计
const calculateStageStatistics = (projectData) => {
  const stageCount = calculateStageCount(projectData)
  
  return Object.entries(stageCount)
    .map(([stage, count]) => ({
      stage,
      stageText: stage,
      count
    }))
}

// 计算每个省份的详细统计数据
const calculateProvinceDetailedStats = (projectData) => {
  const provinceStats = {}
  
  projectData.forEach(project => {
    if (project.province) {
      if (!provinceStats[project.province]) {
        provinceStats[project.province] = {
          totalCount: 0,
          completedCount: 0,
          inProgressCount: 0,
          totalAmount: 0,
          completedAmount: 0,
          inProgressAmount: 0
        }
      }
      
      // 增加总项目数
      provinceStats[project.province].totalCount++
      
      // 增加总金额
      const amount = parseFloat(project.scale) || 0
      provinceStats[project.province].totalAmount += amount
      
      // 判断项目是否已完成（5 = 已完成）
      if (project.stage) {
        const stageNum = parseInt(project.stage)
        if (stageNum === 5) {
          // 已完成项目
          provinceStats[project.province].completedCount++
          provinceStats[project.province].completedAmount += amount
        } else {
          // 进行中项目
          provinceStats[project.province].inProgressCount++
          provinceStats[project.province].inProgressAmount += amount
        }
      } else {
        // 无阶段信息，视为进行中
        provinceStats[project.province].inProgressCount++
        provinceStats[project.province].inProgressAmount += amount
      }
    }
  })
  
  return provinceStats
}

// 绘制各省份项目数量分布饼图
const drawProvinceCountChart = (provinceCount) => {
  if (!provinceCountChart.value) return
  
  const labels = Object.keys(provinceCount)
  const data = Object.values(provinceCount)
  
  createChart('provinceCount', provinceCountChart.value, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#8ACB88', '#FF6B6B', '#4ECDC4', '#45B7D1',
          '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

// 绘制各省份项目金额分布饼图
const drawProvinceAmountChart = (provinceAmount) => {
  if (!provinceAmountChart.value) return
  
  const labels = Object.keys(provinceAmount)
  const data = Object.values(provinceAmount)
  
  createChart('provinceAmount', provinceAmountChart.value, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
          '#FF9F40', '#8ACB88', '#FF6B6B', '#4ECDC4', '#45B7D1',
          '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

// 绘制各阶段项目数量柱状图
const drawStageCountChart = (stageCount) => {
  if (!stageCountChart.value) return
  
  const labels = Object.keys(stageCount)
  const data = Object.values(stageCount)
  
  createChart('stageCount', stageCountChart.value, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '项目数量',
        data: data,
        backgroundColor: '#36A2EB',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

// 绘制月度新增项目趋势折线图
const drawMonthlyTrendChart = (monthlyTrend) => {
  if (!monthlyTrendChart.value) return
  
  const labels = Object.keys(monthlyTrend)
  const data = Object.values(monthlyTrend)
  
  createChart('monthlyTrend', monthlyTrendChart.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '新增项目数量',
        data: data,
        borderColor: '#FF6384',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.1,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  })
}

// 绘制项目规模分布饼图
const drawScaleDistributionChart = (scaleDistribution) => {
  if (!scaleDistributionChart.value) return
  
  const labels = Object.keys(scaleDistribution)
  const data = Object.values(scaleDistribution)
  
  createChart('scaleDistribution', scaleDistributionChart.value, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}

// 计算项目完成金额统计（阶段 4 已中标及以上视为完成；指定年份时统计该年 1-12 月）
const calculateCompletedAmountTrend = (projectData, year) => {
  const monthlyAmount = {}
  
  // 指定年份时初始化该年 1-12 月
  if (year !== 'all') {
    for (let month = 1; month <= 12; month++) {
      monthlyAmount[`${year}-${month.toString().padStart(2, '0')}`] = 0
    }
  }
  
  projectData.forEach(project => {
    if (project.start_date && project.scale) {
      const month = project.start_date.substring(0, 7)
      const stageNum = parseInt(project.stage)

      // 已中标(4)及以上视为进入高阶段/完成统计
      if (stageNum >= 4) {
        const amount = parseFloat(project.scale) || 0
        monthlyAmount[month] = (monthlyAmount[month] || 0) + amount
      }
    }
  })
  
  // 按月份排序
  const sortedMonths = Object.keys(monthlyAmount).sort()
  const sortedTrend = {}
  sortedMonths.forEach(month => {
    sortedTrend[month] = monthlyAmount[month]
  })
  
  return sortedTrend
}

// 绘制项目完成金额统计折线图
const drawMaintenanceTrendChart = (completedAmountTrend, year) => {
  if (!maintenanceTrendChart.value) return
  
  const labels = Object.keys(completedAmountTrend).map(month => {
    // 所有年份时保留年月，避免不同年份的月份重叠
    return year === 'all' ? month : `${parseInt(month.split('-')[1])}月`
  })
  const data = Object.values(completedAmountTrend)
  
  createChart('maintenanceTrend', maintenanceTrendChart.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '完成金额(万元)',
        data: data,
        borderColor: '#9966FF',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        tension: 0.1,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  })
}

// 周日志数量（近12周）柱状图
const drawWeekLogChart = (labels, values) => {
  if (!weekLogChart.value) return
  createChart('weekLog', weekLogChart.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: '日志数量',
        data: values,
        backgroundColor: '#A8E6CF',
        borderColor: '#7DD3C0',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  })
}

// 月日志数量（近12个月）柱状图
const drawMonthLogChart = (labels, values) => {
  if (!monthLogChart.value) return
  createChart('monthLog', monthLogChart.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: '日志数量',
        data: values,
        backgroundColor: '#7EC8E3',
        borderColor: '#6BB8D3',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
    }
  })
}

// 获取日志数量趋势（interval: week|month，year 为年份或 'all'）
const fetchLogStat = async (interval, year) => {
  try {
    const yearParam = year && year !== 'all' ? `&year=${year}` : ''
    const resp = await fetch(`/api/projects/log-statistics?interval=${interval}&size=12${yearParam}`)
    if (resp.ok) {
      const data = await resp.json()
      if (data && Array.isArray(data.labels) && Array.isArray(data.values)) {
        return data
      }
    }
  } catch (e) {
    console.error(`获取${interval}日志统计失败:`, e)
  }
  return null
}

// 按当前所选年份渲染全部图表与表格
const renderStatistics = async () => {
  const year = selectedYear.value
  const projectData = filteredProjects.value

  // 计算统计数据
  const provinceCount = calculateProvinceCountDistribution(projectData)
  const provinceAmount = calculateProvinceAmountDistribution(projectData)
  const stageCount = calculateStageCount(projectData)
  const monthlyTrend = calculateMonthlyTrend(projectData, year)
  const scaleDistribution = calculateScaleDistribution(projectData)
  const completedAmountTrend = calculateCompletedAmountTrend(projectData, year)

  // 更新表格数据
  salesStatistics.value = calculateSalesStatistics(projectData)
  stageStatistics.value = calculateStageStatistics(projectData)

  // 绘制图表
  drawProvinceCountChart(provinceCount)
  drawProvinceAmountChart(provinceAmount)
  drawStageCountChart(stageCount)
  drawMonthlyTrendChart(monthlyTrend)
  drawScaleDistributionChart(scaleDistribution)
  drawMaintenanceTrendChart(completedAmountTrend, year)

  // 周/月日志数量统计图（同样按年份过滤）
  const weekStat = await fetchLogStat('week', year)
  if (weekStat) drawWeekLogChart(weekStat.labels, weekStat.values)
  const monthStat = await fetchLogStat('month', year)
  if (monthStat) drawMonthLogChart(monthStat.labels, monthStat.values)
}

// 初始化
onMounted(async () => {
  await fetchProjects()
  await renderStatistics()
})

// 切换年份时重新统计
watch(selectedYear, () => {
  renderStatistics()
})

onBeforeUnmount(() => {
  destroyAllCharts()
})
</script>

<style scoped>
/* 统计分析页面 - 马卡龙风格 */
.statistics {
  padding: 0;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
}

.statistics h3 {
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
  margin-bottom: 0;
}

.statistics-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.year-filter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.year-filter-label {
  font-size: 13px;
  font-weight: 600;
  color: #8B8798;
}

.year-select {
  min-width: 120px;
  padding: 8px 14px;
  font-size: 14px;
  color: #5D5A6D;
  background: white;
  border: 1px solid #F0E6E3;
  border-radius: 12px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.year-select:hover {
  border-color: #A8E6CF;
}

.year-select:focus {
  border-color: #7DD3C0;
  box-shadow: 0 0 0 3px rgba(168, 230, 207, 0.25);
}

.filter-count {
  font-size: 13px;
  color: #8B8798;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 28px;
}

.chart-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.chart-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.chart-card:nth-child(1)::before {
  background: linear-gradient(90deg, #A8E6CF, #7DD3C0);
}

.chart-card:nth-child(2)::before {
  background: linear-gradient(90deg, #FF9A8B, #FFB7B2);
}

.chart-card:nth-child(3)::before {
  background: linear-gradient(90deg, #7EC8E3, #6BB8D3);
}

.chart-card:nth-child(4)::before {
  background: linear-gradient(90deg, #C3B1E1, #B19FD0);
}

.chart-card:nth-child(5)::before {
  background: linear-gradient(90deg, #FFEAA7, #FDCB6E);
}

.chart-card:nth-child(6)::before {
  background: linear-gradient(90deg, #D4C4F0, #C3B1E1);
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

.chart-card h4 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  text-align: left;
}

.chart {
  height: 380px;
}

.tables-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.table-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  position: relative;
  overflow: hidden;
}

.table-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #A8E6CF, #C3B1E1);
}

.table-card h4 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  text-align: left;
}

.table-responsive {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #F0E6E3;
}

.table {
  width: 100%;
  margin-bottom: 0;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #F0E6E3;
}

.table th {
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.15), rgba(195, 177, 225, 0.1));
  font-weight: 600;
  color: #5D5A6D;
  font-size: 13px;
}

.table td {
  color: #5D5A6D;
  font-size: 13px;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(168, 230, 207, 0.05);
}

.table-striped tbody tr:hover {
  background-color: rgba(168, 230, 207, 0.1);
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .charts-container,
  .tables-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .chart {
    height: 300px;
  }

  .charts-container,
  .tables-container {
    gap: 14px;
    margin-bottom: 16px;
  }

  .chart-card,
  .table-card {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .statistics h3 {
    font-size: 20px;
  }

  .statistics-header {
    margin-bottom: 16px;
  }

  .year-filter {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .chart {
    height: 240px;
  }

  .chart-card h4,
  .table-card h4 {
    font-size: 14px;
    margin-bottom: 12px;
  }

  .table-responsive {
    border-radius: 8px;
  }
}
</style>
<template>
  <div class="statistics">
    <h3>项目统计分析</h3>
    
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
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import * as echarts from 'echarts'

// 图表引用
const provinceCountChart = ref(null)
const provinceAmountChart = ref(null)
const stageCountChart = ref(null)
const monthlyTrendChart = ref(null)
const scaleDistributionChart = ref(null)
const maintenanceTrendChart = ref(null)

// 数据
const projects = ref([])
const salesStatistics = ref([])
const stageStatistics = ref([])

// 项目阶段映射
const stages = {
  '立项中': [1, 2],
  '已立项': [3, 4, 5],
  '招投标': [6, 7, 8],
  '已中标': [9, 10, 11],
  '已完成': [12, 13]
}

// 从API获取项目数据
const fetchProjects = async () => {
  try {
    const response = await fetch('/api/projects/')
    const data = await response.json()
    projects.value = data
    return data
  } catch (error) {
    console.error('获取项目数据失败:', error)
    return []
  }
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

// 计算月度新增项目趋势
const calculateMonthlyTrend = (projectData) => {
  const monthlyTrend = {}
  
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
      
      // 判断项目是否已完成
      if (project.stage) {
        const stageNum = parseInt(project.stage)
        if (stageNum >= 12 && stageNum <= 13) {
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
  
  const ctx = provinceCountChart.value.getContext('2d')
  const labels = Object.keys(provinceCount)
  const data = Object.values(provinceCount)
  
  new Chart(ctx, {
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
  
  const ctx = provinceAmountChart.value.getContext('2d')
  const labels = Object.keys(provinceAmount)
  const data = Object.values(provinceAmount)
  
  new Chart(ctx, {
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
  
  const ctx = stageCountChart.value.getContext('2d')
  const labels = Object.keys(stageCount)
  const data = Object.values(stageCount)
  
  new Chart(ctx, {
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
  
  const ctx = monthlyTrendChart.value.getContext('2d')
  const labels = Object.keys(monthlyTrend)
  const data = Object.values(monthlyTrend)
  
  new Chart(ctx, {
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
  
  const ctx = scaleDistributionChart.value.getContext('2d')
  const labels = Object.keys(scaleDistribution)
  const data = Object.values(scaleDistribution)
  
  new Chart(ctx, {
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

// 计算当年项目完成金额统计（阶段由1-8变为9-13的项目）
const calculateCompletedAmountTrend = (projectData) => {
  const currentYear = new Date().getFullYear()
  const monthlyAmount = {}
  
  // 初始化当年1-12月
  for (let month = 1; month <= 12; month++) {
    monthlyAmount[`${currentYear}-${month.toString().padStart(2, '0')}`] = 0
  }
  
  projectData.forEach(project => {
    if (project.start_date && project.scale) {
      const year = parseInt(project.start_date.substring(0, 4))
      const month = project.start_date.substring(0, 7)
      
      // 只统计当年的数据
      if (year === currentYear) {
        const stageNum = parseInt(project.stage)
        
        // 阶段由1-8变为9-13（即已中标或已完成阶段）
        if (stageNum >= 9 && stageNum <= 13) {
          const amount = parseFloat(project.scale) || 0
          monthlyAmount[month] = (monthlyAmount[month] || 0) + amount
        }
      }
    }
  })
  
  return monthlyAmount
}

// 绘制项目完成金额统计折线图
const drawMaintenanceTrendChart = (completedAmountTrend) => {
  if (!maintenanceTrendChart.value) return
  
  const ctx = maintenanceTrendChart.value.getContext('2d')
  
  const labels = Object.keys(completedAmountTrend).map(month => {
    return `${parseInt(month.split('-')[1])}月`
  })
  const data = Object.values(completedAmountTrend)
  
  new Chart(ctx, {
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

// 初始化
onMounted(async () => {
  // 获取项目数据
  const projectData = await fetchProjects()
  
  // 计算统计数据
  const provinceCount = calculateProvinceCountDistribution(projectData)
  const provinceAmount = calculateProvinceAmountDistribution(projectData)
  const stageCount = calculateStageCount(projectData)
  const monthlyTrend = calculateMonthlyTrend(projectData)
  const scaleDistribution = calculateScaleDistribution(projectData)
  const completedAmountTrend = calculateCompletedAmountTrend(projectData)
  
  // 更新表格数据
  salesStatistics.value = calculateSalesStatistics(projectData)
  stageStatistics.value = calculateStageStatistics(projectData)
  
  // 绘制图表
  drawProvinceCountChart(provinceCount)
  drawProvinceAmountChart(provinceAmount)
  drawStageCountChart(stageCount)
  drawMonthlyTrendChart(monthlyTrend)
  drawScaleDistributionChart(scaleDistribution)
  drawMaintenanceTrendChart(completedAmountTrend)
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
  margin-bottom: 24px;
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
    margin-bottom: 16px;
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
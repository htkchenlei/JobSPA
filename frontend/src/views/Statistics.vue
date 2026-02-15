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
      
      <!-- 后期维护性检验趋势 -->
      <div class="chart-card">
        <h4>后期维护性检验趋势</h4>
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
          beginAtZero: true
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

// 绘制后期维护性检验趋势折线图
const drawMaintenanceTrendChart = () => {
  if (!maintenanceTrendChart.value) return
  
  const ctx = maintenanceTrendChart.value.getContext('2d')
  
  // 模拟数据
  const labels = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const data = [5, 12, 8, 15, 10, 20, 18, 25, 22, 15, 18, 28]
  
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '维护性检验数量',
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
          beginAtZero: true
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
  
  // 更新表格数据
  salesStatistics.value = calculateSalesStatistics(projectData)
  stageStatistics.value = calculateStageStatistics(projectData)
  
  // 绘制图表
  drawProvinceCountChart(provinceCount)
  drawProvinceAmountChart(provinceAmount)
  drawStageCountChart(stageCount)
  drawMonthlyTrendChart(monthlyTrend)
  drawScaleDistributionChart(scaleDistribution)
  drawMaintenanceTrendChart()
})
</script>

<style scoped>
.statistics {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.chart-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  background-color: #f8f9fa;
}

.chart-card h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  text-align: center;
}

.chart {
  height: 400px;
}

.tables-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.table-card {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  background-color: #f8f9fa;
}

.table-card h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  text-align: center;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  width: 100%;
  margin-bottom: 0;
}

.table th,
.table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.table th {
  background-color: #e9ecef;
  font-weight: 600;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, 0.05);
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
}
</style>
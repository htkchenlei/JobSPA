<template>
  <div class="advanced-search">
    <h3>高级查询</h3>
    
    <!-- 搜索表单容器 -->
    <div class="search-form-container">
      <!-- 三种搜索在同一行 -->
      <div class="form-row main-search-row">
        <!-- 关键词搜索 -->
        <div class="search-section col-md-4">
          <h4>关键词搜索</h4>
          <div class="search-form keyword-search">
            <div class="form-row">
              <div class="form-group col-md-12">
                <label>关键词搜索：</label>
                <input 
                  type="text" 
                  class="form-control" 
                  placeholder="请输入一个或多个关键字，用空格分隔" 
                  v-model="keywordSearch.keywords"
                >
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>开始日期：</label>
                <input type="date" class="form-control" v-model="keywordSearch.startDate">
              </div>
              <div class="form-group col-md-6">
                <label>结束日期：</label>
                <input type="date" class="form-control" v-model="keywordSearch.endDate">
              </div>
            </div>
            <div class="form-actions">
              <button class="btn btn-primary" @click="performKeywordSearch">关键词搜索</button>
            </div>
          </div>
        </div>
        
        <!-- 条件搜索 -->
        <div class="search-section col-md-4">
          <h4>条件搜索</h4>
          <div class="search-form condition-search">
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>项目负责人：</label>
                <select class="form-control" v-model="conditionSearch.owner">
                  <option v-for="owner in owners" :key="owner" :value="owner === '所有负责人' ? '' : owner">{{ owner }}</option>
                </select>
              </div>
              <div class="form-group col-md-6">
                <label>销售人员：</label>
                <select class="form-control" v-model="conditionSearch.salesPerson">
                  <option v-for="sales in salesPersons" :key="sales" :value="sales === '所有销售人员' ? '' : sales">{{ sales }}</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>项目阶段：</label>
                <select class="form-control" v-model="conditionSearch.stage">
                  <option value="">所有阶段</option>
                  <option v-for="stage in Object.keys(stages)" :key="stage" :value="stage">{{ stage }}</option>
                </select>
              </div>
              <div class="form-group col-md-6">
                <label>金额范围（万元）：</label>
                <select class="form-control" v-model="conditionSearch.amountRange">
                  <option value="">所有金额</option>
                  <option value="0-100">0-100</option>
                  <option value="100-500">100-500</option>
                  <option value="500-1000">500-1000</option>
                  <option value="1000+">1000+</option>
                </select>
              </div>
            </div>
            <div class="form-actions">
              <button class="btn btn-primary" @click="performConditionSearch">条件搜索</button>
            </div>
          </div>
        </div>
        
        <!-- 地理位置搜索 -->
        <div class="search-section col-md-4">
          <h4>按地理位置搜索</h4>
          <div class="search-form location-search">
            <div class="form-row">
              <div class="form-group col-md-12">
                <label>省份：</label>
                <select class="form-control" v-model="locationSearch.province" @change="onProvinceChange">
                  <option value="">全部省份</option>
                  <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>城市：</label>
                <select class="form-control" v-model="locationSearch.city" @change="onCityChange">
                  <option value="">全部城市</option>
                  <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
                </select>
              </div>
              <div class="form-group col-md-6">
                <label>行政区：</label>
                <select class="form-control" v-model="locationSearch.district">
                  <option value="">全部区域</option>
                  <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
                </select>
              </div>
            </div>
            <div class="form-actions">
              <button class="btn btn-primary" @click="performLocationSearch">地理位置搜索</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 搜索结果 -->
    <div class="search-section">
      <h4>搜索结果（共{{ searchResults.length }}条）</h4>
      <div class="search-results">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>序号</th>
              <th>项目名称</th>
              <th>金额</th>
              <th>项目阶段</th>
              <th>销售人员</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(result, index) in searchResults" :key="result.id">
              <td>{{ index + 1 }}</td>
              <td>{{ result.name }}</td>
              <td>{{ result.scale || '0' }}</td>
              <td>{{ result.stage_text }}</td>
              <td>{{ result.sales_person || '未知' }}</td>
              <td>
                <button class="btn btn-sm btn-info" @click="viewDetails(result.id)">详情</button>
              </td>
            </tr>
            <tr v-if="searchResults.length === 0">
              <td colspan="6" class="text-center">暂无搜索结果</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 关键词搜索表单数据
const keywordSearch = ref({
  keywords: '',
  startDate: '',
  endDate: ''
})

// 设置默认日期范围为近一年
const setDefaultDateRange = () => {
  const today = new Date()
  const oneYearAgo = new Date()
  oneYearAgo.setFullYear(today.getFullYear() - 1)
  
  keywordSearch.value.endDate = today.toISOString().split('T')[0]
  keywordSearch.value.startDate = oneYearAgo.toISOString().split('T')[0]
}

// 条件搜索表单数据
const conditionSearch = ref({
  owner: '',
  salesPerson: '',
  stage: '',
  amountRange: ''
})

// 地理位置搜索表单数据
const locationSearch = ref({
  province: '',
  city: '',
  district: ''
})

// 搜索结果
const searchResults = ref([])

// 数据
const provinces = ref([])
const cities = ref([])
const districts = ref([])
const owners = ref(['所有负责人'])
const salesPersons = ref(['所有销售人员'])
// 项目阶段映射
const stages = {
  '立项中': [1, 2],
  '已立项': [3, 4, 5],
  '招投标': [6, 7, 8],
  '已中标': [9, 10, 11],
  '已完成': [12, 13]
}

// 从API获取用户列表（用于项目负责人下拉框）
const fetchUsers = async () => {
  try {
    // 首先从项目列表API获取所有项目
    const projectsResponse = await fetch('/api/projects/')
    const projects = await projectsResponse.json()
    
    // 提取所有负责人的ID并去重
    const ownerIdSet = new Set()
    
    projects.forEach(project => {
      if (project.owner) {
        ownerIdSet.add(project.owner)
      }
    })
    
    // 获取所有用户信息
    const usersResponse = await fetch('/api/users/')
    const users = await usersResponse.json()
    
    // 创建用户ID到用户名的映射
    const userIdToNameMap = {}
    users.forEach(user => {
      userIdToNameMap[user.id] = user.username
    })
    
    // 构建负责人列表，只包含在项目中出现过的负责人
    const ownerNames = []
    ownerIdSet.forEach(ownerId => {
      if (userIdToNameMap[ownerId]) {
        ownerNames.push(userIdToNameMap[ownerId])
      }
    })
    
    // 更新owners数组
    owners.value = ['所有负责人', ...ownerNames]
  } catch (error) {
    console.error('获取负责人名单失败:', error)
    // 失败时使用默认值
    owners.value = ['所有负责人', '张三', '李四', '王五']
  }
}

// 从API获取负责人和销售人员名单
const fetchOwnersAndSales = async () => {
  try {
    // 从项目列表API获取所有项目
    const response = await fetch('/api/projects/')
    const projectData = await response.json()
    
    // 存储项目数据
    projects.value = projectData
    
    // 提取所有销售人员的名字
    const salesSet = new Set()
    
    // 提取所有省份并去重
    const provinceSet = new Set()
    
    projectData.forEach(project => {
      if (project.sales_person && project.sales_person !== '所有销售人员') {
        salesSet.add(project.sales_person)
      }
      if (project.province) {
        provinceSet.add(project.province)
      }
    })
    
    // 更新salesPersons数组
    salesPersons.value = ['所有销售人员', ...Array.from(salesSet)]
    
    // 更新provinces数组
    provinces.value = Array.from(provinceSet)
  } catch (error) {
    console.error('获取销售人员名单失败:', error)
    // 失败时使用默认值
    salesPersons.value = ['所有销售人员', '刘巧', '王明', '张伟', '李娜']
    // 失败时使用默认省份
    provinces.value = ['北京市', '上海市', '广东省']
  }
}

// 从API获取的项目数据
const projects = ref([])

// 关键词搜索
const performKeywordSearch = async () => {
  const keywords = keywordSearch.value.keywords
  const startDate = keywordSearch.value.startDate
  const endDate = keywordSearch.value.endDate
  
  try {
    // 发送API请求到后端进行关键词搜索
    const response = await fetch('/api/projects/search/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        keywords: keywords,
        start_date: startDate,
        end_date: endDate
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      // 转换后端返回的数据格式为前端需要的格式
      searchResults.value = data.map(project => ({
        id: project.id,
        name: project.name,
        amount: project.scale || '0',
        stage: project.stage_text,
        salesPerson: project.sales_person || '未知'
      }))
    } else {
      console.error('关键词搜索失败:', response.statusText)
      // 失败时显示所有项目
      searchResults.value = projects.value
    }
  } catch (error) {
    console.error('关键词搜索错误:', error)
    // 错误时显示所有项目
    searchResults.value = projects.value
  }
}

// 条件搜索
const performConditionSearch = () => {
  const owner = conditionSearch.value.owner
  const salesPerson = conditionSearch.value.salesPerson
  const stage = conditionSearch.value.stage
  const amountRange = conditionSearch.value.amountRange
  
  // 使用从API获取的实际项目数据
  const results = projects.value.filter(project => {
    // 负责人匹配
    const matchesOwner = !owner || project.owner_username === owner
    
    // 销售人员匹配
    const matchesSalesPerson = !salesPerson || project.sales_person === salesPerson
    
    // 项目阶段匹配
    let matchesStage = !stage
    if (stage && stages[stage]) {
      // API返回的stage是数字
      matchesStage = stages[stage].includes(parseInt(project.stage))
    }
    
    // 金额范围匹配
    const matchesAmount = !amountRange || {
      '0-100': parseFloat(project.scale || '0') <= 100,
      '100-500': parseFloat(project.scale || '0') > 100 && parseFloat(project.scale || '0') <= 500,
      '500-1000': parseFloat(project.scale || '0') > 500 && parseFloat(project.scale || '0') <= 1000,
      '1000+': parseFloat(project.scale || '0') > 1000
    }[amountRange]
    
    return matchesOwner && matchesSalesPerson && matchesStage && matchesAmount
  })
  
  searchResults.value = results
}

// 地理位置搜索
const performLocationSearch = () => {
  const province = locationSearch.value.province
  const city = locationSearch.value.city
  const district = locationSearch.value.district
  
  // 使用从API获取的实际项目数据
  const results = projects.value.filter(project => {
    // 省份匹配
    const matchesProvince = !province || project.province === province
    
    // 城市匹配
    const matchesCity = !city || project.city === city
    
    // 行政区匹配
    const matchesDistrict = !district || project.district === district
    
    return matchesProvince && matchesCity && matchesDistrict
  })
  
  searchResults.value = results
}

// 查看详情
const viewDetails = (projectId) => {
  console.log('查看项目详情:', projectId)
  // 实际应该跳转到项目详情页面或打开详情模态框
}

// 省份选择变化时更新城市下拉框
const onProvinceChange = () => {
  const selectedProvince = locationSearch.value.province
  
  // 清空城市和区/县选择
  locationSearch.value.city = ''
  locationSearch.value.district = ''
  
  // 清空城市和区/县下拉框
  cities.value = []
  districts.value = []
  
  if (selectedProvince) {
    // 从项目数据中过滤出该省份的所有城市并去重
    const citySet = new Set()
    
    projects.value.forEach(project => {
      if (project.province === selectedProvince && project.city) {
        citySet.add(project.city)
      }
    })
    
    // 更新城市下拉框
    cities.value = Array.from(citySet)
  }
}

// 城市选择变化时更新区/县下拉框
const onCityChange = () => {
  const selectedProvince = locationSearch.value.province
  const selectedCity = locationSearch.value.city
  
  // 清空区/县选择
  locationSearch.value.district = ''
  
  // 清空区/县下拉框
  districts.value = []
  
  if (selectedProvince && selectedCity) {
    // 从项目数据中过滤出该省份和城市的所有区/县并去重
    const districtSet = new Set()
    
    projects.value.forEach(project => {
      if (project.province === selectedProvince && project.city === selectedCity && project.district) {
        districtSet.add(project.district)
      }
    })
    
    // 更新区/县下拉框
    districts.value = Array.from(districtSet)
  }
}

// 初始化
onMounted(async () => {
  // 从数据库获取用户列表（用于项目负责人下拉框）
  await fetchUsers()
  
  // 从数据库获取销售人员名单和项目数据
  await fetchOwnersAndSales()
  
  // 初始化时显示所有项目
  searchResults.value = projects.value
  
  // 设置默认日期范围为近一年
  setDefaultDateRange()
})
</script>

<style scoped>
.advanced-search {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-form-container {
  margin-bottom: 30px;
  width: 100%;
  max-width: 1400px;
}

.main-search-row {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: nowrap;
}

.search-section {
  flex: 1;
  min-width: 300px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 0;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .main-search-row {
    flex-wrap: wrap;
  }
  
  .search-section {
    flex: 1 1 30%;
    min-width: 300px;
  }
}

@media (max-width: 992px) {
  .search-section {
    flex: 1 1 45%;
  }
}

@media (max-width: 768px) {
  .search-section {
    flex: 1 1 100%;
  }
}

.search-section h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.search-form {
  max-width: 100%;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 14px;
  color: #666;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.btn {
  padding: 10px 25px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
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

/* 搜索结果样式 */
.search-results {
  margin-top: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table th,
.table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f8f9fa;
}

.table-striped tbody tr:hover {
  background-color: #e3f2fd;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
}

.btn-info {
  background-color: #1abc9c;
  color: white;
  box-shadow: 0 2px 4px rgba(26, 188, 156, 0.3);
}

.btn-info:hover {
  background-color: #16a085;
  box-shadow: 0 4px 8px rgba(26, 188, 156, 0.4);
}

/* 响应式布局 */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
  
  .form-group {
    width: 100%;
  }
}
</style>
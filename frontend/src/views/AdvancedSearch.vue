<template>
  <div class="advanced-search">
    <h3 class="page-title">高级查询</h3>

    <!-- 搜索表单容器：三种搜索并排 -->
    <div class="search-form-container">
      <div class="main-search-row">
        <!-- 关键词搜索 -->
        <n-card class="search-section" title="关键词搜索" size="small" :bordered="false">
          <n-form :model="keywordSearch" label-placement="top" class="search-form">
            <n-form-item label="关键词搜索">
              <n-input
                v-model:value="keywordSearch.keywords"
                placeholder="请输入一个或多个关键字，用空格分隔"
                clearable
              />
            </n-form-item>
            <div class="two-col">
              <n-form-item label="开始日期">
                <n-date-picker
                  v-model:formatted-value="keywordSearch.startDate"
                  value-format="yyyy-MM-dd"
                  type="date"
                  placeholder="选择开始日期"
                />
              </n-form-item>
              <n-form-item label="结束日期">
                <n-date-picker
                  v-model:formatted-value="keywordSearch.endDate"
                  value-format="yyyy-MM-dd"
                  type="date"
                  placeholder="选择结束日期"
                />
              </n-form-item>
            </div>
          </n-form>
          <div class="form-actions">
            <n-button class="mc-btn-coral" :loading="searching" @click="performKeywordSearch">关键词搜索</n-button>
          </div>
        </n-card>

        <!-- 条件搜索 -->
        <n-card class="search-section" title="条件搜索" size="small" :bordered="false">
          <n-form :model="conditionSearch" label-placement="top" class="search-form">
            <div class="two-col">
              <n-form-item label="项目负责人">
                <n-select
                  v-model:value="conditionSearch.owner"
                  :options="ownerOptions"
                  placeholder="所有负责人"
                />
              </n-form-item>
              <n-form-item label="销售人员">
                <n-select
                  v-model:value="conditionSearch.salesPerson"
                  :options="salesOptions"
                  placeholder="所有销售人员"
                />
              </n-form-item>
            </div>
            <div class="two-col">
              <n-form-item label="项目阶段">
                <n-select
                  v-model:value="conditionSearch.stage"
                  :options="stageOptions"
                  placeholder="所有阶段"
                />
              </n-form-item>
              <n-form-item label="金额范围（万元）">
                <n-select
                  v-model:value="conditionSearch.amountRange"
                  :options="amountOptions"
                  placeholder="所有金额"
                />
              </n-form-item>
            </div>
          </n-form>
          <div class="form-actions">
            <n-button class="mc-btn-coral" @click="performConditionSearch">条件搜索</n-button>
          </div>
        </n-card>

        <!-- 地理位置搜索 -->
        <n-card class="search-section" title="按地理位置搜索" size="small" :bordered="false">
          <n-form :model="locationSearch" label-placement="top" class="search-form">
            <n-form-item label="省份">
              <n-select
                v-model:value="locationSearch.province"
                :options="provinceOptions"
                placeholder="全部省份"
                @update:value="onProvinceChange"
              />
            </n-form-item>
            <div class="two-col">
              <n-form-item label="城市">
                <n-select
                  v-model:value="locationSearch.city"
                  :options="cityOptions"
                  placeholder="全部城市"
                  @update:value="onCityChange"
                />
              </n-form-item>
              <n-form-item label="行政区">
                <n-select
                  v-model:value="locationSearch.district"
                  :options="districtOptions"
                  placeholder="全部区域"
                />
              </n-form-item>
            </div>
          </n-form>
          <div class="form-actions">
            <n-button class="mc-btn-coral" @click="performLocationSearch">地理位置搜索</n-button>
          </div>
        </n-card>
      </div>
    </div>

    <!-- 搜索结果 -->
    <n-card class="result-card" :bordered="false">
      <template #header>
        <span class="result-title">搜索结果（共 {{ searchResults.length }} 条）</span>
      </template>
      <n-data-table
        v-if="searchResults.length > 0"
        :columns="resultColumns"
        :data="searchResults"
        :bordered="false"
        :single-line="false"
        size="small"
        :scroll-x="720"
      />
      <n-empty v-else description="暂无搜索结果" size="large" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, h, computed, onMounted } from 'vue'
import {
  NCard, NForm, NFormItem, NInput, NSelect, NDatePicker,
  NDataTable, NButton, NEmpty, NTag
} from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { getStageMeta } from '../constants/stageColors'

interface ProjectLike {
  id: string | number
  name: string
  scale?: string
  stage?: string | number
  stage_text?: string
  sales_person?: string
  owner?: string | number
  owner_username?: string
  province?: string
  city?: string
  district?: string
  [key: string]: unknown
}

// 关键词搜索表单数据
// 注意：n-date-picker 的需用 null 表示"未选择"，传 '' 会在内部
// formatDate('') 时抛 RangeError: Invalid time value 导致整页白屏
const keywordSearch = ref<{
  keywords: string
  startDate: string | null
  endDate: string | null
}>({
  keywords: '',
  startDate: null,
  endDate: null
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
const searchResults = ref<ProjectLike[]>([])
const searching = ref(false)

// 数据
const provinces = ref<string[]>([])
const cities = ref<string[]>([])
const districts = ref<string[]>([])
const owners = ref(['所有负责人'])
const salesPersons = ref(['所有销售人员'])
// 项目阶段映射（统一 5 档）
const stages: Record<string, number[]> = {
  '立项中': [1],
  '已立项': [2],
  '招投标': [3],
  '已中标': [4],
  '已完成': [5]
}

// ---- n-select 选项（派生，不改变任何筛选行为） ----
const ownerOptions = computed(() =>
  owners.value.map((o) => ({ label: o, value: o === '所有负责人' ? '' : o }))
)
const salesOptions = computed(() =>
  salesPersons.value.map((s) => ({ label: s, value: s === '所有销售人员' ? '' : s }))
)
const stageOptions = [
  { label: '所有阶段', value: '' },
  ...Object.keys(stages).map((s) => ({ label: s, value: s }))
]
const amountOptions = [
  { label: '所有金额', value: '' },
  { label: '0-100', value: '0-100' },
  { label: '100-500', value: '100-500' },
  { label: '500-1000', value: '500-1000' },
  { label: '1000+', value: '1000+' }
]
const provinceOptions = computed(() => [
  { label: '全部省份', value: '' },
  ...provinces.value.map((p) => ({ label: p, value: p }))
])
const cityOptions = computed(() => [
  { label: '全部城市', value: '' },
  ...cities.value.map((c) => ({ label: c, value: c }))
])
const districtOptions = computed(() => [
  { label: '全部区域', value: '' },
  ...districts.value.map((d) => ({ label: d, value: d }))
])

// 结果表格列
const resultColumns: DataTableColumns<ProjectLike> = [
  {
    title: '序号',
    key: 'index',
    width: 70,
    render: (_row, index) => index + 1
  },
  {
    title: '项目名称',
    key: 'name',
    minWidth: 180,
    ellipsis: { tooltip: true }
  },
  {
    title: '金额',
    key: 'scale',
    width: 110,
    render: (row) => row.scale || '0'
  },
  {
    title: '项目阶段',
    key: 'stage_text',
    width: 120,
    render: (row) => {
      const meta = getStageMeta(row.stage)
      return h(
        NTag,
        { class: ['mc-stage-tag', meta.className], bordered: false, size: 'small', round: true },
        { default: () => row.stage_text || meta.label }
      )
    }
  },
  {
    title: '销售人员',
    key: 'sales_person',
    width: 120,
    render: (row) => row.sales_person || '未知'
  },
  {
    title: '操作',
    key: 'actions',
    width: 90,
    render: (row) =>
      h(
        NButton,
        { class: 'mc-btn-sky', size: 'small', onClick: () => viewDetails(row.id) },
        { default: () => '详情' }
      )
  }
]

// 从API获取用户列表（用于项目负责人下拉框）
const fetchUsers = async () => {
  try {
    // 首先从项目列表API获取所有项目
    const projectsResponse = await fetch('/api/projects/')
    const projectList: ProjectLike[] = await projectsResponse.json()

    // 提取所有负责人的ID并去重
    const ownerIdSet = new Set<string | number>()

    projectList.forEach((project) => {
      if (project.owner) {
        ownerIdSet.add(project.owner)
      }
    })

    // 获取所有用户信息
    const usersResponse = await fetch('/api/users/')
    const users = await usersResponse.json()

    // 创建用户ID到用户名的映射
    const userIdToNameMap: Record<string, string> = {}
    users.forEach((user: { id: string | number; username: string }) => {
      userIdToNameMap[String(user.id)] = user.username
    })

    // 构建负责人列表，只包含在项目中出现过的负责人
    const ownerNames: string[] = []
    ownerIdSet.forEach((ownerId) => {
      const name = userIdToNameMap[String(ownerId)]
      if (name) {
        ownerNames.push(name)
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
    const projectData: ProjectLike[] = await response.json()

    // 存储项目数据
    projects.value = projectData

    // 提取所有销售人员的名字
    const salesSet = new Set<string>()

    // 提取所有省份并去重
    const provinceSet = new Set<string>()

    projectData.forEach((project) => {
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
const projects = ref<ProjectLike[]>([])

// 关键词搜索
const performKeywordSearch = async () => {
  const keywords = keywordSearch.value.keywords
  const startDate = keywordSearch.value.startDate
  const endDate = keywordSearch.value.endDate

  searching.value = true
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
      searchResults.value = data.map((project: ProjectLike) => ({
        id: project.id,
        name: project.name,
        scale: project.scale || '0',
        stage: project.stage,
        stage_text: project.stage_text,
        sales_person: project.sales_person || '未知'
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
  } finally {
    searching.value = false
  }
}

// 条件搜索
const performConditionSearch = () => {
  const owner = conditionSearch.value.owner
  const salesPerson = conditionSearch.value.salesPerson
  const stage = conditionSearch.value.stage
  const amountRange = conditionSearch.value.amountRange

  // 使用从API获取的实际项目数据
  const results = projects.value.filter((project) => {
    // 负责人匹配
    const matchesOwner = !owner || project.owner_username === owner

    // 销售人员匹配
    const matchesSalesPerson = !salesPerson || project.sales_person === salesPerson

    // 项目阶段匹配
    let matchesStage = !stage
    if (stage && stages[stage]) {
      // API返回的stage是数字
      matchesStage = stages[stage].includes(parseInt(String(project.stage)))
    }

    // 金额范围匹配
    const scale = parseFloat(String(project.scale || '0'))
    const matchesAmount = !amountRange || {
      '0-100': scale <= 100,
      '100-500': scale > 100 && scale <= 500,
      '500-1000': scale > 500 && scale <= 1000,
      '1000+': scale > 1000
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
  const results = projects.value.filter((project) => {
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
const viewDetails = (projectId: string | number) => {
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
    const citySet = new Set<string>()

    projects.value.forEach((project) => {
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
    const districtSet = new Set<string>()

    projects.value.forEach((project) => {
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
  padding: 0;
  background: transparent;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
  margin: 0 0 24px;
}

.search-form-container {
  margin-bottom: 24px;
  width: 100%;
}

.main-search-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.search-section {
  background: rgba(255, 255, 255, 0.86);
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border-top: 4px solid #A8E6CF;
}

.search-section:nth-child(2) {
  border-top-color: #FF9A8B;
}

.search-section:nth-child(3) {
  border-top-color: #7EC8E3;
}

.search-section :deep(.n-card-header__main) {
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
}

.two-col {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 12px;
}

.search-form :deep(.n-input),
.search-form :deep(.n-date-picker),
.search-form :deep(.n-select) {
  width: 100%;
}

.form-actions {
  margin-top: 4px;
  display: flex;
  justify-content: center;
}

.result-card {
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  background: rgba(255, 255, 255, 0.86);
  border-top: 4px solid #FFEAA7;
}

.result-title {
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
}

.result-card :deep(.n-data-table-th) {
  background: #FBF7F4;
  font-weight: 600;
  color: #5D5A6D;
}

@media (max-width: 1200px) {
  .main-search-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 20px;
    margin-bottom: 16px;
  }

  .two-col {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>

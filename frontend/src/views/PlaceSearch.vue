<template>
  <div class="place-search">
    <h1 class="page-title">文档关键词检查工具</h1>

    <n-tabs v-model:value="activeTab" type="line" animated class="place-tabs">
      <n-tab-pane name="document" tab="文档检查">
        <!-- 文件上传和关键词添加区域 -->
        <section class="upload-keywords-container">
          <n-card class="search-card" title="文件上传" :bordered="false">
            <div
              class="upload-area"
              :class="{ 'is-dragover': isDragover }"
              @dragover.prevent="isDragover = true"
              @dragleave.prevent="isDragover = false"
              @drop.prevent="handleFileDrop"
            >
              <div class="upload-content">
                <input
                  type="file"
                  ref="fileInput"
                  style="display: none"
                  accept=".doc,.docx,.xls,.xlsx"
                  @change="handleFileSelect"
                >
                <n-button class="mc-btn-coral" @click="triggerFileInput">选择文件</n-button>
                <p>或拖动文件到此处</p>
                <p class="allowed-types">支持的文件类型：.doc, .docx, .xls, .xlsx</p>
                <p class="allowed-count">一次只能上传一个文件</p>
              </div>
            </div>

            <div v-if="selectedFile" class="file-list">
              <h3>已选择的文件：</h3>
              <ul>
                <li>
                  {{ selectedFile.name }}
                  <n-button class="mc-btn-danger" size="tiny" @click="removeFile">删除</n-button>
                </li>
              </ul>
            </div>
          </n-card>

          <n-card class="search-card" title="添加关键词" :bordered="false">
            <div class="keyword-input-group">
              <n-input
                v-model:value="newKeyword"
                placeholder="输入新的地名关键词，多个关键词用逗号分隔"
                @keyup.enter="addKeyword"
                @blur="addKeyword"
              />
            </div>
            <div v-if="customKeywords.length > 0" class="keyword-list">
              <h3>自定义关键词：</h3>
              <ul>
                <li v-for="(keyword, index) in customKeywords" :key="index">
                  {{ keyword }}
                  <n-button class="mc-btn-danger" size="tiny" @click="removeKeyword(index)">删除</n-button>
                </li>
              </ul>
            </div>
          </n-card>
        </section>

        <!-- 对比结果区域 -->
        <n-card class="search-card results-section" title="对比结果" :bordered="false">
          <n-button
            class="mc-btn-coral"
            :loading="isProcessing"
            :disabled="!selectedFile || isProcessing"
            @click="compareFiles"
          >
            {{ isProcessing ? '处理中...' : '开始对比' }}
          </n-button>

          <div v-if="isProcessing" class="processing">
            <n-spin size="small" />
            <p>正在处理文件并匹配地名，请稍候...</p>
          </div>

          <div v-else-if="comparisonResults.length > 0" class="results-list">
            <div v-for="(result, index) in comparisonResults" :key="index">
              <h3>{{ result.fileName }} - 找到 {{ result.matches.length }} 个匹配的地名</h3>
              <div v-if="result.matches.length > 0" class="matches-grid">
                <div v-for="(match, matchIndex) in result.matches" :key="matchIndex" class="result-item">
                  <div class="match-location">{{ match.location }}</div>
                  <div class="match-text" v-html="highlightKeywords(match.text, [match.place])"></div>
                  <div class="match-place">
                    匹配地名：<strong>{{ match.place }}</strong>
                  </div>
                </div>
              </div>
              <n-empty v-else description="未找到匹配的地名" size="small" />
            </div>
          </div>

          <div v-else-if="selectedFile" class="no-results">
            <p>请点击"开始对比"按钮查看结果</p>
          </div>
        </n-card>
      </n-tab-pane>

      <n-tab-pane name="admin" tab="行政区划管理">
        <!-- 省级行政区 -->
        <n-card class="search-card region-section" :bordered="false">
          <template #header><span class="section-title">省级行政区</span></template>
          <div class="region-tags">
            <n-popconfirm
              v-for="(province, index) in placesJson.provinces"
              :key="index"
              positive-text="删除"
              negative-text="取消"
              @positive-click="deletePlaceAt('省级', index)"
            >
              <template #trigger>
                <n-tag class="region-tag" :bordered="false" round>
                  {{ typeof province === 'string' ? province : province.name }}
                  <span class="delete-icon">×</span>
                </n-tag>
              </template>
              确定要删除 {{ typeof province === 'string' ? province : province.name }} 吗？
            </n-popconfirm>
          </div>
        </n-card>

        <!-- 市级行政区 -->
        <n-card class="search-card region-section" :bordered="false">
          <template #header>
            <div class="section-header">
              <span class="section-title">市级行政区</span>
              <n-button class="mc-btn-mint" size="small" @click="showAddCityDialog = true">新增</n-button>
            </div>
          </template>
          <div class="region-tags">
            <n-popconfirm
              v-for="(city, index) in placesJson.cities"
              :key="index"
              positive-text="删除"
              negative-text="取消"
              @positive-click="deletePlaceAt('市级', index)"
            >
              <template #trigger>
                <n-tag class="region-tag" :bordered="false" round>
                  {{ city }}
                  <span class="delete-icon">×</span>
                </n-tag>
              </template>
              确定要删除 {{ city }} 吗？
            </n-popconfirm>
          </div>
        </n-card>

        <!-- 区级行政区 -->
        <n-card class="search-card region-section" :bordered="false">
          <template #header>
            <div class="section-header">
              <span class="section-title">区级行政区</span>
              <n-button class="mc-btn-mint" size="small" @click="showAddDistrictDialog = true">新增</n-button>
            </div>
          </template>
          <div class="region-tags">
            <n-popconfirm
              v-for="(district, index) in placesJson.districts"
              :key="index"
              positive-text="删除"
              negative-text="取消"
              @positive-click="deletePlaceAt('区级', index)"
            >
              <template #trigger>
                <n-tag class="region-tag" :bordered="false" round>
                  {{ district }}
                  <span class="delete-icon">×</span>
                </n-tag>
              </template>
              确定要删除 {{ district }} 吗？
            </n-popconfirm>
          </div>
        </n-card>

        <!-- 新增城市对话框 -->
        <n-modal
          v-model:show="showAddCityDialog"
          preset="card"
          class="mc-modal place-dialog"
          title="新增市级行政区"
          :bordered="false"
          :style="{ width: '400px' }"
        >
          <n-input v-model:value="newCityName" placeholder="请输入城市名称" />
          <template #footer>
            <div class="dialog-buttons">
              <n-button class="mc-btn-lavender" @click="showAddCityDialog = false">取消</n-button>
              <n-button class="mc-btn-coral" @click="addCity">确认</n-button>
            </div>
          </template>
        </n-modal>

        <!-- 新增区对话框 -->
        <n-modal
          v-model:show="showAddDistrictDialog"
          preset="card"
          class="mc-modal place-dialog"
          title="新增区级行政区"
          :bordered="false"
          :style="{ width: '400px' }"
        >
          <n-input v-model:value="newDistrictName" placeholder="请输入区名称" />
          <template #footer>
            <div class="dialog-buttons">
              <n-button class="mc-btn-lavender" @click="showAddDistrictDialog = false">取消</n-button>
              <n-button class="mc-btn-coral" @click="addDistrict">确认</n-button>
            </div>
          </template>
        </n-modal>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  NTabs, NTabPane, NCard, NInput, NButton, NTag, NEmpty, NSpin, NPopconfirm, NModal
} from 'naive-ui'
import { message } from '../utils/feedback'

// 文件相关
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const isDragover = ref(false)

interface Province {
  name: string
  shortName?: string
}

interface PlacesJson {
  provinces: (string | Province)[]
  cities: string[]
  districts: string[]
}

// JSON相关
const placesJson = ref<PlacesJson>({
  provinces: [],
  cities: [],
  districts: []
})

// 关键词相关
const newKeyword = ref('')
const customKeywords = ref<string[]>([])

// 新增区划对话框状态
const showAddCityDialog = ref(false)
const showAddDistrictDialog = ref(false)
const newCityName = ref('')
const newDistrictName = ref('')

// 标签页状态
const activeTab = ref('document')

// 对比结果相关
interface MatchItem {
  location: string
  text: string
  place: string
}

interface ComparisonResult {
  fileName: string
  matches: MatchItem[]
}

const comparisonResults = ref<ComparisonResult[]>([])
const isProcessing = ref(false)

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
  }
}

// 处理文件拖放
const handleFileDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragover.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectedFile.value = event.dataTransfer.files[0]
  }
}

// 移除文件
const removeFile = () => {
  selectedFile.value = null
  comparisonResults.value = []
}

// 从后端API获取地名数据
const fetchPlacesData = async () => {
  try {
    const response = await fetch('/api/places')
    if (response.ok) {
      const data = await response.json()
      if (typeof data === 'object' && data !== null) {
        placesJson.value = {
          provinces: Array.isArray(data.provinces) ? data.provinces : [],
          cities: Array.isArray(data.cities) ? data.cities : [],
          districts: Array.isArray(data.districts) ? data.districts : []
        }
        console.log('获取的地名数据:', placesJson.value)
      } else {
        console.error('获取的地名数据格式错误:', data)
        placesJson.value = { provinces: [], cities: [], districts: [] }
      }
    } else {
      console.error('获取地名数据失败:', response.statusText)
      placesJson.value = { provinces: [], cities: [], districts: [] }
    }
  } catch (error) {
    console.error('获取地名数据时发生错误:', error)
    placesJson.value = { provinces: [], cities: [], districts: [] }
  }
}

// 添加关键词
const addKeyword = () => {
  if (!newKeyword.value.trim()) return

  const keywords = newKeyword.value.split(/[,，]/).map(k => k.trim()).filter(k => k)

  // 汇总已有地名，用于去重
  const existingKeywords = new Set<string>()
  placesJson.value.provinces.forEach((province) => {
    existingKeywords.add(typeof province === 'string' ? province : province.name)
  })
  placesJson.value.cities.forEach((city) => existingKeywords.add(city))
  placesJson.value.districts.forEach((district) => existingKeywords.add(district))
  customKeywords.value.forEach((keyword) => existingKeywords.add(keyword))

  const newKeywords = keywords.filter((keyword) => {
    if (existingKeywords.has(keyword)) return false
    existingKeywords.add(keyword)
    return true
  })

  if (newKeywords.length > 0) {
    customKeywords.value.push(...newKeywords)
    if (newKeywords.length < keywords.length) {
      message.warning('部分关键词已存在，已添加新关键词')
    }
  } else {
    message.warning('所有关键词都已存在')
  }

  newKeyword.value = ''
}

// 移除关键词
const removeKeyword = (index: number) => {
  customKeywords.value.splice(index, 1)
}

// 对比文件
const compareFiles = async () => {
  if (!selectedFile.value) {
    message.warning('请选择要对比的文件')
    return
  }

  isProcessing.value = true
  comparisonResults.value = []

  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    customKeywords.value.forEach((keyword, index) => {
      formData.append(`keywords[${index}]`, keyword)
    })

    const response = await fetch('/api/file-parse', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || '服务器响应错误')
    }

    const data = await response.json()

    if (data.success) {
      comparisonResults.value = [{
        fileName: data.fileName,
        matches: data.matches
      }]
    } else {
      throw new Error(data.message || '处理失败')
    }
  } catch (error) {
    console.error('对比文件时发生错误:', error)
    message.error(`对比文件时发生错误: ${error instanceof Error ? error.message : '未知错误'}`)
  } finally {
    isProcessing.value = false
  }
}

// 高亮显示关键词
const highlightKeywords = (text: string, keywords: string[]) => {
  if (!text || !keywords || keywords.length === 0) {
    return text
  }

  let highlightedText = text
  const sortedKeywords = [...keywords].sort((a, b) => b.length - a.length)

  sortedKeywords.forEach((keyword) => {
    if (keyword && keyword.trim()) {
      const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
      highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>')
    }
  })

  return highlightedText
}

// 在现有数据中查找地名
const searchPlaceInData = (placeName: string) => {
  for (const province of placesJson.value.provinces) {
    if (typeof province !== 'string' && (province.name === placeName || province.shortName === placeName)) {
      return { level: '省级', place: province }
    }
  }
  for (const city of placesJson.value.cities) {
    if (city === placeName) return { level: '市级', place: city }
  }
  for (const district of placesJson.value.districts) {
    if (district === placeName) return { level: '区级', place: district }
  }
  return null
}

// 添加地名
const addPlace = async (placeName: string, level: string) => {
  try {
    if (searchPlaceInData(placeName)) {
      message.warning('该地名已存在')
      return
    }

    if (level === '市级') {
      placesJson.value.cities.push(placeName)
    } else if (level === '区级') {
      placesJson.value.districts.push(placeName)
    }

    const response = await fetch('/api/places/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ place: placeName, level })
    })

    if (!response.ok) {
      throw new Error('添加地名失败')
    }

    message.success('地名添加成功')
  } catch (error) {
    console.error('添加地名时发生错误:', error)
    message.error('添加地名失败，请重试')
  }
}

// 删除地名（由 n-popconfirm 触发，替代原手写确认弹窗）
const deletePlaceAt = async (level: string, index: number) => {
  let placeName = ''
  if (level === '市级') {
    placeName = placesJson.value.cities[index]
  } else if (level === '区级') {
    placeName = placesJson.value.districts[index]
  } else if (level === '省级') {
    const province = placesJson.value.provinces[index]
    placeName = typeof province === 'string' ? province : province.name
  }

  try {
    if (level === '市级') {
      placesJson.value.cities.splice(index, 1)
    } else if (level === '区级') {
      placesJson.value.districts.splice(index, 1)
    } else if (level === '省级') {
      placesJson.value.provinces.splice(index, 1)
    }

    const response = await fetch('/api/places/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ place: placeName, level })
    })

    if (!response.ok) {
      throw new Error('删除地名失败')
    }

    message.success('地名删除成功')
  } catch (error) {
    console.error('删除地名时发生错误:', error)
    message.error('删除地名失败，请重试')
  }
}

// 添加城市
const addCity = async () => {
  if (newCityName.value.trim()) {
    await addPlace(newCityName.value.trim(), '市级')
    newCityName.value = ''
    showAddCityDialog.value = false
  }
}

// 添加区
const addDistrict = async () => {
  if (newDistrictName.value.trim()) {
    await addPlace(newDistrictName.value.trim(), '区级')
    newDistrictName.value = ''
    showAddDistrictDialog.value = false
  }
}

// 组件挂载时获取地名数据
onMounted(() => {
  fetchPlacesData()
})
</script>

<style scoped>
.place-search {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
  text-align: center;
  margin: 0 0 20px;
}

.place-tabs :deep(.n-tabs-tab) {
  font-size: 15px;
  color: #8B8899;
}

.place-tabs :deep(.n-tabs-tab--active) {
  color: #9575C9;
  font-weight: 600;
}

.place-tabs :deep(.n-tabs-bar) {
  background: linear-gradient(90deg, #C3B1E1, #9575C9) !important;
}

/* 上传和关键词容器样式 */
.upload-keywords-container {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.search-card {
  border-radius: 20px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  background: rgba(255, 255, 255, 0.9);
  margin-bottom: 24px;
}

.search-card :deep(.n-card-header__main) {
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
}

/* 内容区留白见全局 style.css（Naive 类名为 .n-card-content） */

.upload-keywords-container .search-card:last-child {
  margin-bottom: 0;
}

/* 上传区域样式 */
.upload-area {
  border: 2px dashed #E9DAD4;
  border-radius: 16px;
  padding: 28px 20px;
  text-align: center;
  transition: all 0.25s ease;
  background: #FFFCFA;
}

.upload-area:hover,
.upload-area.is-dragover {
  border-color: #A8E6CF;
  background: rgba(168, 230, 207, 0.08);
}

.upload-content p {
  margin: 10px 0;
  color: #8B8899;
  font-size: 13px;
}

.allowed-types {
  font-size: 12px !important;
  color: #A8A5B3 !important;
}

.allowed-count {
  font-size: 12px !important;
  color: #8B8899 !important;
  font-weight: 500;
}

/* 处理状态 / 无结果 */
.processing,
.no-results {
  margin-top: 20px;
  padding: 20px;
  background: #FBF7F4;
  border-radius: 14px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.processing p,
.no-results p {
  margin: 0;
  color: #8B8899;
  font-size: 13px;
}

/* 匹配项样式 */
.match-place {
  margin-top: 6px;
  color: #3E93B3;
  font-size: 13px;
}

:deep(.highlight) {
  background-color: #FFEAA7;
  color: #5D5A6D;
  padding: 0 2px;
  border-radius: 3px;
  font-weight: 700;
}

/* 文件列表 / 关键词列表 */
.file-list,
.keyword-list {
  margin-top: 20px;
}

.file-list h3,
.keyword-list h3 {
  font-size: 14px;
  font-weight: 600;
  color: #5D5A6D;
  margin: 0 0 10px;
}

.file-list ul,
.keyword-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.file-list li,
.keyword-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border: 1px solid #F0E6E3;
  border-radius: 12px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #5D5A6D;
  background: #FFFCFA;
}

.keyword-input-group {
  display: flex;
  gap: 10px;
}

.keyword-input-group :deep(.n-input) {
  flex: 1;
}

/* 结果区域样式 */
.results-list {
  margin-top: 20px;
}

.results-list h3 {
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
  margin: 0 0 12px;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.result-item {
  padding: 16px;
  border: 1px solid #F0E6E3;
  border-radius: 14px;
  background: #FFFCFA;
  transition: all 0.25s ease;
}

.result-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}

.match-location {
  font-weight: 700;
  color: #3E93B3;
  margin-bottom: 6px;
  font-size: 13px;
}

.match-text {
  color: #5D5A6D;
  font-size: 13px;
  line-height: 1.7;
}

/* 区域管理样式 */
.region-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.region-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.region-tag {
  cursor: pointer;
  padding: 6px 14px;
  background: #FBF3EF !important;
  color: #5D5A6D !important;
  font-size: 13px;
  transition: all 0.2s ease;
}

.region-tag:hover {
  background: #F5E6DF !important;
}

.region-tag .delete-icon {
  margin-left: 8px;
  color: #FF8A7A;
  font-size: 15px;
  font-weight: 700;
  line-height: 1;
}

.region-tag .delete-icon:hover {
  color: #F2545B;
}

/* 对话框 */
.place-dialog {
  border-radius: 20px;
  border: 1px solid #F0E6E3;
}

:deep(.place-dialog .n-card-header) {
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.12), rgba(255, 154, 139, 0.12));
  padding: 16px 20px;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 20px;
  }

  .upload-keywords-container {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .matches-grid {
    grid-template-columns: 1fr;
  }

}
</style>

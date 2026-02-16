<template>
  <div class="place-search">
    <h1>文档关键词检查工具</h1>
    
    <!-- 标签页切换 -->
    <div class="tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'document' }"
        @click="activeTab = 'document'"
      >
        文档检查
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'admin' }"
        @click="activeTab = 'admin'"
      >
        行政区划管理
      </button>
    </div>
    
    <!-- 文档检查标签页 -->
    <div v-if="activeTab === 'document'" class="tab-content">
      <!-- 文件上传和关键词添加区域 -->
      <section class="upload-keywords-container">
        <div class="upload-section">
          <h2>文件上传</h2>
          <div class="upload-area" @dragover.prevent @drop="handleFileDrop">
            <div class="upload-content">
              <input 
                type="file" 
                ref="fileInput" 
                style="display: none" 
                accept=".doc,.docx,.xls,.xlsx"
                @change="handleFileSelect"
              >
              <button class="btn btn-primary" @click="triggerFileInput">
                选择文件
              </button>
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
                <button class="btn btn-danger btn-sm" @click="removeFile">
                  删除
                </button>
              </li>
            </ul>
          </div>
        </div>
        
        <div class="keywords-section">
          <h2>添加关键词</h2>
          <div class="keyword-input-group">
            <input 
              type="text" 
              v-model="newKeyword" 
              placeholder="输入新的地名关键词，多个关键词用逗号分隔"
              class="form-control"
              @change="addKeyword"
            >
          </div>
          <div v-if="customKeywords.length > 0" class="keyword-list">
            <h3>自定义关键词：</h3>
            <ul>
              <li v-for="(keyword, index) in customKeywords" :key="index">
                {{ keyword }}
                <button class="btn btn-danger btn-sm" @click="removeKeyword(index)">
                  删除
                </button>
              </li>
            </ul>
          </div>
        </div>
      </section>
      
      <!-- 对比结果区域 -->
      <section class="results-section">
        <h2>对比结果</h2>
        <button class="btn btn-primary" @click="compareFiles" :disabled="!selectedFile || isProcessing">
          {{ isProcessing ? '处理中...' : '开始对比' }}
        </button>
        
        <div v-if="isProcessing" class="processing">
          <p>正在处理文件并匹配地名，请稍候...</p>
        </div>
        
        <div v-else-if="comparisonResults.length > 0" class="results-list">
          <div v-for="(result, index) in comparisonResults" :key="index">
            <h3>{{ result.fileName }} - 找到 {{ result.matches.length }} 个匹配的地名</h3>
            <div v-if="result.matches.length > 0" class="matches-grid">
              <div v-for="(match, matchIndex) in result.matches" :key="matchIndex" class="result-item">
                <div class="match-location">
                  {{ match.location }}
                </div>
                <div class="match-text" v-html="highlightKeywords(match.text, [match.place])"></div>
                <div class="match-place">
                  匹配地名：<strong>{{ match.place }}</strong>
                </div>
              </div>
            </div>
            <div v-else class="no-matches">
              <p>未找到匹配的地名</p>
            </div>
          </div>
        </div>
        
        <div v-else-if="selectedFile" class="no-results">
          <p>请点击"开始对比"按钮查看结果</p>
        </div>
      </section>
    </div>
    
    <!-- 行政区划管理标签页 -->
    <div v-if="activeTab === 'admin'" class="tab-content">
      <!-- 省级行政区 -->
      <div class="region-section">
        <div class="section-header">
          <h3>省级行政区</h3>
          <!-- 省级没有新增按钮 -->
        </div>
        <div class="region-tags">
          <div 
            v-for="(province, index) in placesJson.provinces" 
            :key="index"
            class="region-tag"
          >
            <span>{{ typeof province === 'string' ? province : province.name }}</span>
            <span 
              class="delete-icon" 
              @click="confirmDeletePlace('省级', index)"
            >
              ×
            </span>
          </div>
        </div>
      </div>

      <!-- 市级行政区 -->
      <div class="region-section">
        <div class="section-header">
          <h3>市级行政区</h3>
          <button class="add-button" @click="showAddCityDialog = true">新增</button>
        </div>
        <div class="region-tags">
          <div 
            v-for="(city, index) in placesJson.cities" 
            :key="index"
            class="region-tag"
          >
            <span>{{ city }}</span>
            <span 
              class="delete-icon" 
              @click="confirmDeletePlace('市级', index)"
            >
              ×
            </span>
          </div>
        </div>
      </div>

      <!-- 区级行政区 -->
      <div class="region-section">
        <div class="section-header">
          <h3>区级行政区</h3>
          <button class="add-button" @click="showAddDistrictDialog = true">新增</button>
        </div>
        <div class="region-tags">
          <div 
            v-for="(district, index) in placesJson.districts" 
            :key="index"
            class="region-tag"
          >
            <span>{{ district }}</span>
            <span 
              class="delete-icon" 
              @click="confirmDeletePlace('区级', index)"
            >
              ×
            </span>
          </div>
        </div>
      </div>

      <!-- 新增城市对话框 -->
      <div v-if="showAddCityDialog" class="dialog-overlay" @click.self="showAddCityDialog = false">
        <div class="dialog">
          <h3>新增市级行政区</h3>
          <input 
            type="text" 
            v-model="newCityName" 
            placeholder="请输入城市名称"
            class="input-field"
          >
          <div class="dialog-buttons">
            <button class="cancel-button" @click="showAddCityDialog = false">取消</button>
            <button class="confirm-button" @click="addCity">确认</button>
          </div>
        </div>
      </div>

      <!-- 新增区对话框 -->
      <div v-if="showAddDistrictDialog" class="dialog-overlay" @click.self="showAddDistrictDialog = false">
        <div class="dialog">
          <h3>新增区级行政区</h3>
          <input 
            type="text" 
            v-model="newDistrictName" 
            placeholder="请输入区名称"
            class="input-field"
          >
          <div class="dialog-buttons">
            <button class="cancel-button" @click="showAddDistrictDialog = false">取消</button>
            <button class="confirm-button" @click="addDistrict">确认</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="delete-confirm-dialog">
      <div class="delete-confirm-content">
        <h4>确认删除</h4>
        <p>确定要删除 {{ placeToDelete }} 吗？</p>
        <div class="delete-confirm-buttons">
          <button class="btn btn-primary" @click="cancelDelete">取消</button>
          <button class="btn btn-danger" @click="deletePlace">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 文件相关
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)

// JSON相关
const placesJson = ref<any>({
  provinces: [],
  cities: [],
  districts: []
})

// 关键词相关
const newKeyword = ref('')
const customKeywords = ref<string[]>([])

// 地名管理相关
const searchPlace = ref('')
const isSearching = ref(true)
const selectedPlaceLevel = ref('市级')
const showDeleteConfirm = ref(false)
const placeToDelete = ref('')
const placeToDeleteLevel = ref('')
const placeToDeleteIndex = ref(-1)

// 新增区划对话框状态
const showAddCityDialog = ref(false)
const showAddDistrictDialog = ref(false)
const newCityName = ref('')
const newDistrictName = ref('')

// 标签页状态
const activeTab = ref('document')

// 对比结果相关
const comparisonResults = ref<any[]>([])
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
      // 验证数据结构
      if (typeof data === 'object' && data !== null) {
        // 确保 provinces、cities 和 districts 是数组
        placesJson.value = {
          provinces: Array.isArray(data.provinces) ? data.provinces : [],
          cities: Array.isArray(data.cities) ? data.cities : [],
          districts: Array.isArray(data.districts) ? data.districts : []
        }
        console.log('获取的地名数据:', placesJson.value)
      } else {
        console.error('获取的地名数据格式错误:', data)
        // 使用默认数据结构
        placesJson.value = {
          provinces: [],
          cities: [],
          districts: []
        }
      }
    } else {
      console.error('获取地名数据失败:', response.statusText)
      // 使用默认数据结构
      placesJson.value = {
        provinces: [],
        cities: [],
        districts: []
      }
    }
  } catch (error) {
    console.error('获取地名数据时发生错误:', error)
    // 使用默认数据结构
    placesJson.value = {
      provinces: [],
      cities: [],
      districts: []
    }
  }
}

// 提取所有地名关键词
const extractPlaceKeywords = () => {
  const keywords = new Set<string>()
  
  // 添加省级行政区名称和简称
  if (placesJson.value?.provinces && Array.isArray(placesJson.value.provinces)) {
    placesJson.value.provinces.forEach((province: any) => {
      if (province?.name) keywords.add(province.name)
      if (province?.shortName) keywords.add(province.shortName)
    })
  }
  
  // 添加城市名称
  if (placesJson.value?.cities && Array.isArray(placesJson.value.cities)) {
    placesJson.value.cities.forEach((city: any) => {
      if (typeof city === 'string') keywords.add(city)
    })
  }
  
  // 添加区域名称
  if (placesJson.value?.districts && Array.isArray(placesJson.value.districts)) {
    placesJson.value.districts.forEach((district: any) => {
      if (typeof district === 'string') keywords.add(district)
    })
  }
  
  // 添加自定义关键词
  if (Array.isArray(customKeywords.value)) {
    customKeywords.value.forEach(keyword => {
      if (typeof keyword === 'string') keywords.add(keyword)
    })
  }
  
  return Array.from(keywords)
}

// 添加关键词
const addKeyword = () => {
  if (newKeyword.value.trim()) {
    // 支持逗号分隔的关键词输入，同时处理英文逗号和中文逗号
    const keywords = newKeyword.value.split(/[,，]/).map(keyword => keyword.trim()).filter(keyword => keyword)
    console.log('解析出的关键词:', keywords)
    
    // 检查关键词是否已经存在于json文件的数据中
    const existingKeywords = new Set()
    
    // 添加省级行政区名称
    placesJson.value.provinces.forEach(province => {
      existingKeywords.add(typeof province === 'string' ? province : province.name)
    })
    
    // 添加市级行政区名称
    placesJson.value.cities.forEach(city => {
      existingKeywords.add(city)
    })
    
    // 添加区级行政区名称
    placesJson.value.districts.forEach(district => {
      existingKeywords.add(district)
    })
    
    // 添加已有的自定义关键词
    customKeywords.value.forEach(keyword => {
      existingKeywords.add(keyword)
    })
    
    // 过滤掉已存在的关键词
    const newKeywords = keywords.filter(keyword => {
      if (existingKeywords.has(keyword)) {
        console.log('关键词已存在:', keyword)
        return false
      }
      existingKeywords.add(keyword)
      return true
    })
    
    // 添加新的关键词
    if (newKeywords.length > 0) {
      customKeywords.value.push(...newKeywords)
      console.log('更新后的自定义关键词:', customKeywords.value)
      if (newKeywords.length < keywords.length) {
        alert('部分关键词已存在，已添加新关键词')
      }
    } else {
      alert('所有关键词都已存在')
    }
    
    newKeyword.value = ''
  }
}

// 移除关键词
const removeKeyword = (index: number) => {
  customKeywords.value.splice(index, 1)
}

// 对比文件
const compareFiles = async () => {
  if (!selectedFile) {
    alert('请选择要对比的文件')
    return
  }
  
  isProcessing.value = true
  comparisonResults.value = []
  
  try {
    // 创建FormData对象
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    // 添加用户自定义关键词
    console.log('自定义关键词:', customKeywords.value)
    customKeywords.value.forEach((keyword, index) => {
      formData.append(`keywords[${index}]`, keyword)
      console.log(`添加关键词: keywords[${index}] = ${keyword}`)
    })
    
    // 发送文件到后端进行解析和匹配
    console.log('准备发送请求...')
    const response = await fetch('/api/file-parse', {
      method: 'POST',
      body: formData
    })
    console.log('请求发送成功，状态码:', response.status)
    
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
      
      console.log('对比结果:', comparisonResults.value)
    } else {
      throw new Error(data.message || '处理失败')
    }
  } catch (error) {
    console.error('对比文件时发生错误:', error)
    alert(`对比文件时发生错误: ${error instanceof Error ? error.message : '未知错误'}`)
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
  // 按关键词长度降序排序，确保长关键词优先匹配
  const sortedKeywords = [...keywords].sort((a, b) => b.length - a.length)
  
  sortedKeywords.forEach(keyword => {
    if (keyword && keyword.trim()) {
      const regex = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
      highlightedText = highlightedText.replace(regex, '<span class="highlight">$1</span>')
    }
  })
  
  return highlightedText
}

// 查找或添加地名
const searchOrAddPlace = async () => {
  const placeName = searchPlace.value.trim()
  if (!placeName) return
  
  if (isSearching.value) {
    // 查找地名
    const found = searchPlaceInData(placeName)
    if (found) {
      alert(`找到地名: ${placeName} (${found.level})`)
    } else {
      alert('未找到该地名，是否添加？')
      isSearching.value = false
    }
  } else {
    // 添加地名
    await addPlace(placeName, selectedPlaceLevel.value)
    searchPlace.value = ''
    isSearching.value = true
  }
}

// 在现有数据中查找地名
const searchPlaceInData = (placeName: string) => {
  // 查找省级
  for (const province of placesJson.value.provinces) {
    if (province.name === placeName || province.shortName === placeName) {
      return { level: '省级', place: province }
    }
  }
  
  // 查找市级
  for (const city of placesJson.value.cities) {
    if (city === placeName) {
      return { level: '市级', place: city }
    }
  }
  
  // 查找区级
  for (const district of placesJson.value.districts) {
    if (district === placeName) {
      return { level: '区级', place: district }
    }
  }
  
  return null
}

// 添加地名
const addPlace = async (placeName: string, level: string) => {
  try {
    // 先检查是否已存在
    if (searchPlaceInData(placeName)) {
      alert('该地名已存在')
      return
    }
    
    // 添加到本地数据
    if (level === '市级') {
      placesJson.value.cities.push(placeName)
    } else if (level === '区级') {
      placesJson.value.districts.push(placeName)
    }
    
    // 发送到后端更新JSON文件
    const response = await fetch('/api/places/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        place: placeName,
        level: level
      })
    })
    
    if (!response.ok) {
      throw new Error('添加地名失败')
    }
    
    alert('地名添加成功')
  } catch (error) {
    console.error('添加地名时发生错误:', error)
    alert('添加地名失败，请重试')
  }
}

// 确认删除地名
const confirmDeletePlace = (level: string, index: number) => {
  let placeName = ''
  
  if (level === '市级') {
    placeName = placesJson.value.cities[index]
  } else if (level === '区级') {
    placeName = placesJson.value.districts[index]
  } else if (level === '省级') {
    placeName = placesJson.value.provinces[index].name
  }
  
  placeToDelete.value = placeName
  placeToDeleteLevel.value = level
  placeToDeleteIndex.value = index
  showDeleteConfirm.value = true
}

// 删除地名
const deletePlace = async () => {
  try {
    // 从本地数据中删除
    if (placeToDeleteLevel.value === '市级') {
      placesJson.value.cities.splice(placeToDeleteIndex.value, 1)
    } else if (placeToDeleteLevel.value === '区级') {
      placesJson.value.districts.splice(placeToDeleteIndex.value, 1)
    } else if (placeToDeleteLevel.value === '省级') {
      placesJson.value.provinces.splice(placeToDeleteIndex.value, 1)
    }
    
    // 发送到后端更新JSON文件
    const response = await fetch('/api/places/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        place: placeToDelete.value,
        level: placeToDeleteLevel.value
      })
    })
    
    if (!response.ok) {
      throw new Error('删除地名失败')
    }
    
    showDeleteConfirm.value = false
    alert('地名删除成功')
  } catch (error) {
    console.error('删除地名时发生错误:', error)
    alert('删除地名失败，请重试')
  }
}

// 取消删除
const cancelDelete = () => {
  showDeleteConfirm.value = false
  placeToDelete.value = ''
  placeToDeleteLevel.value = ''
  placeToDeleteIndex.value = -1
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
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 40px;
}

section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #4a4a4a;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
}

/* 上传和关键词容器样式 */
.upload-keywords-container {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.upload-section,
.keywords-section {
  flex: 1;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 上传区域样式 */
.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: border-color 0.3s ease;
}

.upload-area:hover {
  border-color: #3498db;
}

.upload-content p {
  margin: 10px 0;
  color: #666;
}

.allowed-types {
  font-size: 12px;
  color: #999;
}

.allowed-count {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

/* 处理状态样式 */
.processing {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
  text-align: center;
}

.processing p {
  margin: 0;
  color: #666;
}

/* 无结果样式 */
.no-results {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
  text-align: center;
}

.no-results p {
  margin: 0;
  color: #666;
}

/* 无匹配样式 */
.no-matches {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #666;
}

/* 匹配项样式优化 */
.match-place {
  margin-top: 5px;
  color: #3498db;
  font-size: 14px;
}

/* 关键词高亮样式 */
:deep(.highlight) {
  background-color: #ffff00;
  color: #000;
  padding: 0 2px;
  border-radius: 2px;
  font-weight: bold;
}

/* 文件列表样式 */
.file-list {
  margin-top: 20px;
}

.file-list ul {
  list-style: none;
  padding: 0;
}

.file-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 10px;
}

/* JSON预览样式 */
.json-preview {
  margin-top: 20px;
  background-color: #f9f9f9;
  border-radius: 4px;
  padding: 15px;
  overflow-x: auto;
}

.json-preview pre {
  font-family: monospace;
  font-size: 14px;
  white-space: pre-wrap;
}

/* 关键词区域样式 */
.keyword-input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.keyword-input-group .form-control {
  flex: 1;
}

.keyword-list {
  margin-top: 20px;
}

.keyword-list ul {
  list-style: none;
  padding: 0;
}

.keyword-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-bottom: 10px;
}

/* 结果区域样式 */
.results-list {
  margin-top: 20px;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.result-item {
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.result-item h3 {
  color: #333;
  margin-bottom: 15px;
}

.match-item {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.match-location {
  font-weight: bold;
  color: #3498db;
  margin-bottom: 5px;
}

.match-text {
  color: #666;
}

/* 标签页样式 */
.tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 1px solid #e0e0e0;
}

.tab-btn {
  padding: 10px 20px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #1890ff;
}

.tab-btn.active {
  color: #1890ff;
  border-bottom-color: #1890ff;
}

/* 按钮样式 */
.btn {
  padding: 10px 20px;
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

.btn-success {
  background-color: #27ae60;
  color: white;
  box-shadow: 0 2px 4px rgba(39, 174, 96, 0.3);
}

.btn-success:hover {
  background-color: #229954;
  box-shadow: 0 4px 8px rgba(39, 174, 96, 0.4);
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
  box-shadow: 0 2px 4px rgba(231, 76, 60, 0.3);
}

.btn-danger:hover {
  background-color: #c0392b;
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

/* 表单控件样式 */
.form-control {
  padding: 10px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

/* 地名管理区域样式 */
.places-management-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.places-management-controls {
  margin-bottom: 30px;
}

.search-add-container {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.search-add-container .form-control {
  flex: 1;
}

.place-level-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.place-level-selector label {
  font-weight: 500;
  color: #4a4a4a;
}

.place-level-selector .form-control {
  width: 150px;
}

.places-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.place-category {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 15px;
}

.place-category h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 16px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
}

.place-items {
  list-style: none;
  padding: 0;
  max-height: 300px;
  overflow-y: auto;
}

.place-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #f0f0f0;
  position: relative;
}

.place-item:hover {
  background-color: #f9f9f9;
}

.place-item:last-child {
  border-bottom: none;
}

.place-shortname {
  color: #999;
  font-size: 12px;
}

.delete-btn {
  color: #e74c3c;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.place-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: #c0392b;
}

/* 删除确认对话框样式 */
.delete-confirm-dialog {
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

.delete-confirm-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.delete-confirm-content h4 {
  color: #333;
  margin-bottom: 15px;
}

.delete-confirm-content p {
  color: #666;
  margin-bottom: 20px;
}

.delete-confirm-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 区域管理样式 */
.region-section {
  margin-bottom: 40px;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  color: #333;
  font-size: 18px;
  margin: 0;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
  width: 100%;
  margin-right: 15px;
}

.add-button {
  padding: 5px 15px;
  background-color: #52c41a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

.add-button:hover {
  background-color: #73d13d;
}

/* 区域标签样式 */
.region-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.region-tag {
  display: inline-flex;
  align-items: center;
  padding: 8px 15px;
  background-color: #f0f0f0;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.region-tag:hover {
  background-color: #e0e0e0;
}

.region-tag:hover .delete-icon {
  display: inline;
}

.delete-icon {
  display: none;
  margin-left: 10px;
  color: #ff4d4f;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  padding: 0 5px;
}

.delete-icon:hover {
  background-color: rgba(255, 77, 79, 0.1);
  border-radius: 50%;
}

/* 对话框样式 */
.dialog-overlay {
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

.dialog {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.dialog h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  margin-bottom: 20px;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.cancel-button {
  padding: 8px 16px;
  background-color: white;
  color: #333;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button {
  padding: 8px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-button:hover {
  background-color: #40a9ff;
}
</style>
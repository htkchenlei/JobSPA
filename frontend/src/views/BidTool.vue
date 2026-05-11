<template>
  <div class="bid-tool">
    <h3>投标工具</h3>
    
    <!-- 标签页 -->
    <div class="tabs">
      <div 
        class="tab" 
        :class="{ active: activeTab === 'price-adjustment' }"
        @click="activeTab = 'price-adjustment'"
      >
        价格调整
      </div>
      <div 
        class="tab" 
        :class="{ active: activeTab === 'place-search' }"
        @click="activeTab = 'place-search'"
      >
        地名查询
      </div>
    </div>
    
    <!-- 价格调整标签页 -->
    <div v-if="activeTab === 'price-adjustment'" class="tab-content">
      <div class="upload-section">
        <div class="form-row">
          <label for="totalPrice">目标总价：</label>
          <input 
            type="number" 
            id="totalPrice" 
            v-model.number="targetTotalPrice" 
            min="0"
            step="0.01"
            class="form-control"
          >
        </div>
        <div class="form-row file-upload-row">
          <label for="excelFile">上传文件：</label>
          <div class="file-upload-container">
            <input 
              type="text" 
              v-model="selectedFilePath" 
              readonly 
              class="form-control file-path-input"
              placeholder="请选择Excel文件"
            >
            <input 
              type="file" 
              id="excelFile" 
              ref="fileInput"
              accept=".xlsx, .xls"
              class="file-input"
              @change="handleFileSelect"
            >
            <button type="button" class="btn btn-secondary file-select-btn" @click="openFileDialog">选择文件</button>
            <a href="/分项报价表模板.xlsx" download="分项报价表模板.xlsx" class="btn btn-secondary file-select-btn">下载模板</a>
          </div>
        </div>
        <div class="form-row">
          <label for="limitPrice">是否限价：</label>
          <div class="radio-group">
            <label>
              否
              <input type="radio" v-model="limitPrice" :value="false" checked>
            </label>
            <label>
              是
              <input type="radio" v-model="limitPrice" :value="true">
            </label>
          </div>
          <button @click="processExcel" class="btn btn-primary">开始处理</button>
        </div>
        <div class="form-row">
          <label>价格浮动区间：</label>
          <div class="price-range-container">
            <input 
              type="number" 
              v-model.number="priceMin" 
              min="0" 
              step="1"
              class="form-control price-input"
              placeholder="下限(%)"
            >
            <span class="range-separator">-</span>
            <input 
              type="number" 
              v-model.number="priceMax" 
              min="0" 
              step="1"
              class="form-control price-input"
              placeholder="上限(%)"
            >
          </div>
        </div>
      </div>
      
      <!-- 生成结果 -->
      <div v-if="processedFileUrl" class="result-section">
        <h4>处理结果：</h4>
        <p>文件处理完成，点击下方链接下载处理后的文件：</p>
        <a :href="processedFileUrl" :download="processedFileName" class="btn btn-success">下载文件</a>
      </div>
    </div>
    
    <!-- 地名查询标签页 -->
    <div v-if="activeTab === 'place-search'" class="tab-content">
      <div class="place-search-section">
        <h4>地名查询</h4>
        <div class="form-row">
          <label for="placeFile">上传文件：</label>
          <div class="file-upload-container">
            <input 
              type="text" 
              v-model="selectedPlaceFilePath" 
              readonly 
              class="form-control file-path-input"
              placeholder="请选择文件"
            >
            <input 
              type="file" 
              id="placeFile" 
              ref="placeFileInput"
              accept=".doc, .docx, .xls, .xlsx"
              class="file-input"
              @change="handlePlaceFileSelect"
            >
            <button type="button" class="btn btn-secondary file-select-btn" @click="openPlaceFileDialog">选择文件</button>
          </div>
        </div>
        <div class="form-row">
          <label for="customKeywords">自定义关键词：</label>
          <input 
            type="text" 
            id="customKeywords" 
            v-model="customKeywords" 
            class="form-control"
            placeholder="多个关键词用逗号分隔"
          >
        </div>
        <div class="form-row">
          <button @click="searchPlaces" class="btn btn-primary">开始查询</button>
        </div>
        
        <!-- 查询结果 -->
        <div v-if="placeResults.length > 0" class="result-section">
          <h4>查询结果：</h4>
          <div class="results-list">
            <div v-for="(result, index) in placeResults" :key="index" class="result-item">
              <div class="result-place">{{ result.place }}</div>
              <div class="result-location">{{ result.location }}</div>
              <div class="result-text">{{ result.text }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 地名管理 -->
      <div class="place-management-section">
        <div class="management-header" @click="isManagementExpanded = !isManagementExpanded">
          <h4>地名管理</h4>
          <div class="expand-icon" :class="{ rotated: isManagementExpanded }">▼</div>
        </div>
        
        <div v-if="isManagementExpanded" class="management-content">
          <!-- 添加地名 -->
          <div class="add-place-section">
            <h5>添加地名</h5>
            <div class="form-row">
              <label for="newPlace">地名：</label>
              <input 
                type="text" 
                id="newPlace" 
                v-model="newPlace" 
                class="form-control"
                placeholder="请输入地名"
              >
            </div>
            <div class="form-row">
              <label for="placeLevel">级别：</label>
              <select 
                id="placeLevel" 
                v-model="placeLevel" 
                class="form-control"
              >
                <option value="市级">市级</option>
                <option value="区级">区级</option>
              </select>
            </div>
            <div class="form-row">
              <button @click="addPlace" class="btn btn-primary">添加地名</button>
            </div>
            
            <!-- 已有地名 -->
            <div class="existing-places-section">
              <!-- 省级行政区 -->
              <div class="region-section">
                <h5>省级行政区</h5>
                <div class="region-tags">
                  <div 
                    v-for="(place, index) in allPlaces.provinces" 
                    :key="index" 
                    class="region-tag"
                  >
                    <span class="tag-name">{{ place.name || place }}</span>
                    <button 
                      v-if="place.name !== '北京市' && place.name !== '上海市' && place.name !== '天津市' && place.name !== '重庆市'" 
                      @click="deletePlace(place.name || place, '省级')"
                      class="delete-btn"
                      title="删除"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- 市级行政区 -->
              <div class="region-section">
                <h5>市级行政区</h5>
                <div class="region-tags">
                  <div 
                    v-for="(place, index) in allPlaces.cities" 
                    :key="index" 
                    class="region-tag"
                  >
                    <span class="tag-name">{{ place }}</span>
                    <button 
                      @click="deletePlace(place, '市级')"
                      class="delete-btn"
                      title="删除"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- 区级行政区 -->
              <div class="region-section">
                <h5>区级行政区</h5>
                <div class="region-tags">
                  <div 
                    v-for="(place, index) in allPlaces.districts" 
                    :key="index" 
                    class="region-tag"
                  >
                    <span class="tag-name">{{ place }}</span>
                    <button 
                      @click="deletePlace(place, '区级')"
                      class="delete-btn"
                      title="删除"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 标签页管理
const activeTab = ref('price-adjustment')

// Excel处理相关
const targetTotalPrice = ref(0)
const limitPrice = ref(false)
const priceMin = ref(50)
const priceMax = ref(95)
const processedFileUrl = ref('')
const processedFileName = ref('')
const fileInput = ref<HTMLInputElement>()
const selectedFilePath = ref('')

// 地名查询相关
const placeFileInput = ref<HTMLInputElement>()
const selectedPlaceFilePath = ref('')
const customKeywords = ref('')
const placeResults = ref<any[]>([])

// 地名管理相关
const newPlace = ref('')
const placeLevel = ref('市级')
const allPlaces = ref({
  provinces: [],
  cities: [],
  districts: []
})
const isManagementExpanded = ref(false)

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFilePath.value = target.files[0].path || target.files[0].name
  }
}

const openFileDialog = () => {
  fileInput.value?.click()
}

const processExcel = async () => {
  const file = fileInput.value?.files?.[0]
  if (!file) {
    alert('请选择Excel文件')
    return
  }
  
  if (!targetTotalPrice.value) {
    alert('请输入目标总价')
    return
  }
  
  const formData = new FormData()
  formData.append('file', file)
  formData.append('targetTotalPrice', targetTotalPrice.value.toString())
  formData.append('limitPrice', limitPrice.value.toString())
  formData.append('priceMin', priceMin.value.toString())
  formData.append('priceMax', priceMax.value.toString())
  
  try {
    const response = await fetch('/api/process-excel', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      processedFileUrl.value = url
      processedFileName.value = `NEW_${file.name}`
    } else {
      alert('文件处理失败')
    }
  } catch (error) {
    console.error('文件处理失败:', error)
    alert('文件处理失败')
  }
}

// 地名查询相关函数
const handlePlaceFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedPlaceFilePath.value = target.files[0].path || target.files[0].name
  }
}

const openPlaceFileDialog = () => {
  placeFileInput.value?.click()
}

const searchPlaces = async () => {
  const file = placeFileInput.value?.files?.[0]
  if (!file) {
    alert('请选择文件')
    return
  }
  
  const formData = new FormData()
  formData.append('file', file)
  
  // 添加自定义关键词
  if (customKeywords.value) {
    const keywords = customKeywords.value.split(',').map(keyword => keyword.trim())
    keywords.forEach((keyword, index) => {
      formData.append(`keywords[${index}]`, keyword)
    })
  }
  
  try {
    const response = await fetch('/api/file-parse', {
      method: 'POST',
      body: formData
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        placeResults.value = data.matches || []
      } else {
        alert('文件处理失败: ' + (data.message || '未知错误'))
      }
    } else {
      alert('文件处理失败')
    }
  } catch (error) {
    console.error('文件处理失败:', error)
    alert('文件处理失败')
  }
}

// 地名管理相关函数
const loadPlaces = async () => {
  try {
    const response = await fetch('/api/places')
    if (response.ok) {
      const data = await response.json()
      allPlaces.value = data
    }
  } catch (error) {
    console.error('获取地名数据失败:', error)
  }
}

const addPlace = async () => {
  if (!newPlace.value) {
    alert('请输入地名')
    return
  }
  
  try {
    const response = await fetch('/api/places/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        place: newPlace.value,
        level: placeLevel.value
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        alert('地名添加成功')
        newPlace.value = ''
        // 重新加载地名数据
        loadPlaces()
      } else {
        alert('添加失败: ' + (data.message || '未知错误'))
      }
    } else {
      alert('添加失败')
    }
  } catch (error) {
    console.error('添加地名失败:', error)
    alert('添加失败')
  }
}

const deletePlace = async (place: string, level: string) => {
  if (!confirm(`确定要删除地名 "${place}" 吗？`)) {
    return
  }
  
  try {
    const response = await fetch('/api/places/delete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        place: place,
        level: level
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        alert('地名删除成功')
        // 重新加载地名数据
        loadPlaces()
      } else {
        alert('删除失败: ' + (data.message || '未知错误'))
      }
    } else {
      alert('删除失败')
    }
  } catch (error) {
    console.error('删除地名失败:', error)
    alert('删除失败')
  }
}

// 页面加载时获取地名数据
loadPlaces()
</script>

<style scoped>
.bid-tool {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 标签页样式 */
.tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
}

.tab {
  padding: 10px 20px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab:hover {
  color: #3498db;
}

.tab.active {
  color: #3498db;
  border-bottom-color: #3498db;
  font-weight: 500;
}

.tab-content {
  min-height: 400px;
}

/* 上传区域样式 */
.upload-section,
.place-search-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  width: 100%;
  min-width: 600px;
}

.place-search-section h4 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 15px;
}

.form-row label {
  width: 120px;
  font-weight: 500;
  text-align: right;
  flex-shrink: 0;
}

.form-control {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

/* 文件上传样式 */
.file-upload-container {
  flex: 1;
  display: flex;
  gap: 10px;
  align-items: center;
}

.file-path-input {
  flex: 1;
  background-color: white;
}

.file-input {
  display: none;
}

.file-select-btn {
  white-space: nowrap;
}

/* 价格浮动区间样式 */
.price-range-container {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.price-input {
  width: 100px;
  text-align: center;
}

.range-separator {
  font-weight: 500;
  color: #666;
}

/* 单选按钮样式 */
.radio-group {
  display: flex;
  gap: 20px;
  align-items: center;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: normal;
  width: auto;
  text-align: left;
}

.radio-group input[type="radio"] {
  margin-left: 5px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-decoration: none;
  display: inline-block;
}

.form-row button {
  margin-left: 135px;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-success {
  background-color: #27ae60;
  color: white;
}

.btn-success:hover {
  background-color: #229954;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.result-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.result-section h4 {
  margin-bottom: 15px;
}

/* 地名查询结果样式 */
.results-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.result-item {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.result-place {
  font-weight: 500;
  color: #3498db;
  margin-bottom: 5px;
}

.result-location {
  font-size: 12px;
  color: #6c757d;
  margin-bottom: 5px;
}

.result-text {
  font-size: 14px;
  line-height: 1.4;
}

/* 地名管理样式 */
.place-management-section {
  margin-top: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  width: 100%;
  overflow: hidden;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.management-header:hover {
  background-color: #e9ecef;
}

.management-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
}

.expand-icon {
  font-size: 12px;
  color: #666;
  transition: transform 0.3s ease;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}

.management-content {
  padding: 20px;
}

.add-place-section {
  width: 100%;
}

.add-place-section h5,
.region-section h5 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #555;
  font-size: 14px;
  font-weight: 500;
}

/* 已有地名部分 */
.existing-places-section {
  margin-top: 20px;
  width: 100%;
}

/* 区域部分 */
.region-section {
  margin-bottom: 25px;
}

/* 区域标签 */
.region-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  background-color: white;
  padding: 15px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
}

/* 单个标签 */
.region-tag {
  position: relative;
  display: inline-flex;
  align-items: center;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 16px;
  padding: 6px 12px;
  margin-right: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.region-tag:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
}

.tag-name {
  margin-right: 8px;
  color: #333;
}

/* 删除按钮 */
.delete-btn {
  position: relative;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #e74c3c;
  color: white;
  border: none;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  padding: 0;
  flex-shrink: 0;
}

.region-tag:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.btn-sm {
  padding: 4px 12px;
  font-size: 12px;
  border-radius: 3px;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}
</style>
<template>
  <div class="project-management">
    <div class="project-header">
      <h3>项目管理</h3>
      <div class="header-buttons">
          <button class="btn btn-primary" @click="openAddProjectModal">新建项目</button>
          <button class="btn btn-secondary" @click="toggleCompletedProjects">
            {{ showCompletedOnly ? '查看其它' : '查看已完成' }}
          </button>
        </div>
    </div>
    
    <!-- 已完成项目 -->
    <div v-if="showCompletedOnly && completedProjects.length > 0">
      <h4 class="project-section-title">已完成项目</h4>
      <div class="project-list">
        <div 
          class="project-card" 
          :class="getStageClass(project.stage)" 
          v-for="project in completedProjects" 
          :key="project.id"
        >
        <div class="project-card-header">
          <h4 class="project-name">{{ project.name }}</h4>
          <span class="status-badge" :class="getStageClass(project.stage)">
            {{ project.stage_text }}
          </span>
        </div>
        <div class="project-card-body">
          <div class="project-info">
            <div class="info-item">
              <label>规模：</label>
              <span>{{ project.scale || '未设置' }}</span>
            </div>
            <div class="info-item">
              <label>阶段：</label>
              <span>{{ project.stage_text }}</span>
            </div>
            <div class="info-item">
              <label>更新日期：</label>
              <span>{{ getLatestUpdateDate(project.id) || '暂无更新' }}</span>
            </div>
          </div>
          <div class="project-update">
            <label>最近更新：</label>
            <p class="update-content">{{ getLatestUpdate(project.id) || '暂无更新' }}</p>
          </div>
          <div class="project-buttons">
            <button class="btn btn-sm btn-success" @click="updateProgress(project)">更新</button>
            <button class="btn btn-sm btn-info" @click="viewProjectProgress(project)">详情</button>
          </div>
        </div>
        </div>
      </div>
    </div>
    
    <!-- 非已完成项目 -->
    <template v-else>
      <!-- 进行中项目 -->
      <div v-if="activeProjects.length > 0">
        <h4 class="project-section-title">进行中项目</h4>
        <div class="project-list">
          <div 
            class="project-card" 
            :class="getStageClass(project.stage)" 
            v-for="project in activeProjects" 
            :key="project.id"
          >
          <div class="project-card-header">
            <h4 class="project-name">{{ project.name }}</h4>
            <span class="status-badge" :class="getStageClass(project.stage)">
              {{ project.stage_text }}
            </span>
          </div>
          <div class="project-card-body">
            <div class="project-info">
              <div class="info-item">
                <label>规模：</label>
                <span>{{ project.scale || '未设置' }}</span>
              </div>
              <div class="info-item">
                <label>阶段：</label>
                <span>{{ project.stage_text }}</span>
              </div>
              <div class="info-item">
                <label>更新日期：</label>
                <span>{{ getLatestUpdateDate(project.id) || '暂无更新' }}</span>
              </div>
            </div>
            <div class="project-update">
              <label>最近更新：</label>
              <p class="update-content">{{ getLatestUpdate(project.id) || '暂无更新' }}</p>
            </div>
            <div class="project-buttons">
              <button class="btn btn-sm btn-success" @click="updateProgress(project)">更新</button>
              <button class="btn btn-sm btn-info" @click="viewProjectProgress(project)">详情</button>
            </div>
          </div>
          </div>
        </div>
      </div>
      
      <!-- 超期项目 -->
      <div v-if="overdueProjects.length > 0">
        <h4 class="project-section-title">超期项目</h4>
        <div class="project-list">
          <div 
            class="project-card" 
            :class="getStageClass(project.stage)" 
            v-for="project in overdueProjects" 
            :key="project.id"
          >
          <div class="project-card-header">
            <h4 class="project-name">{{ project.name }}</h4>
            <span class="status-badge" :class="getStageClass(project.stage)">
              {{ project.stage_text }}
            </span>
          </div>
          <div class="project-card-body">
            <div class="project-info">
              <div class="info-item">
                <label>规模：</label>
                <span>{{ project.scale || '未设置' }}</span>
              </div>
              <div class="info-item">
                <label>阶段：</label>
                <span>{{ project.stage_text }}</span>
              </div>
              <div class="info-item">
                <label>更新日期：</label>
                <span>{{ getLatestUpdateDate(project.id) || '暂无更新' }}</span>
              </div>
            </div>
            <div class="project-update">
              <label>最近更新：</label>
              <p class="update-content">{{ getLatestUpdate(project.id) || '暂无更新' }}</p>
            </div>
            <div class="project-buttons">
              <button class="btn btn-sm btn-success" @click="updateProgress(project)">更新</button>
              <button class="btn btn-sm btn-info" @click="viewProjectProgress(project)">详情</button>
            </div>
          </div>
          </div>
        </div>
      </div>
    </template>
    
    <!-- 新建/编辑项目弹窗 -->
    <div v-if="showAddProject || showEditProject" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h4>{{ showAddProject ? '新建项目' : '编辑项目' }}</h4>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveProject">
            <div class="form-row">
              <div class="form-group col-md-12">
                <label>项目名称</label>
                <input type="text" v-model="formData.name" class="form-control" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-12">
                <label>客户名称</label>
                <input type="text" v-model="formData.client_name" class="form-control" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>金额</label>
                <input type="text" v-model="formData.scale" class="form-control" required>
              </div>
              <div class="form-group col-md-6">
                <label>销售</label>
                <input type="text" v-model="formData.sales_person" class="form-control" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>开始日期</label>
                <input type="date" v-model="formData.start_date" class="form-control" required>
              </div>
              <div class="form-group col-md-6">
                <label>项目阶段</label>
                <select v-model="formData.stage" class="form-control" required>
                  <option v-for="(text, value) in STAGE_MAP" :key="value" :value="value">
                    {{ text }}
                  </option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>所有者</label>
                <input type="text" v-model="formData.owner" class="form-control" disabled>
              </div>
              <div class="form-group col-md-6">
                <label>省份</label>
                <select v-model="formData.province" class="form-control" required>
                  <option value="">请选择省份</option>
                  <option v-for="province in PROVINCES" :key="province" :value="province">
                    {{ province }}
                  </option>
                </select>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>城市</label>
                <input type="text" v-model="formData.city" class="form-control">
              </div>
              <div class="form-group col-md-6">
                <label>区域</label>
                <input type="text" v-model="formData.district" class="form-control">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
              <button type="submit" class="btn btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 更新项目进展弹窗 -->
    <div v-if="showUpdateProgress" class="modal-overlay">
      <div class="modal view-progress-modal">
        <div class="modal-header">
          <h4>更新项目进展 - {{ currentProject?.name }}</h4>
          <button class="close-btn" @click="showUpdateProgress = false">&times;</button>
        </div>
        <div class="modal-body view-progress-body">
          <!-- 新更新表单 -->
          <form @submit.prevent="saveProgress" class="mb-4">
            <div class="form-group with-checkbox">
              <label for="updateContent">最新更新</label>
              <div class="checkbox-right">
                <input type="checkbox" class="form-check-input" id="importantUpdate" v-model="progressForm.is_important">
                <label class="form-check-label" for="importantUpdate">重要更新</label>
              </div>
              <textarea v-model="progressForm.update_content" class="form-control" rows="3" id="updateContent" required></textarea>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showUpdateProgress = false">取消</button>
              <button type="submit" class="btn btn-primary">保存</button>
            </div>
          </form>
          
          <!-- 历史更新记录 -->
          <div v-if="currentProjectProgress.length > 0" class="mt-4">
            <h5>历史更新记录</h5>
            <div class="progress-item" v-for="progress in currentProjectProgress" :key="progress.id" :class="{ 'important-progress': progress.is_important === 1 }">
              <div class="progress-content">
                <span class="progress-meta">{{ progress.update_date }} {{ progress.update_time }}@{{ getUserName(progress.updated_by) }}：</span>
                <span class="progress-text">{{ progress.update_content }}</span>
              </div>
            </div>
          </div>
          <div v-else class="no-progress mt-4">
            暂无更新记录
          </div>
        </div>
      </div>
    </div>
    
    <!-- 查看项目更新记录弹窗 -->
    <div v-if="showViewProgress" class="modal-overlay">
      <div class="modal view-progress-modal">
        <div class="modal-header">
          <h4>项目详情 - {{ currentProject?.name }}</h4>
          <button class="close-btn" @click="showViewProgress = false">&times;</button>
        </div>
        <div class="modal-body view-progress-body">
          <!-- 项目信息编辑表单 -->
          <form @submit.prevent="saveProject" class="mb-6">
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>项目名称</label>
                <input type="text" v-model="formData.name" class="form-control" required>
              </div>
              <div class="form-group col-md-6">
                <label>客户名称</label>
                <input type="text" v-model="formData.client_name" class="form-control" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-4">
                <label>金额</label>
                <input type="text" v-model="formData.scale" class="form-control" required>
              </div>
              <div class="form-group col-md-4">
                <label>销售</label>
                <input type="text" v-model="formData.sales_person" class="form-control" required>
              </div>
              <div class="form-group col-md-4">
                <label>开始日期</label>
                <input type="date" v-model="formData.start_date" class="form-control" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label>项目阶段</label>
                <select v-model="formData.stage" class="form-control" required>
                  <option v-for="(text, value) in STAGE_MAP" :key="value" :value="value">
                    {{ text }}
                  </option>
                </select>
              </div>
              <div class="form-group col-md-6">
                <label>所有者</label>
                <input type="text" v-model="formData.owner_username" class="form-control" disabled>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-4">
                <label>省份</label>
                <select v-model="formData.province" class="form-control" required>
                  <option value="">请选择省份</option>
                  <option v-for="province in PROVINCES" :key="province" :value="province">
                    {{ province }}
                  </option>
                </select>
              </div>
              <div class="form-group col-md-4">
                <label>城市</label>
                <input type="text" v-model="formData.city" class="form-control">
              </div>
              <div class="form-group col-md-4">
                <label>区域</label>
                <input type="text" v-model="formData.district" class="form-control">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showViewProgress = false">关闭</button>
              <button type="submit" class="btn btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 二次确认对话框 -->
    <div v-if="showConfirmDialog" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h4>确认取消</h4>
          <button class="close-btn" @click="showConfirmDialog = false">&times;</button>
        </div>
        <div class="modal-body">
          <p>您确定要取消创建项目吗？已填写的信息将不会保存。</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showConfirmDialog = false">继续编辑</button>
          <button type="button" class="btn btn-primary" @click="confirmCloseModal">确定取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

// 项目阶段映射
const STAGE_MAP = {
  1: '立项中|初步沟通',
  2: '立项中|提交立项申请',
  3: '已立项|编制解决方案',
  4: '已立项|编制设计方案',
  5: '已立项|编制招投标参数',
  6: '招投标|编制参数',
  7: '招投标|已挂网',
  8: '招投标|等待结果',
  9: '已中标|已公示',
  10: '已中标|已获取中标通知书',
  11: '已中标|签署合同',
  12: '已完成|转入项目实施',
  13: '已完成|项目结束'
}

// 中国省级行政区
const PROVINCES = [
  '北京市', '天津市', '河北省', '山西省', '内蒙古自治区',
  '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省',
  '浙江省', '安徽省', '福建省', '江西省', '山东省',
  '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区',
  '海南省', '重庆市', '四川省', '贵州省', '云南省',
  '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区',
  '新疆维吾尔自治区', '台湾省', '香港特别行政区', '澳门特别行政区'
]

// 项目数据
const projects = ref([])
// 项目进度数据
const projectProgresses = ref({})
// 用户数据
const users = ref([])
// 是否只显示已完成项目
const showCompletedOnly = ref(false)

// 弹窗状态
const showAddProject = ref(false)
const showEditProject = ref(false)
const showUpdateProgress = ref(false)
const showViewProgress = ref(false)
const showConfirmDialog = ref(false)

// 表单数据
const formData = ref({
  id: '',
  name: '',
  client_name: '',
  scale: '',
  start_date: '',
  location: '',
  sales_person: '',
  stage: 1,
  owner: '',
  owner_username: '',
  province: '',
  city: '',
  district: ''
})

// 当前项目
const currentProject = ref(null)
// 当前项目的更新记录
const currentProjectProgress = ref([])

// 进度表单数据
const progressForm = ref({
  stage: '',
  update_content: '',
  is_important: 0
})

// 获取项目数据
const fetchProjects = async () => {
  try {
    console.log('开始获取项目列表')
    const response = await fetch('/api/projects/')
    console.log('获取项目列表响应:', response.status)
    const data = await response.json()
    console.log('获取到的项目数量:', data.length)
    
    // 1. 立即更新项目列表，显示项目卡片
    // 现在API返回的数据中已经包含了最新更新的信息，不需要单独调用fetchProjectProgress
    // 使用展开运算符创建新数组，确保Vue能够检测到变化
    projects.value = [] // 先清空数组
    // 然后逐个添加项目，确保Vue能够检测到每个项目的变化
    for (const project of data) {
      projects.value.push({ ...project })
    }
    
    // 强制Vue重新渲染
    projects.value = [...projects.value]
    
    // 2. 按照每个项目最新的更新内容的日期和时间来排序
    sortProjectsByLatestUpdate()
    console.log('项目列表获取完成')
  } catch (error) {
    console.error('获取项目列表失败:', error)
  }
}

// 按照每个项目最新的更新内容的日期和时间来排序
const sortProjectsByLatestUpdate = () => {
  projects.value.sort((a, b) => {
    // 获取每个项目的最新更新日期和时间
    const getUpdateDateTime = (project) => {
      const latestUpdate = project.latest_update
      if (latestUpdate && latestUpdate.date && latestUpdate.time && latestUpdate.date !== '暂无更新' && latestUpdate.time !== '暂无更新') {
        return new Date(`${latestUpdate.date} ${latestUpdate.time}`)
      }
      return null
    }
    
    const latestA = getUpdateDateTime(a)
    const latestB = getUpdateDateTime(b)
    
    // 比较最新更新日期和时间
    if (latestA && latestB) {
      return latestB.getTime() - latestA.getTime() // 降序排序
    }
    
    // 如果一个项目有更新记录，另一个没有，有更新记录的排在前面
    if (latestA) return -1
    if (latestB) return 1
    
    // 两个项目都没有更新记录，按照项目ID排序
    return parseInt(b.id) - parseInt(a.id)
  })
}

// 获取项目最新更新的日期和时间
const getLatestUpdateDateTime = (projectId) => {
  const progresses = projectProgresses.value[projectId] || []
  if (progresses.length > 0) {
    const latest = progresses[0]
    return new Date(`${latest.update_date} ${latest.update_time}`)
  }
  return null
}

// 获取项目进度
const fetchProjectProgress = async (projectId) => {
  try {
    const response = await fetch(`/api/projects/${projectId}/progress`)
    const data = await response.json()
    // 按照日期和时间倒序排序，最近的更新在最上面
    data.sort((a, b) => {
      // 先比较日期
      const dateA = new Date(a.update_date)
      const dateB = new Date(b.update_date)
      if (dateA.getTime() !== dateB.getTime()) {
        return dateB.getTime() - dateA.getTime()
      }
      // 日期相同，比较时间
      const timeA = new Date(`2000-01-01 ${a.update_time}`)
      const timeB = new Date(`2000-01-01 ${b.update_time}`)
      return timeB.getTime() - timeA.getTime()
    })
    projectProgresses.value[projectId] = data
  } catch (error) {
    console.error(`获取项目${projectId}进度失败:`, error)
    projectProgresses.value[projectId] = []
  }
}

// 获取所有用户信息
const fetchUsers = async () => {
  try {
    const response = await fetch('/api/users/')
    const data = await response.json()
    users.value = data
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 获取最近更新内容
const getLatestUpdate = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  if (project && project.latest_update && project.latest_update.content) {
    return project.latest_update.content
  }
  return '暂无更新'
}

// 获取最近更新日期
const getLatestUpdateDate = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  if (project && project.latest_update && project.latest_update.date) {
    return project.latest_update.date
  }
  return '暂无更新'
}

// 根据用户id获取用户名
const getUserName = (userId) => {
  const user = users.value.find(u => u.id === userId)
  return user ? user.username : userId
}

// 获取阶段类名
const getStageClass = (stage) => {
  const stageNum = parseInt(stage)
  if (stageNum >= 1 && stageNum <= 2) return 'stage-initial'
  if (stageNum >= 3 && stageNum <= 5) return 'stage-approved'
  if (stageNum >= 6 && stageNum <= 8) return 'stage-bidding'
  if (stageNum >= 9 && stageNum <= 11) return 'stage-awarded'
  if (stageNum >= 12 && stageNum <= 13) return 'stage-completed'
  return 'stage-unknown'
}

// 打开编辑项目弹窗
const editProject = (project) => {
  formData.value = { ...project }
  showEditProject.value = true
  showAddProject.value = false
}

// 关闭弹窗
const closeModal = () => {
  // 显示二次确认对话框
  showConfirmDialog.value = true
}

// 保存项目
const saveProject = async () => {
  try {
    if (showEditProject.value || showViewProgress.value) {
      // 编辑现有项目（包括从详情模态框编辑）
      const projectId = formData.value.id
      // 添加调试信息
      console.log('formData.value.id:', formData.value.id)
      console.log('typeof formData.value.id:', typeof formData.value.id)
      console.log('currentProject.value:', currentProject.value)
      console.log('currentProject.value.id:', currentProject.value ? currentProject.value.id : 'undefined')
      
      // 如果formData.value.id不存在，使用currentProject.value.id
      const finalProjectId = projectId || (currentProject.value ? currentProject.value.id : null)
      console.log('finalProjectId:', finalProjectId)
      
      if (!finalProjectId) {
        console.error('项目ID不存在，无法更新项目')
        // 直接关闭模态框，不显示提示
        showAddProject.value = false
        showEditProject.value = false
        showViewProgress.value = false
        formData.value = {
          id: '',
          name: '',
          client_name: '',
          scale: '',
          start_date: '',
          location: '',
          sales_person: '',
          stage: 1,
          owner: '',
          owner_username: '',
          province: '',
          city: '',
          district: ''
        }
        return
      }
      
      // 准备更新数据，确保不包含owner_username字段
      const projectData = {
        name: formData.value.name,
        client_name: formData.value.client_name,
        scale: formData.value.scale,
        start_date: formData.value.start_date,
        location: formData.value.location || '',
        sales_person: formData.value.sales_person,
        stage: formData.value.stage,
        owner: formData.value.owner_username || formData.value.owner,
        province: formData.value.province,
        city: formData.value.city,
        district: formData.value.district
      }
      // 添加调试信息
      console.log('formData.value.owner_username:', formData.value.owner_username)
      console.log('formData.value.owner:', formData.value.owner)
      console.log('projectData.owner:', projectData.owner)
      console.log('currentProject.value.owner_username:', currentProject.value ? currentProject.value.owner_username : 'undefined')
      console.log('currentProject.value.owner:', currentProject.value ? currentProject.value.owner : 'undefined')
      
      // 确保owner字段有值
      if (!projectData.owner && currentProject.value) {
        projectData.owner = currentProject.value.owner_username || currentProject.value.owner
        console.log('更新后的projectData.owner:', projectData.owner)
      }
      
      // 确保stage字段是数字类型
      if (projectData.stage) {
        projectData.stage = parseInt(projectData.stage)
        console.log('更新后的projectData.stage:', projectData.stage, '类型:', typeof projectData.stage)
      }
      
      // 识别修改的字段
      const changes = []
      if (currentProject.value) {
        const fieldNames = {
          name: '项目名称',
          client_name: '客户名称',
          scale: '金额',
          sales_person: '销售',
          start_date: '开始日期',
          stage: '项目阶段',
          province: '省份',
          city: '城市',
          district: '区域',
          location: '位置'
        }
        
        console.log('比较字段值:')
        for (const [field, label] of Object.entries(fieldNames)) {
          const oldValue = currentProject.value[field]
          const newValue = projectData[field]
          console.log(`${label}: 旧值="${oldValue || '空'}", 新值="${newValue || '空'}", 是否不同: ${oldValue !== newValue}`)
          if (oldValue !== newValue) {
            changes.push(`${label}由"${oldValue || '空'}"变更为"${newValue || '空'}"`)
          }
        }
      }
      
      console.log('识别到的修改:', changes)
      
      // 即使没有识别到修改，也执行更新，确保数据库能够正确更新
      if (changes.length === 0) {
        changes.push('更新项目信息')
      }
      
      console.log('准备更新项目:', finalProjectId)
      console.log('更新数据:', projectData)
      
      try {
        // 首先更新项目信息
        console.log('开始更新项目，项目ID:', finalProjectId)
        console.log('更新数据:', projectData)
        
        const response = await fetch(`/api/projects/${finalProjectId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(projectData)
        })
        
        console.log('更新项目响应:', response.status)
        
        if (response.ok) {
          console.log('项目更新成功')
          
          // 如果有修改的字段，添加项目进度记录
          if (changes.length > 0) {
            // 获取当前登录用户ID
            let currentUserId = 1 // 默认值
            const userStr = localStorage.getItem('user')
            if (userStr) {
              try {
                const user = JSON.parse(userStr)
                currentUserId = user.id || 1
              } catch (e) {
                console.error('解析用户信息失败:', e)
              }
            }
            
            const updateContent = changes.join('；')
            console.log('准备添加进度记录:', updateContent)
            
            console.log('准备添加进度记录，项目ID:', finalProjectId)
            console.log('进度记录内容:', {
              stage: projectData.stage,
              update_content: updateContent,
              is_important: 0,
              updated_by: currentUserId
            })
            
            try {
              const progressResponse = await fetch(`/api/projects/${finalProjectId}/progress`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                  stage: projectData.stage,
                  update_content: updateContent,
                  is_important: 0,
                  updated_by: currentUserId
                })
              })
              
              console.log('添加进度记录响应:', progressResponse.status)
              if (!progressResponse.ok) {
                console.error('添加进度记录失败:', await progressResponse.text())
              } else {
                console.log('添加进度记录成功')
              }
            } catch (error) {
              console.error('添加进度记录时发生错误:', error)
            }
          }
          
          // 立即刷新项目列表，确保卡片信息更新
          console.log('准备刷新项目列表')
          await fetchProjects()
          // 重新排序项目列表，确保按照最新更新时间排序
          sortProjectsByLatestUpdate()
          console.log('项目列表刷新完成')
        } else {
          console.error('更新项目失败:', await response.text())
        }
      } catch (error) {
        console.error('更新项目时发生错误:', error)
      } finally {
        // 无论成功还是失败，都关闭模态框
        console.log('准备关闭模态框')
        showAddProject.value = false
        showEditProject.value = false
        showViewProgress.value = false
        formData.value = {
          id: '',
          name: '',
          client_name: '',
          scale: '',
          start_date: '',
          location: '',
          sales_person: '',
          stage: 1,
          owner: '',
          owner_username: '',
          province: '',
          city: '',
          district: ''
        }
      }
    } else {
      // 新建项目
      // 确保location字段有值
      const projectData = {
        ...formData.value,
        location: formData.value.location || '' // 如果location为空，设置为空字符串
        // owner字段保持为用户名，由后端处理转换为用户ID
      }
      const response = await fetch('/api/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(projectData)
      })
      if (response.ok) {
        const newProject = await response.json()
        
        // 1. 立即关闭模态框，不等待其他请求完成
        showAddProject.value = false
        showEditProject.value = false
        formData.value = {
          id: '',
          name: '',
          client_name: '',
          scale: '',
          start_date: '',
          location: '',
          sales_person: '',
          stage: 1,
          owner: '',
          owner_username: '',
          province: '',
          city: '',
          district: ''
        }
        
        // 2. 添加项目进度记录
        // 获取当前登录用户ID
        let currentUserId = 1 // 默认值
        const userStr = localStorage.getItem('user')
        if (userStr) {
          try {
            const user = JSON.parse(userStr)
            currentUserId = user.id || 1
          } catch (e) {
            console.error('解析用户信息失败:', e)
          }
        }
        
        await fetch(`/api/projects/${newProject.id}/progress`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            stage: newProject.stage,
            update_content: '创建项目',
            is_important: 0,
            updated_by: currentUserId
          })
        })
        
        // 3. 立即刷新项目列表并排序，确保新项目快速出现在页面上
        await fetchProjects()
      }
    }
  } catch (error) {
    console.error('保存项目失败:', error)
  }
}

// 确认关闭模态框
const confirmCloseModal = () => {
  showConfirmDialog.value = false
  // 重置表单数据
  formData.value = {
    id: '',
    name: '',
    client_name: '',
    scale: '',
    start_date: new Date().toISOString().split('T')[0],
    location: '',
    sales_person: '',
    stage: 1,
    owner: '',
    province: '',
    city: '',
    district: ''
  }
  // 设置owner为当前登录用户
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      formData.value.owner = user.username || ''
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
  // 关闭模态框
  showAddProject.value = false
  showEditProject.value = false
}

// 更新项目进展
const updateProgress = async (project) => {
  currentProject.value = project
  
  // 每次打开更新模态框时都重新获取最新的项目进度记录
  await fetchProjectProgress(project.id)
  
  // 更新当前项目进度记录
  currentProjectProgress.value = projectProgresses.value[project.id] || []
  // 强制更新数组，确保Vue能够检测到变化
  currentProjectProgress.value = [...currentProjectProgress.value]
  
  progressForm.value = {
    stage: project.stage,
    update_content: '',
    is_important: 0
  }
  showUpdateProgress.value = true
}

// 查看项目更新记录
const viewProjectProgress = async (project) => {
  console.log('viewProjectProgress called with project:', project)
  console.log('project.id:', project.id)
  console.log('typeof project.id:', typeof project.id)
  
  currentProject.value = project
  
  // 加载项目信息到表单中，供用户修改
  formData.value = { 
    ...project,
    id: project.id, // 确保id字段存在
    // 确保owner_username字段存在
    owner_username: project.owner_username || ''
  }
  
  console.log('formData.value after setting:', formData.value)
  console.log('formData.value.id:', formData.value.id)
  
  // 每次点击详情时都重新获取最新的项目进度记录
  await fetchProjectProgress(project.id)
  
  // 更新当前项目进度记录
  currentProjectProgress.value = projectProgresses.value[project.id] || []
  // 强制更新数组，确保Vue能够检测到变化
  currentProjectProgress.value = [...currentProjectProgress.value]
  // 显示详情模态框
  showViewProgress.value = true
}

// 保存进展
const saveProgress = async () => {
  try {
    if (currentProject.value) {
      const projectId = currentProject.value.id
      
      // 获取当前登录用户ID
      let currentUserId = 1 // 默认值
      const userStr = localStorage.getItem('user')
      if (userStr) {
        try {
          const user = JSON.parse(userStr)
          currentUserId = user.id || 1
        } catch (e) {
          console.error('解析用户信息失败:', e)
        }
      }
      
      // 添加用户ID到进度表单数据
      const progressData = {
        ...progressForm.value,
        updated_by: currentUserId
      }
      
      const response = await fetch(`/api/projects/${projectId}/progress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(progressData)
      })
      if (response.ok) {
        // 立即关闭模态框，提供更好的用户体验
        showUpdateProgress.value = false
        currentProject.value = null
        currentProjectProgress.value = []
        progressForm.value = {
          stage: '',
          update_content: '',
          is_important: 0
        }
        // 在后台更新项目信息和进度记录
        const updateProjectInfo = async () => {
          try {
            // 重新获取所有项目信息，确保卡片信息完全更新
            await fetchProjects()
            // 重新获取当前项目的进度记录
            await fetchProjectProgress(projectId)
          } catch (error) {
            console.error('后台更新项目信息失败:', error)
          }
        }
        // 执行后台更新
        updateProjectInfo()
      }
    }
  } catch (error) {
    console.error('保存进展失败:', error)
  }
}

// 删除项目
const deleteProject = async (id) => {
  if (confirm('确定要删除这个项目吗？')) {
    try {
      const response = await fetch(`/api/projects/${id}/`, {
        method: 'DELETE'
      })
      if (response.ok) {
        await fetchProjects()
      }
    } catch (error) {
      console.error('删除项目失败:', error)
    }
  }
}

// 切换显示已完成项目
const toggleCompletedProjects = () => {
  showCompletedOnly.value = !showCompletedOnly.value
}

// 检查项目是否超期（最近更新是否超过60天）
const isProjectOverdue = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  if (!project || !project.latest_update || !project.latest_update.date || project.latest_update.date === '暂无更新') {
    // 没有更新记录，视为超期
    return true
  }
  
  const updateDate = new Date(project.latest_update.date)
  const today = new Date()
  const diffTime = Math.abs(today - updateDate)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  return diffDays > 60
}

// 过滤项目列表
const filteredProjects = computed(() => {
  let filtered = []
  if (showCompletedOnly.value) {
    // 只显示已完成的项目（stage为12或13）
    filtered = projects.value.filter(project => {
      const stage = parseInt(project.stage)
      return stage === 12 || stage === 13
    })
  } else {
    // 不显示已完成的项目（stage不为12或13）
    filtered = projects.value.filter(project => {
      const stage = parseInt(project.stage)
      return stage !== 12 && stage !== 13
    })
  }
  
  // 排序：按照每个项目最新的更新内容的日期和时间来排序，最新的排在最前面
  filtered.sort((a, b) => {
    // 获取每个项目的最新更新日期和时间
    const getUpdateDateTime = (project) => {
      const latestUpdate = project.latest_update
      if (latestUpdate && latestUpdate.date && latestUpdate.time && latestUpdate.date !== '暂无更新' && latestUpdate.time !== '暂无更新') {
        return new Date(`${latestUpdate.date} ${latestUpdate.time}`)
      }
      return null
    }
    
    const latestA = getUpdateDateTime(a)
    const latestB = getUpdateDateTime(b)
    
    // 比较最新更新日期和时间
    if (latestA && latestB) {
      return latestB.getTime() - latestA.getTime() // 降序排序
    }
    
    // 如果一个项目有更新记录，另一个没有，有更新记录的排在前面
    if (latestA) return -1
    if (latestB) return 1
    
    // 两个项目都没有更新记录，按照项目ID排序
    return parseInt(b.id) - parseInt(a.id)
  })
  
  return filtered
})

// 进行中项目（最近60天内有更新）
const activeProjects = computed(() => {
  if (showCompletedOnly.value) return []
  return filteredProjects.value.filter(project => !isProjectOverdue(project.id))
})

// 超期项目（超过60天未更新）
const overdueProjects = computed(() => {
  if (showCompletedOnly.value) return []
  return filteredProjects.value.filter(project => isProjectOverdue(project.id))
})

// 已完成项目
const completedProjects = computed(() => {
  const filtered = projects.value.filter(project => {
    const stage = parseInt(project.stage)
    return stage === 12 || stage === 13
  })
  
  // 排序：按照每个项目最新的更新内容的日期和时间来排序，最新的排在最前面
  filtered.sort((a, b) => {
    // 获取每个项目的最新更新日期和时间
    const getUpdateDateTime = (project) => {
      const latestUpdate = project.latest_update
      if (latestUpdate && latestUpdate.date && latestUpdate.time && latestUpdate.date !== '暂无更新' && latestUpdate.time !== '暂无更新') {
        return new Date(`${latestUpdate.date} ${latestUpdate.time}`)
      }
      return null
    }
    
    const latestA = getUpdateDateTime(a)
    const latestB = getUpdateDateTime(b)
    
    // 比较最新更新日期和时间
    if (latestA && latestB) {
      return latestB.getTime() - latestA.getTime() // 降序排序
    }
    
    // 如果一个项目有更新记录，另一个没有，有更新记录的排在前面
    if (latestA) return -1
    if (latestB) return 1
    
    // 两个项目都没有更新记录，按照项目ID排序
    return parseInt(b.id) - parseInt(a.id)
  })
  
  return filtered
})

// 打开新建项目模态框
const openAddProjectModal = () => {
  // 重置表单数据
  formData.value = {
    id: '',
    name: '',
    client_name: '',
    scale: '',
    start_date: new Date().toISOString().split('T')[0], // 默认今天
    location: '',
    sales_person: '',
    stage: 1, // 默认第一个阶段
    owner: '',
    province: '',
    city: '',
    district: ''
  }
  
  // 设置owner为当前登录用户
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      formData.value.owner = user.username || ''
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
  
  showAddProject.value = true
}

// 初始化加载数据
onMounted(async () => {
  await fetchUsers()
  await fetchProjects()
})
</script>

<style scoped>
.project-management {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* 项目分类标题 */
.project-section-title {
  margin: 20px 0 10px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 8px;
  text-align: center;
}

/* 卡片式布局 */
.project-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  grid-auto-rows: 1fr;
}

.project-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.project-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.project-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.project-update {
  flex: 1;
  margin-bottom: 15px;
}

/* 不同阶段的卡片底色 */
.project-card.stage-initial {
  background-color: #e7f3ff;
  border-left: 4px solid #0066cc;
}

.project-card.stage-approved {
  background-color: #d4edda;
  border-left: 4px solid #155724;
}

.project-card.stage-bidding {
  background-color: #fff3cd;
  border-left: 4px solid #856404;
}

.project-card.stage-awarded {
  background-color: #e2f0d9;
  border-left: 4px solid #388e3c;
}

.project-card.stage-completed {
  background-color: #f3e5f5;
  border-left: 4px solid #7b1fa2;
}

.project-card.stage-unknown {
  background-color: #f8f9fa;
  border-left: 4px solid #6c757d;
}

.project-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.project-card-header {
  padding: 12px 15px;
  border-bottom: 1px solid #e9ecef;
  background-color: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.project-card-body {
  padding: 15px;
}

.project-update {
  margin-bottom: 15px;
}

.project-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 70%;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* 阶段状态样式 */
.status-badge.stage-initial {
  background-color: #e7f3ff;
  color: #0066cc;
}

.status-badge.stage-approved {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.stage-bidding {
  background-color: #fff3cd;
  color: #856404;
}

.status-badge.stage-awarded {
  background-color: #e2f0d9;
  color: #388e3c;
}

.status-badge.stage-completed {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.status-badge.stage-unknown {
  background-color: #f8f9fa;
  color: #6c757d;
}

.project-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.project-info {
  margin-bottom: 15px;
}

.info-item {
  margin-bottom: 8px;
  font-size: 14px;
}

.info-item label {
  font-weight: 500;
  color: #6c757d;
  margin-right: 5px;
}

.project-update {
  flex: 1;
  margin-bottom: 15px;
}

.project-buttons {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.project-update {
  margin-top: 15px;
}

.project-update label {
  font-weight: 500;
  color: #6c757d;
  display: block;
  margin-bottom: 5px;
}

.update-content {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
  max-height: 2.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #495057;
}

.project-buttons {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

/* 弹窗样式 */
.modal-overlay {
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

.modal {
  background-color: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h4 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #e9ecef;
  background-color: #f8f9fa;
}

/* 查看项目更新记录模态框样式 */
.view-progress-modal {
  width: 80%;
  max-width: 900px;
}

.view-progress-body {
  max-height: 60vh;
  overflow-y: auto;
}

/* 项目更新记录样式 */
.progress-item {
  margin-bottom: 15px;
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background-color: #f8f9fa;
}

/* 重要更新高亮显示 */
.important-progress {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
}

.important-progress .progress-content {
  color: #721c24;
}

.progress-content {
  font-size: 14px;
  line-height: 1.4;
  color: #495057;
}

.progress-meta {
  font-weight: 600;
  color: #495057;
}

.important-progress .progress-meta {
  color: #721c24;
  font-weight: 700;
}

.progress-text {
  color: #495057;
}

.important-progress .progress-text {
  color: #721c24;
  font-weight: 500;
}

.no-progress {
  text-align: center;
  color: #6c757d;
  padding: 20px;
  font-style: italic;
}

/* 表单样式 */
.form-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -10px;
}

.form-group {
  margin-bottom: 15px;
  padding: 0 10px;
  flex: 1;
  min-width: 200px;
}

.form-group.col-md-6 {
  flex: 0 0 50%;
  max-width: 50%;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.form-check {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.form-check-input {
  margin-right: 8px;
}

/* 带勾选框的表单组 */
.with-checkbox {
  position: relative;
}

.checkbox-right {
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  align-items: center;
}

.mb-4 {
  margin-bottom: 20px;
}

.mt-4 {
  margin-top: 20px;
}
/* 按钮样式 */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-sm {
  padding: 10px 25px;
  font-size: 14px;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.btn-info:hover {
  background-color: #138496;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .project-list {
    grid-template-columns: 1fr;
  }
}
</style>
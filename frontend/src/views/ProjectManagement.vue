<template>
  <div class="project-management">
    <div class="project-header">
      <h3>项目管理</h3>
      <div class="header-buttons">
        <n-button class="mc-btn-coral" @click="openAddProjectModal">新建项目</n-button>
        <n-button class="mc-btn-lavender" @click="toggleCompletedProjects">
          {{ showCompletedOnly ? '查看其它' : '查看已完成' }}
        </n-button>
      </div>
    </div>

    <!-- 已完成项目 -->
    <div v-if="showCompletedOnly && completedProjects.length > 0">
      <h4 class="project-section-title">已完成项目</h4>
      <div class="project-list">
        <ProjectCard
          v-for="project in completedProjects"
          :key="project.id"
          :project="project"
          :is-admin="isAdmin"
          :get-latest-update-date="getLatestUpdateDate"
          :get-latest-update="getLatestUpdate"
          @update="updateProgress"
          @view="viewProjectProgress"
          @delete="deleteProject"
        />
      </div>
    </div>

    <!-- 非已完成项目 -->
    <template v-else>
      <!-- 进行中项目 -->
      <div v-if="activeProjects.length > 0">
        <h4 class="project-section-title">进行中项目</h4>
        <div class="project-list">
          <ProjectCard
            v-for="project in activeProjects"
            :key="project.id"
            :project="project"
            :is-admin="isAdmin"
            :get-latest-update-date="getLatestUpdateDate"
            :get-latest-update="getLatestUpdate"
            @update="updateProgress"
            @view="viewProjectProgress"
            @delete="deleteProject"
          />
        </div>
      </div>

      <!-- 近期项目（1~3个月） -->
      <div v-if="overdueProjects.length > 0">
        <h4 class="project-section-title">近期项目</h4>
        <div class="project-list">
          <ProjectCard
            v-for="project in overdueProjects"
            :key="project.id"
            :project="project"
            :is-admin="isAdmin"
            :get-latest-update-date="getLatestUpdateDate"
            :get-latest-update="getLatestUpdate"
            @update="updateProgress"
            @view="viewProjectProgress"
            @delete="deleteProject"
          />
        </div>
      </div>

      <!-- 长期未更新项目（超过3个月）默认折叠，点击“显示更多”展开 -->
      <div v-if="staleProjects.length > 0" class="stale-section">
        <div class="project-section-head">
          <h4 class="project-section-title">超期项目</h4>
          <n-button class="show-more-btn mc-btn-lavender" size="small" @click="showStaleProjects = !showStaleProjects">
            {{ showStaleProjects ? '收起' : '显示更多' }}
          </n-button>
        </div>
        <div v-if="showStaleProjects" class="project-list">
          <ProjectCard
            v-for="project in staleProjects"
            :key="project.id"
            :project="project"
            :is-admin="isAdmin"
            :get-latest-update-date="getLatestUpdateDate"
            :get-latest-update="getLatestUpdate"
            @update="updateProgress"
            @view="viewProjectProgress"
            @delete="deleteProject"
          />
        </div>
      </div>
    </template>
    
    <!-- 新建/编辑项目弹窗 -->
    <n-modal
      v-model:show="showAddProject"
      preset="card"
      class="mc-modal"
      :title="'新建项目'"
      :bordered="false"
      :mask-closable="false"
      @close="closeModal"
    >
      <n-form :model="formData" class="form-grid" label-placement="top">
        <n-form-item label="项目名称" class="field-full">
          <n-input v-model:value="formData.name" placeholder="请输入项目名称" />
        </n-form-item>
        <n-form-item label="客户名称" class="field-full">
          <n-input v-model:value="formData.client_name" placeholder="请输入客户名称" />
        </n-form-item>
        <n-form-item label="金额">
          <n-input v-model:value="formData.scale" placeholder="如：120万" />
        </n-form-item>
        <n-form-item label="销售">
          <n-input v-model:value="formData.sales_person" placeholder="请输入销售" />
        </n-form-item>
        <n-form-item label="开始日期">
          <n-date-picker v-model:formatted-value="formData.start_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" />
        </n-form-item>
        <n-form-item label="项目阶段">
          <n-select v-model:value="formData.stage" :options="stageOptions" placeholder="请选择阶段" />
        </n-form-item>
        <n-form-item label="所有者">
          <n-input v-model:value="formData.owner" placeholder="请输入所有者" />
        </n-form-item>
        <n-form-item label="省份">
          <n-select v-model:value="formData.province" :options="provinceOptions" filterable placeholder="请选择省份" />
        </n-form-item>
        <n-form-item label="城市">
          <n-input v-model:value="formData.city" placeholder="请输入城市" />
        </n-form-item>
        <n-form-item label="区域">
          <n-input v-model:value="formData.district" placeholder="请输入区域" />
        </n-form-item>
      </n-form>
      <template #footer>
        <div class="mc-modal-footer">
          <n-button class="mc-btn-lavender" @click="closeModal">取消</n-button>
          <n-button class="mc-btn-coral" :loading="savingProject" @click="saveProject">保存</n-button>
        </div>
      </template>
    </n-modal>

    <!-- 编辑项目弹窗（复用同一套表单，避免结构与主题分叉） -->
    <n-modal
      v-model:show="showEditProject"
      preset="card"
      class="mc-modal"
      title="编辑项目"
      :bordered="false"
      :mask-closable="false"
      @close="closeModal"
    >
      <n-form :model="formData" class="form-grid" label-placement="top">
        <n-form-item label="项目名称" class="field-full">
          <n-input v-model:value="formData.name" placeholder="请输入项目名称" />
        </n-form-item>
        <n-form-item label="客户名称" class="field-full">
          <n-input v-model:value="formData.client_name" placeholder="请输入客户名称" />
        </n-form-item>
        <n-form-item label="金额">
          <n-input v-model:value="formData.scale" placeholder="如：120万" />
        </n-form-item>
        <n-form-item label="销售">
          <n-input v-model:value="formData.sales_person" placeholder="请输入销售" />
        </n-form-item>
        <n-form-item label="开始日期">
          <n-date-picker v-model:formatted-value="formData.start_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" />
        </n-form-item>
        <n-form-item label="项目阶段">
          <n-select v-model:value="formData.stage" :options="stageOptions" placeholder="请选择阶段" />
        </n-form-item>
        <n-form-item label="所有者">
          <n-input v-model:value="formData.owner" placeholder="请输入所有者" />
        </n-form-item>
        <n-form-item label="省份">
          <n-select v-model:value="formData.province" :options="provinceOptions" filterable placeholder="请选择省份" />
        </n-form-item>
        <n-form-item label="城市">
          <n-input v-model:value="formData.city" placeholder="请输入城市" />
        </n-form-item>
        <n-form-item label="区域">
          <n-input v-model:value="formData.district" placeholder="请输入区域" />
        </n-form-item>
      </n-form>
      <template #footer>
        <div class="mc-modal-footer">
          <n-button class="mc-btn-lavender" @click="closeModal">取消</n-button>
          <n-button class="mc-btn-coral" :loading="savingProject" @click="saveProject">保存</n-button>
        </div>
      </template>
    </n-modal>

    <!-- 更新项目进展弹窗 -->
    <n-modal
      v-model:show="showUpdateProgress"
      preset="card"
      class="mc-modal view-progress-modal"
      :title="`更新项目进展 - ${currentProject?.name || ''}`"
      :bordered="false"
    >
      <div class="view-progress-body">
        <!-- 新更新表单 -->
        <n-form :model="progressForm" label-placement="top" class="progress-form">
          <n-form-item label="最新更新">
            <template #label>
              <div class="progress-label-row">
                <span>最新更新</span>
                <n-checkbox v-model:checked="progressForm.is_important">重要更新</n-checkbox>
              </div>
            </template>
            <n-input
              v-model:value="progressForm.update_content"
              type="textarea"
              :rows="3"
              :placeholder="'请填写本次更新内容'"
            />
          </n-form-item>
        </n-form>
        <div class="mc-modal-footer progress-actions">
          <n-button class="mc-btn-lavender" @click="showUpdateProgress = false">取消</n-button>
          <n-button class="mc-btn-coral" :loading="savingProgress" @click="saveProgress">保存</n-button>
        </div>

        <!-- 历史更新记录 -->
        <h5 class="progress-history-title">历史更新记录</h5>
        <n-timeline v-if="currentProjectProgress && currentProjectProgress.length > 0" class="progress-timeline">
          <n-timeline-item
            v-for="(progress, index) in currentProjectProgress"
            :key="index"
            :type="progress.is_important === 1 ? 'error' : 'success'"
            :color="progress.is_important === 1 ? IMPORTANT_COLOR : getStageMeta(5).solid"
            :time="`${progress.update_date} ${progress.update_time}@${getUserName(progress.updated_by)}`"
          >
            <span :class="{ 'important-progress-text': progress.is_important === 1 }">
              {{ progress.update_content }}
            </span>
          </n-timeline-item>
        </n-timeline>
        <n-empty v-else description="暂无更新记录" size="small" />
      </div>
    </n-modal>

    <!-- 查看项目更新记录弹窗 -->
    <n-modal
      v-model:show="showViewProgress"
      preset="card"
      class="mc-modal view-progress-modal"
      :title="`项目详情 - ${currentProject?.name || ''}`"
      :bordered="false"
    >
      <div class="view-progress-body">
          <!-- 项目信息编辑表单 -->
          <n-form :model="formData" class="form-grid detail-form" label-placement="top">
            <n-form-item label="项目名称">
              <n-input v-model:value="formData.name" placeholder="请输入项目名称" />
            </n-form-item>
            <n-form-item label="客户名称">
              <n-input v-model:value="formData.client_name" placeholder="请输入客户名称" />
            </n-form-item>
            <n-form-item label="金额">
              <n-input v-model:value="formData.scale" placeholder="如：120万" />
            </n-form-item>
            <n-form-item label="销售">
              <n-input v-model:value="formData.sales_person" placeholder="请输入销售" />
            </n-form-item>
            <n-form-item label="开始日期">
              <n-date-picker v-model:formatted-value="formData.start_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期" />
            </n-form-item>
            <n-form-item label="项目阶段">
              <n-select v-model:value="formData.stage" :options="stageOptions" placeholder="请选择阶段" />
            </n-form-item>
            <n-form-item label="所有者">
              <n-input v-model:value="formData.owner_username" placeholder="请输入所有者" />
            </n-form-item>
            <n-form-item label="省份">
              <n-select v-model:value="formData.province" :options="provinceOptions" filterable placeholder="请选择省份" />
            </n-form-item>
            <n-form-item label="城市">
              <n-input v-model:value="formData.city" placeholder="请输入城市" />
            </n-form-item>
            <n-form-item label="区域">
              <n-input v-model:value="formData.district" placeholder="请输入区域" />
            </n-form-item>
          </n-form>
          <div class="mc-modal-footer">
            <n-button class="mc-btn-lavender" @click="showViewProgress = false">关闭</n-button>
            <n-button class="mc-btn-coral" :loading="savingProject" @click="saveProject">保存</n-button>
          </div>
      </div>
    </n-modal>

    <!-- 二次确认对话框 -->
    <n-modal
      v-model:show="showConfirmDialog"
      preset="dialog"
      class="mc-modal"
      type="warning"
      title="确认取消"
      content="您确定要取消吗？已填写的信息将不会保存。"
      positive-text="确定取消"
      negative-text="继续编辑"
      @positive-click="confirmCloseModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  NButton, NModal, NForm, NFormItem, NInput, NSelect, NDatePicker,
  NTag, NTimeline, NTimelineItem, NCheckbox, NEmpty, NPopconfirm, NSpin
} from 'naive-ui'
import { message, dialog } from '../utils/feedback'
import ProjectCard from '../components/ProjectCard.vue'
import { getStageMeta, IMPORTANT_COLOR } from '../constants/stageColors'

const route = useRoute()

// 项目阶段映射（统一 5 档）
const STAGE_MAP: Record<number, string> = {
  1: '立项中',
  2: '已立项',
  3: '招投标',
  4: '已中标',
  5: '已完成'
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

// n-select 选项
const stageOptions = Object.entries(STAGE_MAP).map(([value, label]) => ({
  label,
  value: Number(value)
}))
const provinceOptions = PROVINCES.map((p) => ({ label: p, value: p }))

// 项目数据
const projects = ref([])
// 项目进度数据
const projectProgresses = ref({})
// 用户数据
const users = ref([])
// 是否只显示已完成项目
const showCompletedOnly = ref(false)
// 当前登录用户是否为管理员
const isAdmin = ref(false)

// 弹窗状态
const showAddProject = ref(false)
const showEditProject = ref(false)
const showUpdateProgress = ref(false)
const showViewProgress = ref(false)
const showConfirmDialog = ref(false)

// 防重复提交状态
const savingProgress = ref(false)
const savingProject = ref(false)

// 表单数据
// 注意：start_date 绑定到 n-date-picker，空值必须是 null。
// 传 '' 会在组件内部 formatDate('') 时抛 RangeError: Invalid time value，导致整页白屏。
const formData = ref<{
  id: string
  name: string
  client_name: string
  scale: string
  start_date: string | null
  location: string
  sales_person: string
  stage: number
  owner: string
  owner_username: string
  province: string
  city: string
  district: string
}>({
  id: '',
  name: '',
  client_name: '',
  scale: '',
  start_date: null,
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
    console.log(`开始获取项目${projectId}的进度记录`)
    
    // 直接调用API获取项目进度记录
    const response = await fetch(`/api/projects/${projectId}/progress`)
    
    if (!response.ok) {
      console.error(`获取项目${projectId}进度失败:`, response.status)
      projectProgresses.value[projectId] = []
      return
    }
    
    const data = await response.json()
    console.log(`获取到项目${projectId}的进度记录数量:`, data.length)
    console.log(`获取到的进度记录:`, data)
    
    // 确保data是一个数组
    if (Array.isArray(data)) {
      // 按照日期和时间倒序排序，最近的更新在最上面
      const sortedProgress = [...data].sort((a, b) => {
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
      projectProgresses.value[projectId] = sortedProgress
    } else {
      console.error(`项目${projectId}的进度记录不是数组:`, data)
      projectProgresses.value[projectId] = []
    }
    console.log(`更新后projectProgresses[${projectId}]:`, projectProgresses.value[projectId])
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
  if (stageNum === 1) return 'stage-initial'
  if (stageNum === 2) return 'stage-approved'
  if (stageNum === 3) return 'stage-bidding'
  if (stageNum === 4) return 'stage-awarded'
  if (stageNum === 5) return 'stage-completed'
  return 'stage-unknown'
}

// 打开编辑项目弹窗
const editProject = (project) => {
  formData.value = { ...project }
  showEditProject.value = true
  showAddProject.value = false
}

// 关闭弹窗：弹窗内已填写内容时先二次确认
const closeModal = () => {
  showConfirmDialog.value = true
}

// 保存项目
const saveProject = async () => {
  // 防重复提交：上一次请求未完成前忽略本次提交
  if (savingProject.value) return
  savingProject.value = true
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
          start_date: null,
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
        projectData.stage = parseInt(String(projectData.stage))
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
            // 对于项目阶段，将数字转换为阶段名称
            if (field === 'stage') {
              // 确保使用数字作为键来查找STAGE_MAP
              const oldStageKey = parseInt(String(oldValue))
              const newStageKey = parseInt(String(newValue))
              const oldStageName = STAGE_MAP[oldStageKey] || String(oldValue) || '空'
              const newStageName = STAGE_MAP[newStageKey] || String(newValue) || '空'
              changes.push(`${label}由"${oldStageName}"变更为"${newStageName}"`)
            } else {
              changes.push(`${label}由"${oldValue || '空'}"变更为"${newValue || '空'}"`)
            }
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
            const userStr = sessionStorage.getItem('user')
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
          start_date: null,
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
          start_date: null,
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
        const userStr = sessionStorage.getItem('user')
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
    message.error('保存失败，请重试')
  } finally {
    savingProject.value = false
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
    owner_username: '',
    province: '',
    city: '',
    district: ''
  }
  // 设置owner为当前登录用户
  const userStr = sessionStorage.getItem('user')
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
  console.log('updateProgress called with project:', project)
  console.log('project.id:', project.id)
  
  currentProject.value = project
  const projectId = project.id
  
  // 每次打开更新模态框时都重新获取最新的项目进度记录
  console.log('开始获取项目进度记录')
  await fetchProjectProgress(projectId)
  console.log('获取项目进度记录完成')
  
  // 直接更新当前项目进度记录，不需要setTimeout
  console.log('projectProgresses.value[projectId]:', projectProgresses.value[projectId])
  currentProjectProgress.value = projectProgresses.value[projectId] || []
  console.log('currentProjectProgress.value before update:', currentProjectProgress.value)
  // 强制更新数组，确保Vue能够检测到变化
  currentProjectProgress.value = [...currentProjectProgress.value]
  console.log('currentProjectProgress.value after update:', currentProjectProgress.value)
  
  progressForm.value = {
    stage: project.stage,
    update_content: '',
    is_important: 0
  }
  showUpdateProgress.value = true
  console.log('showUpdateProgress set to true')
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
  // 防重复提交：上一次请求未完成前忽略本次提交
  if (savingProgress.value) return
  savingProgress.value = true
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
        message.success('进展已保存')
      } else {
        message.error('保存失败，请重试')
      }
    }
  } catch (error) {
    console.error('保存进展失败:', error)
    message.error('保存失败，请重试')
  } finally {
    savingProgress.value = false
  }
}

// 删除项目（确认由模板中的 n-popconfirm 负责，此处只执行删除）
const deleteProject = async (id) => {
  try {
    const token = sessionStorage.getItem('token')
    const response = await fetch(`/api/projects/${id}`, {
      method: 'DELETE',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    if (response.ok) {
      message.success('项目已删除')
      await fetchProjects()
    } else if (response.status === 403) {
      message.error('无权限：仅管理员可删除项目')
    } else {
      const err = await response.json().catch(() => null)
      message.error('删除失败: ' + (err?.error || response.statusText))
    }
  } catch (error) {
    console.error('删除项目失败:', error)
    message.error('删除项目失败，请稍后重试')
  }
}

// 切换显示已完成项目
const toggleCompletedProjects = () => {
  showCompletedOnly.value = !showCompletedOnly.value
}

// 获取项目距离最近更新的天数（无更新记录返回 null）
const getDaysSinceUpdate = (project) => {
  if (!project || !project.latest_update || !project.latest_update.date || project.latest_update.date === '暂无更新') {
    return null
  }
  const updateDate = new Date(project.latest_update.date)
  const today = new Date()
  return Math.floor((today.getTime() - updateDate.getTime()) / (1000 * 60 * 60 * 24))
}

// 过滤项目列表
const filteredProjects = computed(() => {
  let filtered = []
  if (showCompletedOnly.value) {
    // 只显示已完成的项目（stage 为 5）
    filtered = projects.value.filter(project => {
      const stage = parseInt(project.stage)
      return stage === 5
    })
  } else {
    // 不显示已完成的项目（stage 不为 5）
    filtered = projects.value.filter(project => {
      const stage = parseInt(project.stage)
      return stage !== 5
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

// 是否展开显示“超过3个月”的长期未更新项目
const showStaleProjects = ref(false)

// 进行中项目：1个月内（30天内）有更新
const activeProjects = computed(() => {
  if (showCompletedOnly.value) return []
  return filteredProjects.value.filter(project => {
    const days = getDaysSinceUpdate(project)
    return days !== null && days <= 30
  })
})

// 超期项目：超过1个月且不超过3个月（30~90天）未更新
const overdueProjects = computed(() => {
  if (showCompletedOnly.value) return []
  return filteredProjects.value.filter(project => {
    const days = getDaysSinceUpdate(project)
    return days !== null && days > 30 && days <= 90
  })
})

// 长期未更新项目：超过3个月（90天以上）或从无更新记录，默认收起，点“显示更多”展示
const staleProjects = computed(() => {
  if (showCompletedOnly.value) return []
  return filteredProjects.value.filter(project => {
    const days = getDaysSinceUpdate(project)
    return days === null || days > 90
  })
})

// 已完成项目
const completedProjects = computed(() => {
  const filtered = projects.value.filter(project => {
    const stage = parseInt(project.stage)
    return stage === 5
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
    owner_username: '',
    province: '',
    city: '',
    district: ''
  }
  
  // 设置owner为当前登录用户
  const userStr = sessionStorage.getItem('user')
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
  // 从 URL 参数判断是否直接进入“已完成”视图（仪表盘“已完成”卡片跳转而来）
  if (route.query.view === 'completed') {
    showCompletedOnly.value = true
  }
  // 读取当前登录用户信息，判断是否为管理员
  const userStr = sessionStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      isAdmin.value = !!user.is_admin
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
  await fetchUsers()
  await fetchProjects()
})
</script>

<style scoped>
/* 项目管理页面 - 马卡龙风格 */
.project-management {
  padding: 0;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.project-header h3 {
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
  margin: 0;
}

.header-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 项目分类标题 */
.project-section-title {
  margin: 24px 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #8B8899;
  padding-bottom: 12px;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 12px;
}

.project-section-title::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(180deg, #FF9A8B, #FFB7B2);
  border-radius: 2px;
}

/* 分类标题行（标题 + 显示更多按钮） */
.project-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.project-section-head .project-section-title {
  margin: 24px 0 16px 0;
}

.show-more-btn {
  background: linear-gradient(135deg, #C3B1E1 0%, #B19FD0 100%);
  color: white;
  border: none;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(195, 177, 225, 0.35);
}

.show-more-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(195, 177, 225, 0.5);
}

/* 卡片式布局 */
.project-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 20px;
  grid-auto-rows: 1fr;
}

.project-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  border: 1px solid #F0E6E3;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

.project-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.project-update {
  flex: 1;
  margin-bottom: 16px;
}

/* 不同阶段的卡片边框颜色 - 马卡龙配色 */
.project-card.stage-initial {
  border-left: 4px solid #7EC8E3;
  background: linear-gradient(135deg, rgba(126, 200, 227, 0.05) 0%, white 100%);
}

.project-card.stage-approved {
  border-left: 4px solid #A8E6CF;
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.05) 0%, white 100%);
}

.project-card.stage-bidding {
  border-left: 4px solid #FFEAA7;
  background: linear-gradient(135deg, rgba(255, 234, 167, 0.1) 0%, white 100%);
}

.project-card.stage-awarded {
  border-left: 4px solid #FFB7B2;
  background: linear-gradient(135deg, rgba(255, 183, 178, 0.05) 0%, white 100%);
}

.project-card.stage-completed {
  border-left: 4px solid #C3B1E1;
  background: linear-gradient(135deg, rgba(195, 177, 225, 0.05) 0%, white 100%);
}

.project-card.stage-unknown {
  border-left: 4px solid #D4C4F0;
  background: white;
}

.project-card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.08), rgba(255, 154, 139, 0.08));
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.project-card-body {
  padding: 20px;
}

.project-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 70%;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

/* 阶段状态样式 - 马卡龙配色 */
.status-badge.stage-initial {
  background: linear-gradient(135deg, #7EC8E3, #6BB8D3);
  color: white;
}

.status-badge.stage-approved {
  background: linear-gradient(135deg, #A8E6CF, #88D8B0);
  color: white;
}

.status-badge.stage-bidding {
  background: linear-gradient(135deg, #FFEAA7, #FDCB6E);
  color: #5D5A6D;
}

.status-badge.stage-awarded {
  background: linear-gradient(135deg, #FFB7B2, #FF9A8B);
  color: white;
}

.status-badge.stage-completed {
  background: linear-gradient(135deg, #C3B1E1, #B19FD0);
  color: white;
}

.status-badge.stage-unknown {
  background: #E8E0F0;
  color: #8B8899;
}

.project-info {
  margin-bottom: 16px;
}

.info-item {
  margin-bottom: 8px;
  font-size: 13px;
}

.info-item label {
  font-weight: 500;
  color: #8B8899;
  margin-right: 8px;
}

.info-item span {
  color: #5D5A6D;
}

.project-buttons {
  margin-top: 16px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.project-update {
  margin-top: 16px;
}

.project-update label {
  font-weight: 500;
  color: #8B8899;
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
}

.update-content {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  max-height: 3em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #5D5A6D;
}

/* ==================== 弹窗（n-modal）样式 ====================
   注意：n-modal 被 teleport 到 body，scoped 的 :deep(.mc-modal) 无法命中，
   .mc-modal 全部外观样式统一写在 src/style.css 中，此处只保留业务内部结构样式。 */

/* 弹窗内容不设独立 max-height/overflow：滚动统一由 .mc-modal .n-card-content
   （style.css，弹窗总高超 88vh 时才滚动）承接，滚动条位于内容区右缘，
   距文本/按钮约 24px，颜色沿用全局薄荷绿渐变。 */

.mc-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

/* label 容器撑满整行，使「最新更新 / 重要更新」两端对齐生效 */
.progress-form :deep(.n-form-item-label) {
  display: block;
  width: 100%;
}

.progress-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 12px;
}

.progress-history-title {
  margin: 20px 0 12px;
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
}

.progress-timeline {
  padding-left: 2px;
}

.important-progress-text {
  color: #D35D6E;
  font-weight: 600;
}

/* 表单栅格：n-form-item 自适应两列 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 16px;
}

.form-grid :deep(.n-form-item) {
  min-width: 0;
}

.form-grid .field-full,
.form-grid :deep(.field-full) {
  grid-column: 1 / -1;
}

.form-grid :deep(.n-input),
.form-grid :deep(.n-date-picker),
.form-grid :deep(.n-select) {
  width: 100%;
}

.progress-actions {
  margin-top: 4px;
}

/* 按钮/头部区域的 n-button 在移动端等宽平分 */
.header-buttons :deep(.n-button) {
  min-width: 108px;
}

/* ==================== 移动端适配 ==================== */
@media (max-width: 768px) {
  .project-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .project-header h3 {
    font-size: 20px;
  }

  .header-buttons {
    width: 100%;
  }

  .header-buttons :deep(.n-button) {
    flex: 1;
    min-width: 0;
  }

  .project-list {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .project-section-title {
    margin: 16px 0 12px 0;
    font-size: 15px;
  }

  .project-section-head .project-section-title {
    margin: 16px 0 12px 0;
  }

  /* 移动端抽屉外观（.mc-modal 相关规则见 src/style.css 全局段） */
  .mc-modal-footer {
    margin-top: 0;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>
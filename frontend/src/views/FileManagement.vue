<template>
  <div class="file-management">
    <div class="file-header">
      <h3>文件管理</h3>
      <div class="header-actions">
        <button class="btn btn-primary" @click="createFolder">新建文件夹</button>
        <button class="btn btn-success" @click="uploadFile">上传文件</button>
      </div>
    </div>
    
    <div class="file-content">
      <!-- 左侧树形结构 -->
      <div class="file-tree">
        <h4>文件夹结构</h4>
        <ul class="tree">
          <li class="tree-node">
            <div class="tree-node-content" @click="toggleNode(rootFolder)">
              <span class="tree-icon">{{ rootFolder.expanded ? '📁' : '📂' }}</span>
              <span class="tree-label">{{ rootFolder.name }}</span>
              <div class="tree-node-actions">
                <button class="tree-action-btn" @click.stop="createSubFolder(rootFolder)">📁</button>
                <button class="tree-action-btn" @click.stop="uploadToFolder(rootFolder)">⬆️</button>
              </div>
            </div>
            <ul v-if="rootFolder.expanded" class="tree-children">
              <tree-node
                v-for="node in rootFolder.children"
                :key="node.id"
                :node="node"
                @toggle="toggleNode"
                @create-folder="createSubFolder"
                @upload-file="uploadToFolder"
                @delete="deleteNode"
              />
            </ul>
          </li>
        </ul>
      </div>
      
      <!-- 右侧文件列表 -->
      <div class="file-list">
        <h4>{{ currentPath }}</h4>
        <div v-if="currentFiles.length === 0" class="empty-state">
          该文件夹为空
        </div>
        <div v-else class="files">
          <div v-for="file in currentFiles" :key="file.id" class="file-item">
            <div class="file-icon">
              {{ getFileIcon(file.type) }}
            </div>
            <div class="file-info">
              <div class="file-name">{{ file.name }}</div>
              <div class="file-meta">
                <span>{{ file.size }}</span>
                <span>{{ file.uploadedAt }}</span>
              </div>
            </div>
            <div class="file-actions">
              <button class="btn btn-sm btn-info">下载</button>
              <button class="btn btn-sm btn-danger" @click="deleteFile(file.id)">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 新建文件夹弹窗 -->
    <div v-if="showCreateFolder" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h4>新建文件夹</h4>
          <button class="close-btn" @click="showCreateFolder = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveFolder">
            <div class="form-group">
              <label>文件夹名称</label>
              <input type="text" v-model="folderForm.name" class="form-control" required>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showCreateFolder = false">取消</button>
              <button type="submit" class="btn btn-primary">创建</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 上传文件弹窗 -->
    <div v-if="showUploadFile" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h4>上传文件</h4>
          <button class="close-btn" @click="showUploadFile = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleFileUpload">
            <div class="form-group">
              <label>选择文件</label>
              <input type="file" ref="fileInput" class="form-control" multiple required>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showUploadFile = false">取消</button>
              <button type="submit" class="btn btn-primary">上传</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import TreeNode from '../components/TreeNode.vue'

// 模拟文件系统数据
const rootFolder = ref({
  id: 'root',
  name: '根目录',
  type: 'folder',
  expanded: true,
  children: [
    {
      id: 'folder1',
      name: '项目文档',
      type: 'folder',
      expanded: false,
      children: [
        {
          id: 'file1',
          name: '项目方案.docx',
          type: 'document',
          size: '2.5MB',
          uploadedAt: '2026-01-01'
        }
      ]
    },
    {
      id: 'folder2',
      name: '会议记录',
      type: 'folder',
      expanded: false,
      children: []
    }
  ]
})

// 当前选中的文件夹
const currentFolder = ref(rootFolder.value)

// 弹窗状态
const showCreateFolder = ref(false)
const showUploadFile = ref(false)

// 文件夹表单
const folderForm = ref({
  name: '',
  parentId: 'root'
})

// 文件设置
const fileSettings = ref({
  rootDirectory: '',
  allowedTypes: 'jpg,png,gif,doc,docx,txt,pdf,xls,xlsx,ppt,pptx',
  maxFileSize: 50
})

// 计算当前路径
const currentPath = computed(() => {
  return getPath(currentFolder.value)
})

// 计算当前文件夹中的文件
const currentFiles = computed(() => {
  return currentFolder.value.children.filter(item => item.type !== 'folder')
})

// 初始化
onMounted(() => {
  // 从localStorage获取文件设置
  const fileSettingsStr = localStorage.getItem('fileSettings')
  if (fileSettingsStr) {
    fileSettings.value = { ...fileSettings.value, ...JSON.parse(fileSettingsStr) }
  }
  
  // 从后端获取文件系统数据
  fetchFileSystem()
})

// 从后端获取文件系统数据
const fetchFileSystem = async () => {
  try {
    const token = sessionStorage.getItem('token')
    console.log('Fetching file system with token:', token)
    
    if (!token) {
      console.error('No token found, please login first')
      // 可以在这里添加提示，让用户登录
      return
    }
    
    const response = await fetch('/api/files/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    console.log('File API response status:', response.status)
    if (response.ok) {
      const data = await response.json()
      // 根据后端返回的数据更新rootFolder
      console.log('文件系统数据:', data)
      // 更新根文件夹数据
      if (data) {
        rootFolder.value = {
          ...rootFolder.value,
          children: data.children || []
        }
      }
    } else {
      const errorData = await response.json()
      console.error('File API error:', errorData)
    }
  } catch (error) {
    console.error('获取文件系统数据失败:', error)
  }
}

// 获取文件路径
const getPath = (node) => {
  if (node.id === 'root') return node.name
  let path = node.name
  let parent = findParent(node.id)
  while (parent && parent.id !== 'root') {
    path = parent.name + ' / ' + path
    parent = findParent(parent.id)
  }
  return '根目录 / ' + path
}

// 查找父节点
const findParent = (nodeId) => {
  const findParentRecursive = (nodes) => {
    for (const node of nodes) {
      if (node.children) {
        if (node.children.some(child => child.id === nodeId)) {
          return node
        }
        const parent = findParentRecursive(node.children)
        if (parent) return parent
      }
    }
    return null
  }
  return findParentRecursive(rootFolder.value.children)
}

// 切换节点展开/折叠
const toggleNode = (node) => {
  node.expanded = !node.expanded
  currentFolder.value = node
}

// 新建文件夹
const createFolder = () => {
  folderForm.value.parentId = currentFolder.value.id
  showCreateFolder.value = true
}

// 在子文件夹中新建文件夹
const createSubFolder = (parentNode) => {
  console.log('创建子文件夹，父节点:', parentNode)
  folderForm.value.parentId = parentNode.id
  showCreateFolder.value = true
}

// 保存文件夹
const saveFolder = async () => {
  try {
    console.log('保存文件夹，表单数据:', folderForm.value)
    const token = sessionStorage.getItem('token')
    const response = await fetch('/api/files/folders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify({
        name: folderForm.value.name,
        parentId: folderForm.value.parentId
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      console.log('后端创建文件夹响应:', data)
      // 后端创建成功后，更新前端数据
      const newFolder = {
        id: folderForm.value.parentId === 'root' ? folderForm.value.name : folderForm.value.parentId + '/' + folderForm.value.name,
        name: folderForm.value.name,
        type: 'folder',
        expanded: false,
        children: []
      }
      
      const addToFolder = (nodes) => {
        for (const node of nodes) {
          if (node.id === folderForm.value.parentId) {
            node.children.push(newFolder)
            return true
          }
          if (node.children && addToFolder(node.children)) {
            return true
          }
        }
        return false
      }
      
      if (folderForm.value.parentId === 'root') {
        rootFolder.value.children.push(newFolder)
      } else {
        addToFolder(rootFolder.value.children)
      }
      
      showCreateFolder.value = false
      folderForm.value.name = ''
    }
  } catch (error) {
    console.error('创建文件夹失败:', error)
    // 如果后端创建失败，使用前端模拟数据
    const newFolder = {
      id: folderForm.value.parentId === 'root' ? folderForm.value.name : folderForm.value.parentId + '/' + folderForm.value.name,
      name: folderForm.value.name,
      type: 'folder',
      expanded: false,
      children: []
    }
    
    const addToFolder = (nodes) => {
      for (const node of nodes) {
        if (node.id === folderForm.value.parentId) {
          node.children.push(newFolder)
          return true
        }
        if (node.children && addToFolder(node.children)) {
          return true
        }
      }
      return false
    }
    
    if (folderForm.value.parentId === 'root') {
      rootFolder.value.children.push(newFolder)
    } else {
      addToFolder(rootFolder.value.children)
    }
    
    showCreateFolder.value = false
    folderForm.value.name = ''
  }
}

// 上传文件
const uploadFile = () => {
  showUploadFile.value = true
}

// 上传到指定文件夹
const uploadToFolder = (folderNode) => {
  currentFolder.value = folderNode
  showUploadFile.value = true
}

// 处理文件上传
const handleFileUpload = async () => {
  const fileInput = document.querySelector('input[type="file"]')
  if (fileInput.files.length > 0) {
    try {
      const token = sessionStorage.getItem('token')
      const formData = new FormData()
      
      for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('files', fileInput.files[i])
      }
      formData.append('folderId', currentFolder.value.id)
      
      const response = await fetch('/api/files/upload', {
        method: 'POST',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: formData
      })
      
      if (response.ok) {
        // 后端上传成功后，更新前端数据
        for (let i = 0; i < fileInput.files.length; i++) {
          const file = fileInput.files[i]
          const newFile = {
            id: 'file_' + Date.now() + i,
            name: file.name,
            type: getFileType(file.name),
            size: formatFileSize(file.size),
            uploadedAt: new Date().toISOString().split('T')[0]
          }
          
          currentFolder.value.children.push(newFile)
        }
      }
    } catch (error) {
      console.error('上传文件失败:', error)
      // 如果后端上传失败，使用前端模拟数据
      for (let i = 0; i < fileInput.files.length; i++) {
        const file = fileInput.files[i]
        const newFile = {
          id: 'file_' + Date.now() + i,
          name: file.name,
          type: getFileType(file.name),
          size: formatFileSize(file.size),
          uploadedAt: new Date().toISOString().split('T')[0]
        }
        
        currentFolder.value.children.push(newFile)
      }
    }
  }
  showUploadFile.value = false
}

// 删除节点
const deleteNode = async (node) => {
  if (confirm('确定要删除 ' + node.name + ' 吗？')) {
    try {
      const token = sessionStorage.getItem('token')
      const response = await fetch(`/api/files/${node.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
        }
      })
      
      if (response.ok) {
        // 后端删除成功后，更新前端数据
        const removeFromFolder = (nodes) => {
          for (let i = 0; i < nodes.length; i++) {
            if (nodes[i].id === node.id) {
              nodes.splice(i, 1)
              return true
            }
            if (nodes[i].children && removeFromFolder(nodes[i].children)) {
              return true
            }
          }
          return false
        }
        
        if (node.id === 'root') {
          return // 不能删除根目录
        } else if (findParent(node.id) === null) {
          // 根目录的直接子节点
          removeFromFolder(rootFolder.value.children)
        } else {
          removeFromFolder(rootFolder.value.children)
        }
      }
    } catch (error) {
      console.error('删除节点失败:', error)
      // 如果后端删除失败，使用前端模拟数据
      const removeFromFolder = (nodes) => {
        for (let i = 0; i < nodes.length; i++) {
          if (nodes[i].id === node.id) {
            nodes.splice(i, 1)
            return true
          }
          if (nodes[i].children && removeFromFolder(nodes[i].children)) {
            return true
          }
        }
        return false
      }
      
      if (node.id === 'root') {
        return // 不能删除根目录
      } else if (findParent(node.id) === null) {
        // 根目录的直接子节点
        removeFromFolder(rootFolder.value.children)
      } else {
        removeFromFolder(rootFolder.value.children)
      }
    }
  }
}

// 删除文件
const deleteFile = async (fileId) => {
  if (confirm('确定要删除该文件吗？')) {
    try {
      const token = sessionStorage.getItem('token')
      const response = await fetch(`/api/files/${fileId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
        }
      })
      
      if (response.ok) {
        // 后端删除成功后，更新前端数据
        currentFolder.value.children = currentFolder.value.children.filter(
          item => item.id !== fileId
        )
      }
    } catch (error) {
      console.error('删除文件失败:', error)
      // 如果后端删除失败，使用前端模拟数据
      currentFolder.value.children = currentFolder.value.children.filter(
        item => item.id !== fileId
      )
    }
  }
}

// 获取文件类型
const getFileType = (fileName) => {
  const extension = fileName.split('.').pop().toLowerCase()
  const docExtensions = ['doc', 'docx', 'txt', 'pdf']
  const imgExtensions = ['jpg', 'jpeg', 'png', 'gif']
  const excelExtensions = ['xls', 'xlsx']
  const pptExtensions = ['ppt', 'pptx']
  
  if (docExtensions.includes(extension)) return 'document'
  if (imgExtensions.includes(extension)) return 'image'
  if (excelExtensions.includes(extension)) return 'excel'
  if (pptExtensions.includes(extension)) return 'ppt'
  return 'file'
}

// 获取文件图标
const getFileIcon = (type) => {
  const icons = {
    document: '📄',
    image: '🖼️',
    excel: '📊',
    ppt: '📺',
    file: '📑'
  }
  return icons[type] || '📑'
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + 'B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + 'KB'
  return (bytes / (1024 * 1024)).toFixed(1) + 'MB'
}
</script>

<style scoped>
/* 文件管理页面 - 马卡龙风格 */
.file-management {
  padding: 0;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
}

.file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.file-header h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.file-content {
  display: flex;
  gap: 24px;
  height: calc(100vh - 250px);
}

.file-tree {
  width: 300px;
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  overflow-y: auto;
  position: relative;
}

.file-tree::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #A8E6CF, #7DD3C0);
  border-radius: 20px 20px 0 0;
}

.file-tree h4 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
}

.tree {
  list-style: none;
  padding: 0;
}

.tree-node {
  margin-bottom: 4px;
}

.tree-node-content {
  display: flex;
  align-items: center;
  padding: 12px 14px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tree-node-content:hover {
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.2), rgba(168, 230, 207, 0.1));
}

.tree-icon {
  margin-right: 10px;
  font-size: 18px;
}

.tree-label {
  flex: 1;
  font-size: 14px;
  color: #5D5A6D;
  font-weight: 500;
}

.tree-node-actions {
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tree-node-content:hover .tree-node-actions {
  opacity: 1;
}

.tree-action-btn {
  background: rgba(168, 230, 207, 0.2);
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 4px 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.tree-action-btn:hover {
  background: rgba(168, 230, 207, 0.4);
}

.tree-children {
  list-style: none;
  padding-left: 28px;
  margin-top: 4px;
}

.file-list {
  flex: 1;
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  overflow-y: auto;
  position: relative;
}

.file-list::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #FF9A8B, #FFB7B2);
  border-radius: 20px 20px 0 0;
}

.file-list h4 {
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  border-bottom: 1px solid #F0E6E3;
}

.empty-state {
  text-align: center;
  padding: 60px 30px;
  color: #8B8899;
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.05), rgba(255, 154, 139, 0.05));
  border-radius: 16px;
  border: 2px dashed #F0E6E3;
  font-size: 14px;
}

.files {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.file-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 16px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.05), rgba(195, 177, 225, 0.05));
  border: 1px solid #F0E6E3;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.file-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  border-color: #A8E6CF;
}

.file-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.file-info {
  flex: 1;
  width: 100%;
}

.file-name {
  font-weight: 600;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #5D5A6D;
  font-size: 13px;
}

.file-meta {
  font-size: 11px;
  color: #8B8899;
  display: flex;
  justify-content: center;
  gap: 8px;
}

.file-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

/* 弹窗样式 - 马卡龙风格 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(93, 90, 109, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 20px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border: 1px solid #F0E6E3;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.1), rgba(255, 154, 139, 0.1));
}

.modal-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #5D5A6D;
}

.close-btn {
  background: rgba(255, 154, 139, 0.1);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 20px;
  color: #FF9A8B;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 154, 139, 0.2);
  transform: rotate(90deg);
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #5D5A6D;
  font-size: 13px;
}

.form-control {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #F0E6E3;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
  color: #5D5A6D;
}

.form-control:focus {
  outline: none;
  border-color: #A8E6CF;
  box-shadow: 0 0 0 3px rgba(168, 230, 207, 0.2);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.05), rgba(195, 177, 225, 0.05));
}

/* 按钮样式 - 使用全局马卡龙样式 */
.btn-sm {
  padding: 6px 14px;
  font-size: 12px;
  border-radius: 10px;
}
</style>
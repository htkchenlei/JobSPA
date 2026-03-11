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
.file-management {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.file-content {
  display: flex;
  gap: 20px;
  height: calc(100vh - 250px);
}

.file-tree {
  width: 300px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 15px;
  overflow-y: auto;
}

.file-tree h4 {
  margin-top: 0;
  margin-bottom: 15px;
}

.tree {
  list-style: none;
  padding: 0;
}

.tree-node {
  margin-bottom: 5px;
}

.tree-node-content {
  display: flex;
  align-items: center;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
}

.tree-node-content:hover {
  background-color: #f8f9fa;
}

.tree-icon {
  margin-right: 10px;
  font-size: 16px;
}

.tree-label {
  flex: 1;
}

.tree-node-actions {
  display: flex;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.2s;
}

.tree-node-content:hover .tree-node-actions {
  opacity: 1;
}

.tree-action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 2px;
}

.tree-children {
  list-style: none;
  padding-left: 25px;
  margin-top: 5px;
}

.file-list {
  flex: 1;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 15px;
  overflow-y: auto;
}

.file-list h4 {
  margin-top: 0;
  margin-bottom: 15px;
  padding-bottom: 5px;
  border-bottom: 1px solid #e9ecef;
}

.empty-state {
  text-align: center;
  padding: 50px;
  color: #6c757d;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.files {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.file-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  background-color: #f8f9fa;
  text-align: center;
}

.file-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.file-info {
  flex: 1;
  width: 100%;
}

.file-name {
  font-weight: 500;
  margin-bottom: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  font-size: 12px;
  color: #6c757d;
}

.file-actions {
  margin-top: 10px;
  display: flex;
  gap: 5px;
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
  width: 400px;
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

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-info {
  background-color: #17a2b8;
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
  padding: 4px 8px;
  font-size: 12px;
}

.btn-primary:hover {
  background-color: #0069d9;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-info:hover {
  background-color: #138496;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
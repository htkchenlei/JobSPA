<template>
  <div class="todos">
    <h3>待办事项</h3>
    
    <div class="todos-container">
      <!-- 左侧：待办事项 -->
      <div class="todo-column pending-column">
        <h4>待完成</h4>
        
        <!-- 现有待办事项 -->
        <div class="pending-list">
          <div v-if="pendingTodos.length === 0" class="empty-state">
            暂无待办事项
          </div>
          <ul v-else class="todo-items">
            <li v-for="todo in pendingTodos" :key="todo.id" class="todo-item">
              <div class="todo-content">
                <input type="checkbox" :checked="todo.is_finished" @change="toggleTodo(todo.id)" />
                <div class="todo-info">
                  <div class="todo-title">{{ todo.item }}</div>
                  <div class="todo-meta">
                    <span class="todo-date">{{ todo.create_at }}</span>
                  </div>
                </div>
              </div>
              <div class="todo-actions">
                <button class="btn btn-sm btn-info" @click="editTodo(todo)">编辑</button>
                <button class="btn btn-sm btn-danger" @click="deleteTodo(todo.id)">删除</button>
              </div>
            </li>
          </ul>
        </div>
        
        <!-- 新增待办事项输入框 -->
        <div class="add-todo-form">
          <h5>添加新待办</h5>
          <form @submit.prevent="addNewTodo">
            <div class="form-row">
              <div class="form-group">
                <textarea v-model="newTodoItem" placeholder="输入待办事项描述" class="form-control" rows="3" required></textarea>
              </div>
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">添加</button>
              </div>
            </div>
          </form>
        </div>
      </div>
      
      <!-- 右侧：已完成事项 -->
      <div class="todo-column completed-column">
        <h4>已完成</h4>
        <div class="completed-list">
          <div v-if="completedTodos.length === 0" class="empty-state">
            暂无已完成事项
          </div>
          <ul v-else class="todo-items completed">
            <li v-for="todo in completedTodos" :key="todo.id" class="todo-item">
              <div class="todo-content">
                <input type="checkbox" :checked="todo.is_finished" @change="confirmUndo(todo.id)" />
                <div class="todo-info">
                    <div class="todo-title">{{ todo.item }}</div>
                    <div class="todo-meta">
                      <span class="todo-date">{{ todo.create_at }}</span>
                      <span class="todo-completed-date">完成于: {{ todo.finish_at }}</span>
                    </div>
                  </div>
              </div>
              <div class="todo-actions">
                <button class="btn btn-sm btn-secondary" @click="confirmUndo(todo.id)">撤销</button>
                <button class="btn btn-sm btn-danger" @click="deleteTodo(todo.id)">删除</button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- 编辑待办弹窗 -->
    <div v-if="showEditTodo" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h4>编辑待办</h4>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveTodo">
            <div class="form-group">
              <label>待办事项</label>
              <textarea v-model="todoForm.item" class="form-control" rows="4" required></textarea>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">取消</button>
              <button type="submit" class="btn btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

// 待办数据
interface Todo {
  id: number
  item: string
  is_finished: boolean
  create_at: string
  finish_at: string | null
}

const todos = ref<Todo[]>([])

// 弹窗状态
const showEditTodo = ref(false)

// 表单数据
const todoForm = ref({
  id: 0,
  item: ''
})

// 新待办事项输入
const newTodoItem = ref('')

// 待完成列表
const pendingTodos = computed(() => {
  return todos.value.filter(todo => !todo.is_finished)
})

// 已完成列表
const completedTodos = computed(() => {
  return todos.value.filter(todo => todo.is_finished)
})

// 从后端获取待办事项
const fetchTodos = async () => {
  try {
    const token = sessionStorage.getItem('token')
    console.log('Fetching todos with token:', token)
    
    if (!token) {
      console.error('No token found, please login first')
      // 可以在这里添加提示，让用户登录
      return
    }
    
    const response = await fetch('/api/todos/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    console.log('Todo API response status:', response.status)
    if (response.ok) {
      const data = await response.json()
      console.log('Todo API response data:', data)
      todos.value = data
    } else {
      const errorData = await response.json()
      console.error('Todo API error:', errorData)
    }
  } catch (error) {
    console.error('获取待办事项失败:', error)
  }
}

// 打开编辑待办弹窗
const editTodo = (todo: Todo) => {
  todoForm.value = { ...todo }
  showEditTodo.value = true
}

// 关闭弹窗
const closeModal = () => {
  showEditTodo.value = false
  todoForm.value = {
    id: 0,
    item: ''
  }
}

// 保存待办
const saveTodo = async () => {
  if (showEditTodo.value) {
    try {
      const token = sessionStorage.getItem('token')
      const response = await fetch(`/api/todos/${todoForm.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({ item: todoForm.value.item })
      })
      if (response.ok) {
        await fetchTodos()
      }
    } catch (error) {
      console.error('更新待办事项失败:', error)
    }
  }
  closeModal()
}

// 切换待办状态
const toggleTodo = async (id: number) => {
  try {
    const token = sessionStorage.getItem('token')
    const response = await fetch(`/api/todos/${id}/complete`, {
      method: 'POST',
      headers: {
        'Authorization': token ? `Bearer ${token}` : ''
      }
    })
    if (response.ok) {
      await fetchTodos()
    }
  } catch (error) {
    console.error('标记待办事项完成失败:', error)
  }
}

// 确认撤销待办
const confirmUndo = async (id: number) => {
  if (confirm('确定要撤销这个已完成的待办事项吗？')) {
    try {
      const token = sessionStorage.getItem('token')
      const response = await fetch(`/api/todos/${id}/uncomplete`, {
        method: 'POST',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
        }
      })
      if (response.ok) {
        await fetchTodos()
      }
    } catch (error) {
      console.error('撤销待办事项失败:', error)
    }
  }
}

// 添加新待办
const addNewTodo = async () => {
  try {
    const token = sessionStorage.getItem('token')
    const response = await fetch('/api/todos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify({ item: newTodoItem.value })
    })
    if (response.ok) {
      await fetchTodos()
      // 清空输入框
      newTodoItem.value = ''
    }
  } catch (error) {
    console.error('添加待办事项失败:', error)
  }
}

// 删除待办
const deleteTodo = async (id: number) => {
  if (confirm('确定要删除这个待办事项吗？')) {
    try {
      const token = sessionStorage.getItem('token')
      const response = await fetch(`/api/todos/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
        }
      })
      if (response.ok) {
        await fetchTodos()
      }
    } catch (error) {
      console.error('删除待办事项失败:', error)
    }
  }
}



// 初始化
onMounted(async () => {
  await fetchTodos()
})
</script>

<style scoped>
/* 待办事项页面 - 马卡龙风格 */
.todos {
  padding: 0;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.todos h3 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
}

.todos-container {
  display: flex;
  gap: 24px;
  flex: 1;
  overflow: hidden;
}

.todo-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  overflow: hidden;
}

.todo-column h4 {
  margin: 0;
  padding: 20px 24px;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  border-bottom: 1px solid #F0E6E3;
}

/* 左侧待办事项 */
.pending-column {
  position: relative;
}

.pending-column::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #A8E6CF, #7DD3C0);
  border-radius: 20px 20px 0 0;
}

.pending-column h4 {
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.15), rgba(168, 230, 207, 0.05));
}

.pending-list {
  flex: 0 0 60%;
  padding: 20px;
  overflow-y: auto;
}

.add-todo-form {
  padding: 20px;
  border-top: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.05), rgba(255, 154, 139, 0.05));
  display: flex;
  flex-direction: column;
  min-height: 200px;
  flex: 0 0 40%;
}

.add-todo-form form {
  display: flex;
  flex-direction: column;
}

.add-todo-form h5 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 14px;
  font-weight: 600;
  color: #5D5A6D;
}

/* 右侧已完成事项 */
.completed-column {
  position: relative;
}

.completed-column::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #C3B1E1, #B19FD0);
  border-radius: 20px 20px 0 0;
}

.completed-column h4 {
  background: linear-gradient(90deg, rgba(195, 177, 225, 0.15), rgba(195, 177, 225, 0.05));
}

.completed-list {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #8B8899;
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.05), rgba(195, 177, 225, 0.05));
  border-radius: 16px;
  border: 2px dashed #F0E6E3;
  font-size: 14px;
}

.todo-items {
  list-style: none;
  padding: 0;
  margin: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 12px;
  background: white;
  border: 1px solid #F0E6E3;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.todo-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  border-color: #A8E6CF;
}

.todo-content {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.todo-content input[type="checkbox"] {
  margin-top: 4px;
  transform: scale(1.2);
  accent-color: #A8E6CF;
}

.todo-info {
  flex: 1;
}

.todo-title {
  font-weight: 500;
  margin-bottom: 6px;
  color: #5D5A6D;
}

.todo-description {
  color: #8B8899;
  font-size: 13px;
  margin-bottom: 8px;
}

.todo-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #8B8899;
  flex-wrap: wrap;
}

.todo-priority {
  padding: 3px 10px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 11px;
}

.todo-priority.low {
  background: linear-gradient(135deg, #A8E6CF, #7DD3C0);
  color: white;
}

.todo-priority.medium {
  background: linear-gradient(135deg, #FFEAA7, #FDCB6E);
  color: #5D5A6D;
}

.todo-priority.high {
  background: linear-gradient(135deg, #FF9A8B, #FFB7B2);
  color: white;
}

.todo-actions {
  display: flex;
  gap: 8px;
}

.todo-items.completed .todo-item {
  background: linear-gradient(135deg, rgba(195, 177, 225, 0.1), rgba(195, 177, 225, 0.05));
  opacity: 0.8;
}

.todo-items.completed .todo-title {
  text-decoration: line-through;
  color: #8B8899;
}

.todo-completed-date {
  font-size: 12px;
  color: #C3B1E1;
}

/* 表单样式 */
.form-group {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
}

.form-control {
  width: 100%;
  padding: 12px 14px;
  border: 2px solid #F0E6E3;
  border-radius: 12px;
  font-size: 14px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  background: white;
  color: #5D5A6D;
  flex: 1;
  resize: none;
}

.form-control:focus {
  outline: none;
  border-color: #A8E6CF;
  box-shadow: 0 0 0 3px rgba(168, 230, 207, 0.2);
}

.form-row {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.form-group {
  flex: 1;
  margin-bottom: 0;
  display: flex;
  flex-direction: column;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
  min-height: 40px;
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
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.1), rgba(195, 177, 225, 0.1));
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

.modal-body .form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #5D5A6D;
  font-size: 13px;
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
.btn {
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
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

.btn-sm {
  padding: 6px 14px;
  font-size: 12px;
  border-radius: 10px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .todos-container {
    flex-direction: column;
  }
  
  .pending-list {
    flex: 0 0 60%;
  }
  
  .add-todo-form {
    flex: 0 0 40%;
  }
}
</style>
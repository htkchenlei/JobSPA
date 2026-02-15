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
            <div class="form-group">
              <textarea v-model="newTodoItem" placeholder="输入待办事项描述" class="form-control" rows="3" required></textarea>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">添加</button>
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
    const token = localStorage.getItem('token')
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
      const token = localStorage.getItem('token')
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
    const token = localStorage.getItem('token')
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
      const token = localStorage.getItem('token')
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
    const token = localStorage.getItem('token')
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
      const token = localStorage.getItem('token')
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
.todos {
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.todos h3 {
  margin-top: 0;
  margin-bottom: 20px;
}

.todos-container {
  display: flex;
  gap: 20px;
  flex: 1;
  overflow: hidden;
}

.todo-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f8f9fa;
}

.todo-column h4 {
  margin: 0;
  padding: 15px;
  background-color: #e9ecef;
  border-bottom: 1px solid #dee2e6;
  font-size: 16px;
  font-weight: 600;
}

/* 左侧待办事项 */
.pending-column {
  display: flex;
  flex-direction: column;
}

.pending-list {
  flex: 0 0 60%;
  padding: 15px;
  overflow-y: auto;
}

.add-todo-form {
  flex: 0 0 50%;
  padding: 15px;
  border-top: 1px solid #e9ecef;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  min-height: 200px;
}

.add-todo-form form {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.add-todo-form h5 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 14px;
  font-weight: 600;
}

/* 右侧已完成事项 */
.completed-column {
  display: flex;
  flex-direction: column;
}

.completed-list {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: #6c757d;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #e9ecef;
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
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  margin-bottom: 10px;
  background-color: #ffffff;
}

.todo-item:hover {
  background-color: #f8f9fa;
}

.todo-content {
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.todo-content input[type="checkbox"] {
  margin-top: 5px;
  transform: scale(1.2);
}

.todo-info {
  flex: 1;
}

.todo-title {
  font-weight: 500;
  margin-bottom: 5px;
}

.todo-description {
  color: #6c757d;
  font-size: 14px;
  margin-bottom: 10px;
}

.todo-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #6c757d;
  flex-wrap: wrap;
}

.todo-priority {
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.todo-priority.low {
  background-color: #d4edda;
  color: #155724;
}

.todo-priority.medium {
  background-color: #fff3cd;
  color: #856404;
}

.todo-priority.high {
  background-color: #f8d7da;
  color: #721c24;
}

.todo-actions {
  display: flex;
  gap: 5px;
}

.todo-items.completed .todo-item {
  background-color: #e7f3ff;
  opacity: 0.8;
}

.todo-items.completed .todo-title {
  text-decoration: line-through;
}

.todo-completed-date {
  font-size: 12px;
  color: #6c757d;
}

/* 表单样式 */
.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  flex-shrink: 0;
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

.modal-body .form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
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

.btn-info:hover {
  background-color: #138496;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-secondary:hover {
  background-color: #5a6268;
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
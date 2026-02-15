<template>
  <div class="login-container">
    <div class="login-form">
      <h2>
        <img src="/workspace.svg" alt="Logo" class="logo-icon">
        JobSPA 登录
      </h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="loginForm.username" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="loginForm.password" class="form-control" required>
        </div>
        <div class="form-group buttons-group">
          <button type="submit" class="btn btn-primary">登录</button>
          <button type="button" class="btn btn-secondary" @click="resetForm">取消</button>
        </div>
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loginForm = ref({
  username: '',
  password: ''
})
const error = ref('')

const login = async () => {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginForm.value)
    })
    
    if (response.ok) {
      const data = await response.json()
      // 存储token到localStorage
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      // 跳转到仪表板
      router.push('/dashboard')
    } else {
      const errorData = await response.json()
      error.value = errorData.error || '登录失败'
    }
  } catch (err) {
    console.error('登录失败:', err)
    error.value = '网络错误，请稍后重试'
  }
}

// 重置表单
const resetForm = () => {
  loginForm.value = {
    username: '',
    password: ''
  }
  error.value = ''
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.login-form {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.login-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.buttons-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.buttons-group .btn {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  text-align: center;
}

/* 按钮样式 */
.btn {
  border: none;
  border-radius: 4px;
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

.btn-secondary {
  background-color: #95a5a6;
  color: white;
  box-shadow: 0 2px 4px rgba(149, 165, 166, 0.3);
}

.btn-secondary:hover {
  background-color: #7f8c8d;
  box-shadow: 0 4px 8px rgba(149, 165, 166, 0.4);
}

.logo-icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  vertical-align: middle;
}
</style>
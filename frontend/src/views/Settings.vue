<template>
  <div class="change-password">
    <h1>个人设置</h1>
    
    <div class="settings-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'password' }"
        @click="activeTab = 'password'"
      >
        修改密码
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'ai' }"
        @click="activeTab = 'ai'"
      >
        AI模型设置
      </button>
    </div>
    
    <!-- 修改密码表单 -->
    <div v-if="activeTab === 'password'" class="change-password-form">
      <form @submit.prevent="submitChangePassword">
        <div class="form-group">
          <label>当前密码</label>
          <input type="password" v-model="changePasswordForm.currentPassword" class="form-control" required>
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input type="password" v-model="changePasswordForm.newPassword" class="form-control" required>
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input type="password" v-model="changePasswordForm.confirmPassword" class="form-control" required>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">保存</button>
        </div>
      </form>
    </div>
    
    <!-- AI模型设置 -->
    <div v-if="activeTab === 'ai'" class="ai-settings-form">
      <div class="form-group">
        <label>选择AI模型</label>
        <div class="model-options">
          <label v-for="model in models" :key="model.value" class="model-option">
            <input type="radio" v-model="aiForm.defaultModel" :value="model.value">
            <span>{{ model.label }}</span>
          </label>
        </div>
      </div>
      
      <div class="model-apis">
        <h4>API密钥设置</h4>
        
        <div v-if="aiForm.defaultModel === 'deepseek'" class="form-group">
          <label>DeepSeek API密钥</label>
          <input type="password" v-model="aiForm.apiKeys.deepseek" class="form-control" placeholder="输入DeepSeek API密钥" required>
          <small class="form-text text-muted">从 https://www.deepseek.com/ 获取API密钥</small>
        </div>
        
        <div v-if="aiForm.defaultModel === 'qwen'" class="form-group">
          <label>Qwen API密钥</label>
          <input type="password" v-model="aiForm.apiKeys.qwen" class="form-control" placeholder="输入Qwen API密钥" required>
          <small class="form-text text-muted">从 https://dashscope.aliyun.com/ 获取API密钥</small>
        </div>
        
        <div v-if="aiForm.defaultModel === 'doubao'" class="form-group">
          <label>Doubao API密钥</label>
          <input type="password" v-model="aiForm.apiKeys.doubao" class="form-control" placeholder="输入Doubao API密钥" required>
          <small class="form-text text-muted">从 https://console.volcengine.com/ark/ 获取API密钥</small>
        </div>
      </div>
      
      <div class="form-actions">
        <button class="btn btn-primary" @click="updateAiSettings">保存设置</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 当前激活的标签
const activeTab = ref('password')

// 修改密码表单
const changePasswordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 模型列表
const models = [
  { value: 'deepseek', label: 'DeepSeek' },
  { value: 'qwen', label: 'Qwen' },
  { value: 'doubao', label: 'Doubao' }
]

// AI模型设置表单
const aiForm = ref({
  defaultModel: 'deepseek',
  apiKeys: {
    deepseek: '',
    qwen: '',
    doubao: ''
  }
})

// 初始化表单数据
onMounted(() => {
  // 从localStorage获取AI设置
  const aiSettingsStr = localStorage.getItem('aiSettings')
  if (aiSettingsStr) {
    aiForm.value = { ...aiForm.value, ...JSON.parse(aiSettingsStr) }
  }
})

// 提交修改密码
const submitChangePassword = async () => {
  // 验证新密码和确认密码是否一致
  if (changePasswordForm.value.newPassword !== changePasswordForm.value.confirmPassword) {
    alert('新密码和确认密码不一致')
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/auth/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify(changePasswordForm.value)
    })
    
    if (response.ok) {
      const data = await response.json()
      alert('密码修改成功')
      // 重置表单
      changePasswordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
      // 可以选择跳转回仪表盘
      // router.push('/dashboard')
    } else {
      const errorData = await response.json()
      alert(`密码修改失败: ${errorData.error}`)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    alert('修改密码失败，请稍后重试')
  }
}

// 更新AI模型设置
const updateAiSettings = () => {
  console.log('更新AI模型设置:', aiForm.value)
  localStorage.setItem('aiSettings', JSON.stringify(aiForm.value))
  alert('AI模型设置保存成功')
}
</script>

<style scoped>
.change-password {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 40px;
}

/* 标签页样式 */
.settings-tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 1px solid #e9ecef;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  color: #3498db;
}

.tab-btn.active {
  border-bottom-color: #3498db;
  color: #3498db;
  font-weight: 500;
}

/* 表单样式 */
.change-password-form,
.ai-settings-form {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
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

.form-actions {
  margin-top: 30px;
  text-align: center;
}

/* 模型API设置样式 */
.model-apis {
  margin-top: 30px;
}

.model-apis h4 {
  color: #333;
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}

.form-text {
  font-size: 12px;
  color: #6c757d;
  margin-top: 5px;
  display: block;
}

/* 模型选项样式 */
.model-options {
  display: flex;
  gap: 30px;
  margin-top: 10px;
}

.model-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.model-option input[type="radio"] {
  width: auto;
  margin: 0;
}

.model-option span {
  font-size: 14px;
  color: #555;
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
</style>
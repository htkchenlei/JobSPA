<template>
  <div class="change-password">
    <h1 class="page-title">个人设置</h1>

    <n-tabs v-model:value="activeTab" type="line" animated class="settings-tabs">
      <n-tab-pane name="password" tab="修改密码">
        <n-card class="settings-card" :bordered="false">
          <n-form
            ref="passwordFormRef"
            :model="changePasswordForm"
            :rules="passwordRules"
            label-placement="top"
          >
            <n-form-item label="当前密码" path="currentPassword">
              <n-input
                v-model:value="changePasswordForm.currentPassword"
                type="password"
                show-password-on="click"
                placeholder="请输入当前密码"
              />
            </n-form-item>
            <n-form-item label="新密码" path="newPassword">
              <n-input
                v-model:value="changePasswordForm.newPassword"
                type="password"
                show-password-on="click"
                placeholder="请输入新密码"
              />
            </n-form-item>
            <n-form-item label="确认新密码" path="confirmPassword">
              <n-input
                v-model:value="changePasswordForm.confirmPassword"
                type="password"
                show-password-on="click"
                placeholder="请再次输入新密码"
              />
            </n-form-item>
          </n-form>
          <div class="form-actions">
            <n-button class="mc-btn-coral" :loading="savingPassword" @click="submitChangePassword">保存</n-button>
          </div>
        </n-card>
      </n-tab-pane>

      <n-tab-pane name="ai" tab="AI模型设置">
        <n-card class="settings-card" :bordered="false">
          <n-form label-placement="top">
            <n-form-item label="选择AI模型">
              <n-radio-group v-model:value="aiForm.defaultModel" class="model-options">
                <n-radio-button
                  v-for="model in models"
                  :key="model.value"
                  :value="model.value"
                  class="model-option"
                >
                  {{ model.label }}
                </n-radio-button>
              </n-radio-group>
            </n-form-item>

            <n-divider title-placement="left" class="api-divider">API密钥设置</n-divider>

            <n-form-item v-if="aiForm.defaultModel === 'deepseek'" label="DeepSeek API密钥" :feedback="deepseekTip">
              <n-input
                v-model:value="aiForm.apiKeys.deepseek"
                type="password"
                show-password-on="click"
                placeholder="输入DeepSeek API密钥"
              />
            </n-form-item>

            <n-form-item v-if="aiForm.defaultModel === 'qwen'" label="Qwen API密钥" :feedback="qwenTip">
              <n-input
                v-model:value="aiForm.apiKeys.qwen"
                type="password"
                show-password-on="click"
                placeholder="输入Qwen API密钥"
              />
            </n-form-item>

            <n-form-item v-if="aiForm.defaultModel === 'doubao'" label="Doubao API密钥" :feedback="doubaoTip">
              <n-input
                v-model:value="aiForm.apiKeys.doubao"
                type="password"
                show-password-on="click"
                placeholder="输入Doubao API密钥"
              />
            </n-form-item>
          </n-form>
          <div class="form-actions">
            <n-button class="mc-btn-coral" @click="updateAiSettings">保存设置</n-button>
          </div>
        </n-card>
      </n-tab-pane>

      <n-tab-pane name="api" tab="API文档">
        <ApiDocumentation />
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NTabs, NTabPane, NCard, NForm, NFormItem, NInput,
  NButton, NRadioGroup, NRadioButton, NDivider
} from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'
import { message } from '../utils/feedback'
import ApiDocumentation from './ApiDocumentation.vue'

const router = useRouter()

// 当前激活的标签
const activeTab = ref('password')

// 修改密码表单
const changePasswordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordFormRef = ref<FormInst | null>(null)
const savingPassword = ref(false)

const passwordRules: FormRules = {
  currentPassword: { required: true, message: '请输入当前密码', trigger: ['input', 'blur'] },
  newPassword: { required: true, message: '请输入新密码', trigger: ['input', 'blur'] },
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: ['input', 'blur'] },
    {
      validator: (_rule, value: string) => {
        if (!value) return true
        return value === changePasswordForm.value.newPassword
      },
      message: '两次输入的密码不一致',
      trigger: ['input', 'blur']
    }
  ]
}

// 模型列表
const models = [
  { value: 'deepseek', label: 'DeepSeek' },
  { value: 'qwen', label: 'Qwen' },
  { value: 'doubao', label: 'Doubao' }
]

// 密钥获取提示
const deepseekTip = '从 https://www.deepseek.com/ 获取API密钥'
const qwenTip = '从 https://dashscope.aliyun.com/ 获取API密钥'
const doubaoTip = '从 https://console.volcengine.com/ark/ 获取API密钥'

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
  const aiSettingsStr = localStorage.getItem('aiSettings')
  if (aiSettingsStr) {
    try {
      aiForm.value = { ...aiForm.value, ...JSON.parse(aiSettingsStr) }
    } catch (e) {
      console.error('解析AI设置失败:', e)
    }
  }
})

// 提交修改密码
const submitChangePassword = async () => {
  try {
    await passwordFormRef.value?.validate()
  } catch {
    return
  }

  if (changePasswordForm.value.newPassword !== changePasswordForm.value.confirmPassword) {
    message.warning('新密码和确认密码不一致')
    return
  }

  savingPassword.value = true
  try {
    const token = sessionStorage.getItem('token')
    const response = await fetch('/api/auth/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      body: JSON.stringify(changePasswordForm.value)
    })

    if (response.ok) {
      await response.json()
      message.success('密码修改成功')
      changePasswordForm.value = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } else {
      const errorData = await response.json()
      message.error(`密码修改失败: ${errorData.error}`)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    message.error('修改密码失败，请稍后重试')
  } finally {
    savingPassword.value = false
  }
}

// 更新AI模型设置
const updateAiSettings = () => {
  localStorage.setItem('aiSettings', JSON.stringify(aiForm.value))
  message.success('AI模型设置保存成功')
}
</script>

<style scoped>
.change-password {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
  margin: 0 0 20px;
}

/* Tab 选中态用薰衣草紫，去蓝色叛离 */
.settings-tabs :deep(.n-tabs-nav) {
  margin-bottom: 20px;
}

.settings-tabs :deep(.n-tabs-tab) {
  font-size: 15px;
  color: #8B8899;
}

.settings-tabs :deep(.n-tabs-tab--active) {
  color: #9575C9;
  font-weight: 600;
}

.settings-tabs :deep(.n-tabs-bar) {
  background: linear-gradient(90deg, #C3B1E1, #9575C9) !important;
  border-radius: 2px;
}

.settings-card {
  border-radius: 20px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  background: rgba(255, 255, 255, 0.9);
  border-top: 4px solid #A8E6CF;
}

/* 内容区留白见全局 style.css（Naive 类名为 .n-card-content） */

.form-actions {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}

/* 模型选择：卡片化单选按钮 */
.model-options {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.model-options :deep(.n-radio-button) {
  border-radius: 12px !important;
  border: 1px solid #F0E6E3 !important;
  padding: 8px 20px;
  transition: all 0.2s ease;
}

.model-options :deep(.n-radio-button--checked) {
  border-color: #A8E6CF !important;
  background: rgba(168, 230, 207, 0.15) !important;
  color: #4A9E7F !important;
  font-weight: 600;
}

.api-divider {
  margin: 8px 0 20px;
}

.api-divider :deep(.n-divider__title) {
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 20px;
    margin-bottom: 14px;
  }

  .model-options {
    width: 100%;
  }

  .model-options :deep(.n-radio-button) {
    flex: 1;
    padding: 8px 10px;
  }
}
</style>

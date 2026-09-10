<template>
  <div class="login-page">
    <n-card class="login-card" :bordered="false">
      <div class="login-head">
        <img src="/workspace.svg" alt="Logo" class="logo-icon">
        <h2>JobSPA 登录</h2>
        <p class="login-sub">项目管理平台 · 薄荷绿马卡龙</p>
      </div>

      <n-form ref="formRef" :model="loginForm" :rules="rules">
        <n-form-item path="username" label="用户名">
          <n-input
            v-model:value="loginForm.username"
            size="large"
            placeholder="请输入用户名"
            :input-props="{ autocomplete: 'username' }"
            @keydown.enter="login"
          />
        </n-form-item>
        <n-form-item path="password" label="密码">
          <n-input
            v-model:value="loginForm.password"
            type="password"
            show-password-on="click"
            size="large"
            placeholder="请输入密码"
            :input-props="{ autocomplete: 'current-password' }"
            @keydown.enter="login"
          />
        </n-form-item>

        <div class="login-actions">
          <n-button type="primary" size="large" block :loading="loading" @click="login">登录</n-button>
          <n-button class="mc-btn-lavender" size="large" block :disabled="loading" @click="resetForm">取消</n-button>
        </div>
      </n-form>

      <n-alert v-if="error" type="error" :bordered="false" class="login-error" closable @close="error = ''">
        {{ error }}
      </n-alert>

      <p class="login-tip">默认账号请联系管理员分配</p>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NAlert, NButton, NCard, NForm, NFormItem, NInput } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'

const router = useRouter()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)
const error = ref('')

const loginForm = ref({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: { required: true, message: '请输入用户名', trigger: ['blur', 'input'] },
  password: { required: true, message: '请输入密码', trigger: ['blur', 'input'] }
}

const login = async () => {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }

  loading.value = true
  error.value = ''
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
      // 存储token到sessionStorage，关闭浏览器后自动清除
      sessionStorage.setItem('token', data.token)
      sessionStorage.setItem('user', JSON.stringify(data.user))
      router.push('/dashboard')
    } else {
      const errorData = await response.json().catch(() => null)
      error.value = errorData?.error || '登录失败'
    }
  } catch (err) {
    console.error('登录失败:', err)
    error.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}

// 重置表单
const resetForm = () => {
  loginForm.value = {
    username: '',
    password: ''
  }
  error.value = ''
  formRef.value?.restoreValidation()
}
</script>

<style scoped>
/* 登录页融入马卡龙氛围，彻底去掉原有蓝色 Bootstrap 观感 */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 24px;
  background:
    radial-gradient(1000px 500px at 15% 0%, rgba(168, 230, 207, 0.20), transparent 60%),
    radial-gradient(900px 460px at 90% 10%, rgba(255, 154, 139, 0.14), transparent 55%),
    radial-gradient(800px 420px at 50% 100%, rgba(195, 177, 225, 0.16), transparent 60%),
    var(--macaron-cream);
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 8px 8px 4px;
  border-radius: var(--radius-lg);
  box-shadow: 0 12px 40px rgba(93, 90, 109, 0.10);
  overflow: hidden;
}

.login-card::before {
  content: '';
  display: block;
  height: 4px;
  margin: -8px -8px 20px;
  background: linear-gradient(90deg, var(--macaron-mint), var(--macaron-sky));
}

.login-head {
  text-align: center;
  margin-bottom: 24px;
}

.login-head h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--macaron-text);
  margin: 0;
}

.login-sub {
  margin: 8px 0 0;
  font-size: var(--fs-sm);
  color: var(--macaron-text-light);
}

.logo-icon {
  width: 32px;
  height: 32px;
  vertical-align: middle;
  margin-right: 8px;
}

.login-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-top: var(--space-2);
}

.login-error {
  margin-top: var(--space-4);
  border-radius: var(--radius-md);
}

.login-tip {
  margin: var(--space-4) 0 0;
  text-align: center;
  font-size: var(--fs-xs);
  color: var(--macaron-text-light);
  background: rgba(195, 177, 225, 0.10);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
}

/* ==================== 移动端适配 ==================== */
@media (max-width: 480px) {
  .login-page {
    padding: 12px;
  }

  .login-card {
    max-width: 100%;
    padding: 4px;
  }

  .login-head h2 {
    font-size: 20px;
  }
}
</style>

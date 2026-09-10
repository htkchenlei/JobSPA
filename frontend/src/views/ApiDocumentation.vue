<template>
  <div class="api-documentation">
    <h2 class="api-doc-title">API接口文档</h2>

    <n-collapse :default-expanded-names="['auth']" class="api-collapse">
      <n-collapse-item v-for="group in apiGroups" :key="group.key" :name="group.key">
        <template #header>
          <span class="group-title">{{ group.title }}</span>
        </template>

        <n-card
          v-for="api in group.apis"
          :key="api.url + api.method"
          class="api-card"
          :bordered="false"
          size="small"
        >
          <template #header>
            <div class="api-head">
              <n-tag :class="methodClass(api.method)" :bordered="false" size="small" round>
                {{ api.method }}
              </n-tag>
              <span class="api-name">{{ api.title }}</span>
            </div>
          </template>

          <div class="api-details">
            <code class="api-url">{{ api.url }}</code>
            <p class="api-description">{{ api.description }}</p>

            <div v-if="api.request?.length" class="api-block">
              <h4>请求参数：</h4>
              <pre v-for="(req, i) in api.request" :key="i">{{ req }}</pre>
            </div>

            <div v-if="api.response" class="api-block">
              <h4>响应示例：</h4>
              <pre>{{ api.response }}</pre>
            </div>
          </div>
        </n-card>
      </n-collapse-item>
    </n-collapse>
  </div>
</template>

<script setup lang="ts">
import { NCard, NCollapse, NCollapseItem, NTag } from 'naive-ui'

interface ApiItem {
  title: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE'
  url: string
  description: string
  request?: string[]
  response?: string
}

interface ApiGroup {
  key: string
  title: string
  apis: ApiItem[]
}

const authHeader = 'Authorization: Bearer {token}'

const apiGroups: ApiGroup[] = [
  {
    key: 'auth',
    title: '认证相关API',
    apis: [
      {
        title: '登录',
        method: 'POST',
        url: '/api/auth/login',
        description: '用户登录接口，返回JWT token',
        request: ['{"username": "用户名", "password": "密码"}'],
        response: '{"token": "JWT token", "user": {"id": 1, "username": "用户名", "is_admin": false}}'
      },
      {
        title: '验证token',
        method: 'GET',
        url: '/api/auth/verify',
        description: '验证JWT token的有效性',
        request: [authHeader],
        response: '{"user": {"id": 1, "username": "用户名", "is_admin": false}}'
      },
      {
        title: '登出',
        method: 'POST',
        url: '/api/auth/logout',
        description: '用户登出接口',
        response: '{"message": "登出成功"}'
      },
      {
        title: '修改密码',
        method: 'POST',
        url: '/api/auth/change-password',
        description: '修改用户密码',
        request: [authHeader, '{"currentPassword": "当前密码", "newPassword": "新密码"}'],
        response: '{"message": "密码修改成功"}'
      }
    ]
  },
  {
    key: 'users',
    title: '用户相关API',
    apis: [
      {
        title: '获取用户列表',
        method: 'GET',
        url: '/api/users/',
        description: '获取所有用户列表',
        request: [authHeader],
        response: '[{"id": 1, "username": "用户名"}]'
      }
    ]
  },
  {
    key: 'projects',
    title: '项目相关API',
    apis: [
      {
        title: '获取项目列表',
        method: 'GET',
        url: '/api/projects/',
        description: '获取所有未删除的项目列表',
        request: [authHeader],
        response: '[{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}]'
      },
      {
        title: '获取单个项目',
        method: 'GET',
        url: '/api/projects/{id}',
        description: '获取单个项目的详细信息',
        request: [authHeader],
        response: '{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}'
      },
      {
        title: '创建项目',
        method: 'POST',
        url: '/api/projects/',
        description: '创建新项目',
        request: [authHeader, '{"name": "项目名称", "client_name": "客户名称", "stage": 1}'],
        response: '{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}'
      },
      {
        title: '更新项目',
        method: 'PUT',
        url: '/api/projects/{id}',
        description: '更新项目信息',
        request: [authHeader, '{"name": "项目名称", "client_name": "客户名称", "stage": 2}'],
        response: '{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 2, "stage_text": "已立项"}'
      },
      {
        title: '更新项目进度',
        method: 'POST',
        url: '/api/projects/{id}/progress',
        description: '更新项目进度信息',
        request: [authHeader, '{"update_content": "进度内容", "stage": 3, "updated_by": "更新人"}'],
        response: '{"id": 1, "stage": 3, "stage_text": "已立项", "message": "项目进度更新成功"}'
      },
      {
        title: '获取项目进度历史',
        method: 'GET',
        url: '/api/projects/{id}/progress',
        description: '获取项目的进度历史记录',
        request: [authHeader],
        response: '[{"id": 1, "update_content": "进度内容", "update_date": "2024-01-01", "update_time": "12:00:00", "updated_by": "更新人"}]'
      },
      {
        title: '删除项目',
        method: 'DELETE',
        url: '/api/projects/{id}',
        description: '软删除项目',
        request: [authHeader],
        response: '{"message": "项目删除成功"}'
      },
      {
        title: '获取项目阶段列表',
        method: 'GET',
        url: '/api/projects/stages',
        description: '获取所有项目阶段列表',
        request: [authHeader],
        response: '[{"value": 1, "label": "立项中"}, {"value": 2, "label": "已立项"}, {"value": 3, "label": "招投标"}, {"value": 4, "label": "已中标"}, {"value": 5, "label": "已完成"}]'
      },
      {
        title: '搜索项目',
        method: 'POST',
        url: '/api/projects/search',
        description: '根据关键词搜索项目',
        request: [authHeader, '{"keywords": "关键词", "start_date": "开始日期", "end_date": "结束日期"}'],
        response: '[{"id": 1, "name": "项目名称", "client_name": "客户名称", "stage": 1, "stage_text": "立项中"}]'
      }
    ]
  },
  {
    key: 'worklog',
    title: '工作日志相关API',
    apis: [
      {
        title: '获取所有工作日志',
        method: 'GET',
        url: '/api/work-log/',
        description: '获取所有工作日志',
        request: [authHeader],
        response: '[{"id": 1, "today_activities": "活动记录", "user": 1, "work_log_by_ai": "AI生成的工作日志", "log_date": "2024-01-01", "log_time": "12:00:00", "created_by_ai": "DeepSeek"}]'
      },
      {
        title: '获取用户的工作日志',
        method: 'GET',
        url: '/api/work-log/user/{user_id}',
        description: '获取指定用户的所有工作日志',
        request: [authHeader],
        response: '[{"id": 1, "today_activities": "活动记录", "user": 1, "work_log_by_ai": "AI生成的工作日志", "log_date": "2024-01-01", "log_time": "12:00:00", "created_by_ai": "DeepSeek"}]'
      },
      {
        title: '获取指定日期的工作日志',
        method: 'GET',
        url: '/api/work-log/date/{log_date}',
        description: '获取指定日期的工作日志',
        request: [authHeader],
        response: '{"id": 1, "today_activities": "活动记录", "user": 1, "work_log_by_ai": "AI生成的工作日志", "log_date": "2024-01-01", "log_time": "12:00:00", "created_by_ai": "DeepSeek"}'
      },
      {
        title: '生成今日活动记录',
        method: 'POST',
        url: '/api/work-log/generate-activities',
        description: '生成今日的活动记录',
        request: [authHeader, '{"user_id": 1}'],
        response: '{"activities": ["活动1", "活动2", "活动3"]}'
      },
      {
        title: '保存工作日志',
        method: 'POST',
        url: '/api/work-log/save',
        description: '保存工作日志',
        request: [authHeader, '{"user_id": 1, "work_log_by_ai": "AI生成的工作日志"}'],
        response: '{"message": "工作日志保存成功"}'
      },
      {
        title: '获取今日活动记录',
        method: 'GET',
        url: '/api/work-log/today-activities',
        description: '获取今日的活动记录',
        request: [authHeader],
        response: '["活动1", "活动2", "活动3"]'
      }
    ]
  },
  {
    key: 'ai',
    title: 'AI相关API',
    apis: [
      {
        title: '生成AI内容',
        method: 'POST',
        url: '/api/ai/generate',
        description: '调用大模型生成内容',
        request: [authHeader, '{"model": "deepseek", "prompt": "提示词", "max_tokens": 500}'],
        response: '{"content": "AI生成的内容"}'
      }
    ]
  }
]

/** GET=天蓝、POST=薄荷绿、PUT=柠檬黄、DELETE=珊瑚红 */
const methodClass = (method: string) => {
  switch (method) {
    case 'GET':
      return 'mc-method-get'
    case 'POST':
      return 'mc-method-post'
    case 'PUT':
      return 'mc-method-put'
    default:
      return 'mc-method-delete'
  }
}
</script>

<style scoped>
.api-documentation {
  max-width: 1100px;
  margin: 0 auto;
}

.api-doc-title {
  font-size: 20px;
  font-weight: 700;
  color: #5D5A6D;
  margin: 0 0 16px;
}

.api-collapse :deep(.n-collapse-item__header) {
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
}

.group-title {
  color: #5D5A6D;
}

.api-card {
  border-radius: 16px !important;
  border: 1px solid #F0E6E3;
  background: rgba(255, 255, 255, 0.9);
  margin-bottom: 14px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
}

/* 内容区留白见全局 style.css（Naive 类名为 .n-card-content） */

.api-card :deep(.n-card-header) {
  padding: 14px 20px 0;
}

.api-head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.api-name {
  font-size: 15px;
  font-weight: 600;
  color: #5D5A6D;
}

:deep(.mc-method-get) {
  background: rgba(126, 200, 227, 0.18) !important;
  color: #3E93B3 !important;
  font-weight: 700;
}

:deep(.mc-method-post) {
  background: rgba(168, 230, 207, 0.22) !important;
  color: #4A9E7F !important;
  font-weight: 700;
}

:deep(.mc-method-put) {
  background: rgba(255, 234, 167, 0.32) !important;
  color: #B98B12 !important;
  font-weight: 700;
}

:deep(.mc-method-delete) {
  background: rgba(255, 154, 139, 0.2) !important;
  color: #D35D6E !important;
  font-weight: 700;
}

.api-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.api-url {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: 13px;
  color: #5D5A6D;
  background: #FBF5F1;
  border: 1px solid #F0E6E3;
  padding: 8px 12px;
  border-radius: 8px;
  overflow-wrap: anywhere;
}

.api-description {
  color: #8B8899;
  font-size: 13px;
  margin: 0;
}

.api-block h4 {
  margin: 0 0 6px;
  color: #5D5A6D;
  font-size: 13px;
  font-weight: 600;
}

.api-block pre {
  background: #FBF5F1;
  border: 1px solid #F0E6E3;
  padding: 10px 12px;
  border-radius: 8px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
  font-size: 12.5px;
  line-height: 1.6;
  overflow-x: auto;
  margin: 0 0 8px;
  color: #5D5A6D;
}

@media (max-width: 768px) {
  .api-url,
  .api-block pre {
    font-size: 12px;
  }
}
</style>

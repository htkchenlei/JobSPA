<template>
  <div class="logs">
    <h3 class="page-title">日志查询</h3>

    <n-card class="logs-card" :bordered="false">
      <div class="logs-filter">
        <div class="form-group">
          <label>日志类型</label>
          <n-select v-model:value="logType" :options="logTypeOptions" placeholder="全部" />
        </div>
        <div class="form-group">
          <label>时间范围</label>
          <div class="date-range">
            <n-date-picker v-model:formatted-value="startDate" value-format="yyyy-MM-dd" type="date" placeholder="开始日期" />
            <span>至</span>
            <n-date-picker v-model:formatted-value="endDate" value-format="yyyy-MM-dd" type="date" placeholder="结束日期" />
          </div>
        </div>
        <div class="form-group">
          <label>关键词</label>
          <n-input v-model:value="keyword" placeholder="输入关键词" clearable />
        </div>
        <n-button class="mc-btn-coral" @click="handleSearch">查询</n-button>
      </div>

      <n-data-table
        :columns="columns"
        :data="logs"
        :bordered="false"
        :single-line="false"
        size="small"
        :scroll-x="760"
      />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NSelect, NDatePicker, NInput, NButton, NDataTable } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'

interface LogItem {
  time: string
  type: string
  operator: string
  content: string
  ip: string
}

const logType = ref('')
// n-date-picker 的"未选择"必须是 null，传 '' 会在内部 formatDate('')
// 时抛 RangeError: Invalid time value 导致整页白屏
const startDate = ref<string | null>(null)
const endDate = ref<string | null>(null)
const keyword = ref('')

const logTypeOptions = [
  { label: '全部', value: '' },
  { label: '项目操作', value: 'project' },
  { label: '待办操作', value: 'todo' },
  { label: '文件操作', value: 'file' },
  { label: '用户操作', value: 'user' }
]

const logs = ref<LogItem[]>([
  { time: '2026-01-01 10:00:00', type: '项目操作', operator: 'Admin', content: '创建项目 "企业官网建设"', ip: '127.0.0.1' },
  { time: '2026-01-01 10:30:00', type: '项目操作', operator: 'Admin', content: '更新项目 "企业官网建设" 状态为 "项目立项"', ip: '127.0.0.1' },
  { time: '2026-01-01 11:00:00', type: '待办操作', operator: 'Admin', content: '创建待办事项 "完成项目方案"', ip: '127.0.0.1' },
  { time: '2026-01-01 11:30:00', type: '文件操作', operator: 'Admin', content: '上传文件 "项目方案.docx"', ip: '127.0.0.1' }
])

const columns: DataTableColumns<LogItem> = [
  { title: '时间', key: 'time', width: 170 },
  { title: '类型', key: 'type', width: 110 },
  { title: '操作人', key: 'operator', width: 100 },
  { title: '操作内容', key: 'content', minWidth: 220, ellipsis: { tooltip: true } },
  { title: 'IP地址', key: 'ip', width: 130 }
]

const handleSearch = () => {
  // 该页面当前为静态演示数据，保留原有行为
  console.log('查询日志', {
    logType: logType.value,
    startDate: startDate.value,
    endDate: endDate.value,
    keyword: keyword.value
  })
}
</script>

<style scoped>
.logs {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #5D5A6D;
  margin: 0 0 20px;
}

.logs-card {
  border-radius: 20px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid #F0E6E3;
  background: rgba(255, 255, 255, 0.9);
  border-top: 4px solid #7EC8E3;
}

/* 内容区留白见全局 style.css（Naive 类名为 .n-card-content） */

.logs-filter {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  font-size: 13px;
  color: #5D5A6D;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-range :deep(.n-date-picker) {
  flex: 1;
  min-width: 0;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 20px;
  }

  .form-group {
    min-width: 100%;
  }
}
</style>

<template>
  <n-card
    class="project-card"
    :class="stageMeta.className"
    :bordered="true"
    size="small"
  >
    <template #header>
      <div class="project-card-header">
        <h4 class="project-name" :title="project.name">{{ project.name }}</h4>
        <n-tag
          class="status-badge mc-stage-tag"
          :class="stageMeta.className"
          :bordered="false"
          size="small"
          round
        >
          {{ project.stage_text || stageMeta.label }}
        </n-tag>
      </div>
    </template>

    <div class="project-card-body">
      <div class="project-info">
        <div class="info-item">
          <label>规模：</label>
          <span>{{ project.scale || '未设置' }}</span>
        </div>
        <div class="info-item">
          <label>阶段：</label>
          <span>{{ project.stage_text || stageMeta.label }}</span>
        </div>
        <div class="info-item">
          <label>更新日期：</label>
          <span>{{ getLatestUpdateDate(project.id) || '暂无更新' }}</span>
        </div>
      </div>

      <div class="project-update">
        <label>最近更新：</label>
        <p class="update-content">{{ getLatestUpdate(project.id) || '暂无更新' }}</p>
      </div>

      <div class="project-buttons">
        <n-button class="mc-btn-mint" size="small" @click="emit('update', project)">更新</n-button>
        <n-button class="mc-btn-blue" size="small" @click="emit('view', project)">详情</n-button>
        <n-popconfirm
          v-if="isAdmin"
          positive-text="删除"
          negative-text="取消"
          @positive-click="emit('delete', project.id)"
        >
          <template #trigger>
            <n-button class="mc-btn-danger" size="small">删除</n-button>
          </template>
          确定删除项目「{{ project.name }}」吗？删除后不可恢复。
        </n-popconfirm>
      </div>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NCard, NTag, NButton, NPopconfirm } from 'naive-ui'
import { getStageMeta } from '../constants/stageColors'

interface ProjectLike {
  id: string | number
  name: string
  scale?: string
  stage?: string | number
  stage_text?: string
  [key: string]: unknown
}

const props = defineProps<{
  project: ProjectLike
  isAdmin: boolean
  /** 由父组件注入，保持唯一的进度数据来源 */
  getLatestUpdateDate: (projectId: string | number) => string
  getLatestUpdate: (projectId: string | number) => string
}>()

const emit = defineEmits<{
  (e: 'update', project: ProjectLike): void
  (e: 'view', project: ProjectLike): void
  (e: 'delete', id: string | number): void
}>()

/** 阶段徽标配色沿用原有五档渐变（保留资产），由 style.css 的 .mc-stage-tag 承载 */
const stageMeta = computed(() => getStageMeta(props.project.stage))
</script>

<style scoped>
.project-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 16px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}

/* 不同阶段的卡片左边框颜色 - 马卡龙配色（保留资产） */
.project-card.stage-initial {
  border-left: 4px solid #7EC8E3;
  background: linear-gradient(135deg, rgba(126, 200, 227, 0.05) 0%, white 100%);
}

.project-card.stage-approved {
  border-left: 4px solid #A8E6CF;
  background: linear-gradient(135deg, rgba(168, 230, 207, 0.05) 0%, white 100%);
}

.project-card.stage-bidding {
  border-left: 4px solid #FFEAA7;
  background: linear-gradient(135deg, rgba(255, 234, 167, 0.1) 0%, white 100%);
}

.project-card.stage-awarded {
  border-left: 4px solid #FFB7B2;
  background: linear-gradient(135deg, rgba(255, 183, 178, 0.05) 0%, white 100%);
}

.project-card.stage-completed {
  border-left: 4px solid #C3B1E1;
  background: linear-gradient(135deg, rgba(195, 177, 225, 0.05) 0%, white 100%);
}

.project-card.stage-unknown {
  border-left: 4px solid #D4C4F0;
  background: white;
}

:deep(.n-card-header) {
  padding: 16px 20px;
  border-bottom: 1px solid #F0E6E3;
  background: linear-gradient(90deg, rgba(168, 230, 207, 0.08), rgba(255, 154, 139, 0.08));
}

.project-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.project-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #5D5A6D;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 70%;
}

.status-badge {
  flex-shrink: 0;
  font-weight: 600;
  font-size: 12px;
}

.project-card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.project-info {
  margin-bottom: 16px;
}

.info-item {
  margin-bottom: 8px;
  font-size: 13px;
}

.info-item label {
  font-weight: 500;
  color: #8B8899;
  margin-right: 8px;
}

.info-item span {
  color: #5D5A6D;
}

.project-update {
  flex: 1;
  margin-top: 16px;
}

.project-update label {
  font-weight: 500;
  color: #8B8899;
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
}

.update-content {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  max-height: 3em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #5D5A6D;
}

.project-buttons {
  margin-top: 16px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

@media (max-width: 768px) {
  :deep(.n-card-header) {
    padding: 14px 16px;
  }

  .project-name {
    max-width: 100%;
    white-space: normal;
  }

  .project-card-body {
    padding: 16px;
  }

  .update-content {
    -webkit-line-clamp: 3;
    max-height: 4.5em;
  }

  .project-buttons {
    flex-wrap: wrap;
    gap: 8px;
  }

  .project-buttons :deep(.n-button) {
    flex: 1 1 auto;
  }
}
</style>

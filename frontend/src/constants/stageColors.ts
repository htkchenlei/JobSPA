/**
 * 「保留资产」常量：阶段五档配色、项目卡片左边框色、日历三态色、图表色板。
 * 这些色值属于方案文档明确保留的品牌资产，改造时只换承载组件，色值不得调整。
 */

export interface StageMeta {
  /** CSS 类名，与原有 .status-badge / .project-card 的阶段类一致 */
  className: string
  /** 阶段名称 */
  label: string
  /** 徽标渐变背景 */
  gradient: string
  /** 徽标文字色 */
  textColor: string
  /** 卡片左边框 / 图表 / 时间线节点用的纯色 */
  solid: string
}

/** 阶段五档（1 立项中 / 2 已立项 / 3 招投标 / 4 已中标 / 5 已完成） */
export const STAGE_META: Record<number, StageMeta> = {
  1: {
    className: 'stage-initial',
    label: '立项中',
    gradient: 'linear-gradient(135deg, #7EC8E3, #6BB8D3)',
    textColor: '#FFFFFF',
    solid: '#7EC8E3'
  },
  2: {
    className: 'stage-approved',
    label: '已立项',
    gradient: 'linear-gradient(135deg, #A8E6CF, #88D8B0)',
    textColor: '#FFFFFF',
    solid: '#A8E6CF'
  },
  3: {
    className: 'stage-bidding',
    label: '招投标',
    gradient: 'linear-gradient(135deg, #FFEAA7, #FDCB6E)',
    textColor: '#5D5A6D',
    solid: '#FFEAA7'
  },
  4: {
    className: 'stage-awarded',
    label: '已中标',
    gradient: 'linear-gradient(135deg, #FFB7B2, #FF9A8B)',
    textColor: '#FFFFFF',
    solid: '#FFB7B2'
  },
  5: {
    className: 'stage-completed',
    label: '已完成',
    gradient: 'linear-gradient(135deg, #C3B1E1, #B19FD0)',
    textColor: '#FFFFFF',
    solid: '#C3B1E1'
  }
}

const UNKNOWN_STAGE: StageMeta = {
  className: 'stage-unknown',
  label: '未知阶段',
  gradient: 'linear-gradient(135deg, #E8E0F0, #D4C4F0)',
  textColor: '#8B8899',
  solid: '#D4C4F0'
}

export const getStageMeta = (stage: unknown): StageMeta => {
  const num = parseInt(String(stage))
  return STAGE_META[num] ?? UNKNOWN_STAGE
}

/** 图表统一色板（薄荷绿 / 珊瑚粉 / 天蓝 / 薰衣草 / 柠檬黄 循环） */
export const CHART_PALETTE = [
  '#A8E6CF',
  '#FF9A8B',
  '#7EC8E3',
  '#C3B1E1',
  '#FFEAA7',
  '#88D8B0',
  '#FFB7B2',
  '#6BB8D3',
  '#B19FD0',
  '#FDCB6E',
  '#7DD3C0',
  '#FF8A7A'
]

/** 日历三态 + 选中态配色（保留原有语义） */
export const CALENDAR_COLORS = {
  today: { gradient: 'linear-gradient(135deg, #7EC8E3, #6BB8D3)', solid: '#7EC8E3' },
  log: { gradient: 'linear-gradient(135deg, #A8E6CF, #7DD3C0)', solid: '#A8E6CF' },
  activities: { gradient: 'linear-gradient(135deg, #F1F8F1, #E8F5E8)', solid: '#E8F5E8' },
  selected: '#B19FD0',
  muted: '#D4C4F0'
} as const

/** 「重要更新」强调色 */
export const IMPORTANT_COLOR = '#FF9A8B'

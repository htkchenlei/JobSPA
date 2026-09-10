import type { GlobalThemeOverrides } from 'naive-ui'

/**
 * 马卡龙品牌五色 —— 全站唯一真源，与 style.css 中的 --macaron-* 完全一致。
 * 改造原则「只换壳不改色」：以下色值禁止调整。
 */
export const macaron = {
  cream: '#FFF9F5', // 奶油白 - 主背景
  mint: '#A8E6CF', // 薄荷绿
  mintDark: '#88D8B0', // 薄荷绿深
  coral: '#FF9A8B', // 珊瑚粉 - 主操作
  coralDark: '#FF8A7A', // 珊瑚粉深
  sky: '#7EC8E3', // 天蓝
  skyDark: '#6BB8D3', // 天蓝深
  lavender: '#C3B1E1', // 薰衣草紫 - 次操作
  lavenderDark: '#B19FD0', // 薰衣草紫深 - 聚焦/选中描边
  peach: '#FFB7B2', // 蜜桃粉
  lemon: '#FFEAA7', // 柠檬黄
  text: '#5D5A6D', // 主文字
  textLight: '#8B8899', // 次要文字
  border: '#F0E6E3', // 边框
  danger: '#FF6B6B', // 危险
  white: '#FFFFFF'
} as const

/** 语义色（方案文档 root 中定义的语义色，用于在浅色卡片上保持可读对比度） */
const semantic = {
  success: '#5EC2A0', // 薄荷绿深一档，保证浅底上的 3:1 以上对比
  successHover: '#4FB58F',
  successPressed: '#46A583',
  warning: '#E0A32E', // 柠檬黄深一档
  warningHover: '#D0952A',
  warningPressed: '#C08724'
} as const

const fontFamily =
  '"PingFang SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'

/**
 * 马卡龙配色 → Naive UI 主题映射。
 * 任何组件都从这里取色，禁止在页面里硬编码十六进制。
 */
export const macaronThemeOverrides: GlobalThemeOverrides = {
  common: {
    // 主操作：珊瑚粉
    primaryColor: macaron.coral,
    primaryColorHover: macaron.coralDark,
    primaryColorPressed: '#F2796A',
    primaryColorSuppl: macaron.coralDark,
    // 成功态：薄荷绿
    successColor: semantic.success,
    successColorHover: semantic.successHover,
    successColorPressed: semantic.successPressed,
    successColorSuppl: semantic.success,
    // 信息态：天蓝
    infoColor: macaron.skyDark,
    infoColorHover: '#5AA9C4',
    infoColorPressed: '#4E9BB6',
    infoColorSuppl: macaron.skyDark,
    // 警示态：柠檬黄
    warningColor: semantic.warning,
    warningColorHover: semantic.warningHover,
    warningColorPressed: semantic.warningPressed,
    warningColorSuppl: semantic.warning,
    // 危险态：深珊瑚红
    errorColor: macaron.danger,
    errorColorHover: '#F25C5C',
    errorColorPressed: '#E04F4F',
    errorColorSuppl: macaron.danger,

    // 文字
    textColorBase: macaron.text,
    textColor1: macaron.text,
    textColor2: '#6E6B7E',
    textColor3: macaron.textLight,
    textColorDisabled: '#B4B1C0',
    placeholderColor: '#B4B1C0',
    placeholderColorDisabled: '#C9C6D2',
    iconColor: macaron.textLight,
    iconColorHover: macaron.text,
    iconColorPressed: macaron.text,
    iconColorDisabled: '#C9C6D2',

    // 面 / 线
    baseColor: macaron.white,
    bodyColor: macaron.cream,
    cardColor: macaron.white,
    modalColor: macaron.white,
    popoverColor: macaron.white,
    tableColor: macaron.white,
    tableHeaderColor: '#FFF6F1',
    inputColor: macaron.white,
    inputColorDisabled: '#FBF7F4',
    codeColor: '#FFF6F1',
    tagColor: '#FFFFFF',
    actionColor: '#FFF3EE',
    borderColor: macaron.border,
    dividerColor: macaron.border,
    hoverColor: 'rgba(168, 230, 207, 0.10)',
    pressedColor: 'rgba(168, 230, 207, 0.18)',
    tableColorHover: 'rgba(168, 230, 207, 0.08)',
    tableColorStriped: 'rgba(168, 230, 207, 0.05)',
    railColor: '#F0E6E3',

    // 圆角 / 字号 / 行高 / 控件高度（8px 网格 + 1.25 刻度）
    borderRadius: '12px',
    borderRadiusSmall: '8px',
    fontFamily,
    fontFamilyMono: '"SFMono-Regular", "JetBrains Mono", Consolas, "Courier New", monospace',
    fontSize: '14px',
    fontSizeMini: '11px',
    fontSizeTiny: '12px',
    fontSizeSmall: '13px',
    fontSizeMedium: '14px',
    fontSizeLarge: '16px',
    fontSizeHuge: '20px',
    lineHeight: '1.6',
    heightMini: '24px',
    heightTiny: '28px',
    heightSmall: '32px',
    heightMedium: '38px',
    heightLarge: '44px',
    heightHuge: '52px',
    fontWeight: '400',
    fontWeightStrong: '600',

    // 阴影：低饱和彩色投影，保持马卡龙柔和观感
    boxShadow1: '0 1px 3px rgba(93, 90, 109, 0.06), 0 1px 2px rgba(93, 90, 109, 0.04)',
    boxShadow2: '0 4px 16px rgba(93, 90, 109, 0.06), 0 2px 6px rgba(93, 90, 109, 0.04)',
    boxShadow3: '0 12px 32px rgba(93, 90, 109, 0.10), 0 4px 12px rgba(93, 90, 109, 0.06)',

    cubicBezierEaseInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    scrollbarColor: 'rgba(177, 159, 208, 0.35)',
    scrollbarColorHover: 'rgba(177, 159, 208, 0.55)',
    scrollbarBorderRadius: '6px'
  },
  Input: {
    borderRadius: '10px',
    border: `1px solid ${macaron.border}`,
    borderHover: `1px solid ${macaron.lavenderDark}`,
    borderFocus: `1px solid ${macaron.mintDark}`,
    boxShadowFocus: '0 0 0 3px rgba(168, 230, 207, 0.28)',
    borderError: '1px solid #F2A0A0',
    borderHoverError: '1px solid #EC8C8C',
    borderFocusError: `1px solid ${macaron.danger}`,
    boxShadowFocusError: '0 0 0 3px rgba(255, 107, 107, 0.22)',
    borderWarning: '1px solid #F0DCA6',
    borderHoverWarning: '1px solid #E8CE86',
    borderFocusWarning: `1px solid ${semantic.warning}`,
    boxShadowFocusWarning: '0 0 0 3px rgba(224, 163, 46, 0.20)'
  },
  Card: {
    borderRadius: '20px',
    borderColor: macaron.border,
    color: macaron.white,
    textColor: macaron.text,
    titleTextColor: macaron.text,
    titleFontWeight: '600',
    titleFontSizeMedium: '16px',
    fontSizeMedium: '14px',
    paddingMedium: '20px',
    paddingLarge: '24px',
    boxShadow: '0 4px 20px rgba(93, 90, 109, 0.05)'
  },
  Button: {
    borderRadiusTiny: '8px',
    borderRadiusSmall: '10px',
    borderRadiusMedium: '12px',
    borderRadiusLarge: '14px',
    fontWeight: '600',
    fontWeightStrong: '700'
  },
  Tag: {
    borderRadius: '999px',
    fontWeightStrong: '600'
  },
  Tabs: {
    tabFontWeightActive: '700',
    barColor: macaron.lavenderDark,
    tabTextColorActiveLine: macaron.text,
    tabTextColorHoverLine: macaron.text
  },
  Message: {
    borderRadius: '12px',
    boxShadow: '0 8px 28px rgba(93, 90, 109, 0.12)'
  },
  Dialog: {
    borderRadius: '20px',
    titleFontWeight: '700'
  },
  Popconfirm: {
    // n-popconfirm 的气泡圆角由 Popover 主题统一控制
    fontSize: '13px'
  }
}

export default macaronThemeOverrides

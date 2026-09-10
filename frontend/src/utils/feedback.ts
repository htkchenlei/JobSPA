import { createDiscreteApi, dateZhCN, zhCN } from 'naive-ui'
import { macaronThemeOverrides } from '../theme/naiveTheme'

/**
 * 与主题一致的全局消息 / 确认框。
 *
 * 说明：`useMessage()` 只能在 provider 子组件的 setup 内调用，而项目里的
 * `alert()` / `confirm()` 大多写在普通函数中，因此这里用 `createDiscreteApi`
 * 生成一个与 NConfigProvider 同主题的单例，可在任意上下文中直接替换原生弹窗。
 */
const { message, dialog, notification, loadingBar } = createDiscreteApi(
  ['message', 'dialog', 'notification', 'loadingBar'],
  {
    configProviderProps: {
      themeOverrides: macaronThemeOverrides,
      locale: zhCN,
      dateLocale: dateZhCN
    }
  }
)

/** 危险操作二次确认（替代原生 confirm()） */
export const confirmDanger = (options: {
  title: string
  content: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void | Promise<void>
}) => {
  dialog.warning({
    title: options.title,
    content: options.content,
    positiveText: options.confirmText ?? '确认删除',
    negativeText: options.cancelText ?? '取消',
    positiveButtonProps: { type: 'error' },
    onPositiveClick: async () => {
      await options.onConfirm()
    }
  })
}

/** 普通二次确认（替代原生 confirm()） */
export const confirmAction = (options: {
  title: string
  content: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void | Promise<void>
}) => {
  dialog.info({
    title: options.title,
    content: options.content,
    positiveText: options.confirmText ?? '确认',
    negativeText: options.cancelText ?? '取消',
    onPositiveClick: async () => {
      await options.onConfirm()
    }
  })
}

export { message, dialog, notification, loadingBar }

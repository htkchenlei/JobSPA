import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5000,
    host: true,
    // /api 前缀专属后端接口（Flask 蓝图），代理到本地后端服务。
    // 前端页面路由不得占用 /api（API 文档页已改为 /api-docs），
    // 其余前端路由由 appType: 'spa' 回退到 index.html。
    appType: 'spa',
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  }
})
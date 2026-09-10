import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5000,
    host: true,
    // 后端接口均为 /api/xxx 形式，代理规则精确到 /api/ 前缀，
    // 避免误伤以 /api 开头的前端路由（如 /apis 文档页）。
    // 其余前端路由由 appType: 'spa' 回退到 index.html。
    appType: 'spa',
    proxy: {
      '/api/': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  }
})
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5000,
    host: true,
    // 允许直接访问 /api、/dashboard 等前端路由时回退到 index.html。
    // 否则 Vite 会把 /api 当成真实目录去找 dist/api 下的文件，
    // 命中构建产物或 404，导致按路由直接打开时整页白屏。
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
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 15669,
    host: true,
    proxy: {
      '/api': {
        target: 'http://172.16.100.223:15667',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  }
})
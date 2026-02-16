import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 15668,
    proxy: {
      '/api': {
        target: 'http://localhost:15667',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    port: 5174,  // make sure this matches the port you actually use
    proxy: {
    // It was literally just this fml
    '^/pages.json$': {
      target: 'http://127.0.0.1:5000',
      changeOrigin: true,
      secure: false,
    },
    '/data': {
      target: 'http://127.0.0.1:5000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/data/, '/data'),
      },
    }
  }
})

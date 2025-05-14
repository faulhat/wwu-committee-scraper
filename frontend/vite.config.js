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
      // Proxy /pages.json → your Flask backend
      '/pages.json': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // Proxy anything under /data/ to Flask’s /data/
      '/data': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        // If your Flask route is /data/<path>, this rewrite preserves it:
        rewrite: (path) => path.replace(/^\/data/, '/data'),
      },
    }
  }
})

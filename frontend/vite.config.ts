import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import reactRefresh from '@vitejs/plugin-react-refresh'
import { resolve } from 'path'

const root = resolve(__dirname, 'src')
const outDir = resolve(__dirname, 'dist')

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [reactRefresh(), svelte()],
  build: {
    outDir,
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(root, 'index.html'),
      }
    }
  }
})

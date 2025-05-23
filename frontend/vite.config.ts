import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import monacoEditorPlugin from 'vite-plugin-monaco-editor';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    (monacoEditorPlugin as any).default({})
  ],
  optimizeDeps: {
    exclude: ['lucide-vue-next'],
  },
}); 
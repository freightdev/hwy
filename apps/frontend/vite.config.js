import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { hwyFrontendConfig } from '../configs/frontend/app.config.js';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    host: hwyFrontendConfig.devHost,
    port: hwyFrontendConfig.devPort,
    strictPort: true,
    allowedHosts: hwyFrontendConfig.allowedHosts,
    proxy: {
      '/api': {
        target: hwyFrontendConfig.viteProxyTarget,
        changeOrigin: true,
      }
    }
  }
});

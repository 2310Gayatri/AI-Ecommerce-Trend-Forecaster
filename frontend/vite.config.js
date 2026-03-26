import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'

// Plugin: watches backend output (JSON + PDF) and triggers a browser reload when it changes
function backendDataWatcher() {
  return {
    name: 'backend-data-watcher',
    configureServer(server) {
      const backendDir = path.resolve(__dirname, '../data/output')
      const publicDir = path.resolve(__dirname, 'public')

      const syncFiles = [
        { src: 'market_dashboard_data.json', dest: 'market_dashboard_data.json' },
        { src: 'market_report.pdf', dest: 'market_report.pdf' }
      ]

      const sync = () => {
        syncFiles.forEach(({ src, dest }) => {
          const srcPath = path.join(backendDir, src)
          const destPath = path.join(publicDir, dest)
          if (fs.existsSync(srcPath)) {
            try {
              fs.copyFileSync(srcPath, destPath)
              console.log(`[vite] Sync: ${src} -> public/${dest}`)
            } catch (e) {
              console.error(`[vite] Sync failed for ${src}:`, e)
            }
          }
        })
      }

      // Initial sync
      sync()

      // Watch the whole output directory for changes
      if (fs.existsSync(backendDir)) {
        fs.watch(backendDir, (eventType, filename) => {
          // If the specifically watched files changed, re-sync and reload
          if (syncFiles.some(f => f.src === filename)) {
            sync()
            if (filename.endsWith('.json')) {
              console.log(`[vite] ${filename} updated — reloading browser...`)
              server.ws.send({ type: 'full-reload' })
            }
          }
        })
      }
    },
  }
}

export default defineConfig({
  plugins: [react(), backendDataWatcher()],
})

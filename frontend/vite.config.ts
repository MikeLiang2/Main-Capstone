import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
//import { createSvgIconsPlugin } from 'vite-plugin-svg-icons-ng'
import path from 'path'
import Components from 'unplugin-vue-components/vite'
// Automatically import components from Element Plus
// https://github.com/unplugin/unplugin-vue-components
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import svgLoader from 'vite-svg-loader'

export default defineConfig({
  plugins: [
    vue(),
    svgLoader(),
    Components({
      dirs: ['src/components'],      // 自动扫描的目录（可多个）
      extensions: ['vue'],           // 支持的文件扩展名
      deep: true,                    // 是否深度扫描子目录
      dts: 'src/components.d.ts',    // 自动生成类型声明文件
      resolvers: [
        ElementPlusResolver()        // 如果你还用 Element Plus，它也自动引入
      ]
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@utils': path.resolve(__dirname, 'src/utils')
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @use "@/styles/reset.scss" as *;
          @use "@/styles/global_var.scss";
        `,
      },
    },
  },
   server: {
    host: '0.0.0.0', 
    port: 5173,
  },
})

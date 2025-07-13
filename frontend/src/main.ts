// 入口

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
//import './style.css'
import '@/styles/index.scss'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

//pinia storage
import pinia from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router)
app.use(ElementPlus)
app.use(pinia)

import '@/premission' // routing premission control

app.mount('#app')


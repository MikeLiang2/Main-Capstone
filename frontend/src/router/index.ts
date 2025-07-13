import { createRouter, createWebHashHistory } from 'vue-router'
import { constantRoute } from './routes'

// 创建路由器对象
const router = createRouter({
  history: createWebHashHistory(),


  routes: constantRoute,

  // scroll behavior
  scrollBehavior() {
    return {
      left: 0,
      top: 0
    }
  }
})

export default router;

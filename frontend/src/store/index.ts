//多个组件之间要共享数据
//你也不想每次刷新页面就让登录状态丢失罢
//管理全局状态（比如登录状态、用户信息、权限、主题色...）
//然后用个仓库存这些状态

// pinia storage
import { createPinia } from 'pinia';

// create
let pinia = createPinia();

export default pinia;


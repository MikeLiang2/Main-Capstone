// data state
import type {RouteRecordRaw} from 'vue-router'
export interface UserState {
    token: string | null;
    menuRoutes: RouteRecordRaw[];
    username: string; // 用户名
    userimage: string; // 用户头像
}


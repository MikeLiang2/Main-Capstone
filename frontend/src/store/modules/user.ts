//创建用户相关的仓库
import { defineStore } from 'pinia';
// api
import { Mylogin, getUserInfo } from '@/api/user';
// data type
import type { loginData, tokenData } from '@/api/user/type';

import type { UserState } from '@/store/modules/types/type';

// token OPERATIONS
import { GET_TOKEN, SET_TOKEN, REMOVE_TOKEN } from '@/utils/token';
import { constantRoute } from '@/router/routes';

let useUserStore = defineStore('User', {
    //store user status
    state: (): UserState => {
        return {
            // user token
            // token: localStorage.getItem('token') || ''
            // get token from local storage 本地拿token
            // token: localStorage.getItem('token') || ''
            // 通过工具函数获取token
            // 通过工具函数获取token
            // token: GET_TOKEN() || ''
            // token: localStorage.getItem('token') || GET_TOKEN()
            token: GET_TOKEN(),
            menuRoutes: constantRoute, // get all routes
            username: '', // 用户名
            userimage: '', // 用户头像
        }
        // get token from local storage 本地拿token
        // token: localStorage.getItem('token')
        //token: GET_TOKEN()
    },
    // store user getters
    // get status from state
    getters: {

    },

    //process user actions after login/logout
    actions: {
        async userLogin(user: loginData) {
            let res = await Mylogin(user);

            // Check if the response is successful
            if (res.status == 200) {
                // Set user info and token in the store
                this.token = (res.data.access_token as string);
                // store user info in local storage
                //本地存储用户信息 token
                //localStorage.setItem('token', (res.data.token as string));
                SET_TOKEN(res.data.access_token as string);
                // success
                return 'ojbk';

            } else {
                // Handle login failure
                return Promise.reject('Login failed: ' + (res.statusText as string));
            }
        },

        async fetchUserData() {
            // Fetch user data from the server
            // You can use your API service to get user data
            // For example:
            // return MyfetchUserData().then(res => {
            //     if (res.code == 200) {
            //         this.userInfo = res.data;
            //     }
            // });
            let res = await getUserInfo();

            //store user info when success fetch
            if (res.status == 200) {
                // Set user info in the store
                this.username = res.data.username;
                this.userimage = res.data.avatar;
                //console.log(this.username);
                //console.log(this.userimage);
                // return successa
                return 'ojbk';

            } else {
                // Handle fetch failure
                return Promise.reject('Fetch user data failed');
            }
        },

        // logout
        logout() {
            // Clear user token and info
            this.token = '';
            this.username = '';
            this.userimage = '';
            // Clear token from local storage
            // localStorage.removeItem('token');
            // Clear token using utility function
            REMOVE_TOKEN();
            // return success
            // console.log(this.token);
        }
    }
})

export default useUserStore;
// routing premission control

import router from '@/router';
import nprogress from 'nprogress';
import 'nprogress/nprogress.css'

// user store, for token check
import pinia from './store';
import useUserStore from '@/store/modules/user';
import { GET_TOKEN } from './utils/token';

let userStore = useUserStore(pinia);

// global
//  front guard
// before touch any route, check if the user is logged in
router.beforeEach(async (to, from, next) => {
    // if the route is login, then allow

    nprogress.start(); // start progress bar

    let token = GET_TOKEN();
    let hasUsername = userStore.username;
    if (token) {

        // 登陆成功后的所有判断
        // if the user is logged in, then allow to go to the route
        if (to.path === '/login') {
            // if the user is logged in, then redirect to home page
            next({ path: '/' });
        }
        else {
            // if the user is logged in, then allow to go to the route
            // 可以加入其他的权限判断
            
            if (hasUsername) {
                // if the user has a username, then allow to go to the route
                // await userStore.fetchUserData();
                // console.log(GET_TOKEN());
                next();
            }

            else {
                // if the user does not have a username,
                // try to get one
                // or redirect to the login route
                // avoid token expired
                try {
                    await userStore.fetchUserData();
                    next(); // allow to go to the route
                } catch (error) {
                    // token expired or other error, like edit token

                    //needs clear all user info
                    // force logout
                    userStore.logout();
                    next({ path: '/login' });
                }
            }
        }
    }
    else {
        if (to.path === '/login') {
            // if the user is not logged in, then allow to go to the login route
            next();
        }
        else {
            // if the user is not logged in, then redirect to the login route
            next({ path: '/login' });
        }
    }

});

// after guard
router.afterEach((to, from) => {
    // set document title
    nprogress.done(); // end progress bar
});

//用token 判断是否登陆
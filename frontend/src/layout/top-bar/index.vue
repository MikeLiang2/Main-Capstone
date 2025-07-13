<template>
    <div class="top-bar">
        <!-- <h1>top navi bar</h1> -->
        <bread />

        <div class="top-bar-content">
            <el-button type="primary" size="large" icon="RefreshLeft" @click="Refresh"></el-button>
            <el-button type="primary" size="large" icon="Setting"></el-button>
            <img :src="userStore.userimage" style="width: 40px; height: 40px; border-radius: 50%;">

            <el-dropdown>
                <span class="el-dropdown-link">
                    <!-- // Display the username from the user store -->
                    {{ userStore.username }}
                    <el-icon class="el-icon--right">
                        <arrow-down />
                    </el-icon>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="logout">Logout</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
    </div>
</template>

<script setup lang="ts">
import Bread from '@/layout/top-bar/bread/index.vue';
import useSettingStore from '@/store/setup';
import useUserStore from '@/store/modules/user';

import { useRouter } from 'vue-router';


let settingStore = useSettingStore();
let userStore = useUserStore();
let $router = useRouter();



function Refresh() {
    // Add your refresh logic here
    settingStore.refresh = !settingStore.refresh; // Toggle the refresh state
}


// logout
const logout = () => {
    // Call the logout method from the user store
    //console.log('logout', userStore.token);
    userStore.logout()

    // clear user info in local
    localStorage.removeItem('userInfo');
    // reroute to login page
    $router.push({ path: '/login' });

};
</script>

<script lang="ts">
export default {
    name: 'TopBar'
}
</script>

<style scoped lang="scss">
@use '@/styles/global_var.scss' as *;

.top-bar {
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, #3e6da3, #9b59b6);
    color: $light-text-color;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 20px;
    font-weight: bold;



    .top-bar-content {
        display: flex;
        align-items: center;
        justify-content: center;

        img {
            margin-left: 10px;
            margin-right: 10px;
        }

        .el-dropdown-link {
            color: $light-text-color;
            font-size: 16px;
            margin-right: 25px;
            cursor: pointer;
        }

        .el-icon--right {
            color: $light-text-color;
        }
    }

    ::v-deep(.el-button) {
        background-color: rgb(131, 71, 158);
        color: $light-text-color;
        font-size: 20px;
        margin: 0 6px;
        transition: all 0.3s ease;
        border-color: rgb(190, 175, 255);

        &:hover {
            background-color: rgba(255, 255, 255, 0.2); // hover background color
            color: #ffd166; // hover text and icon color
        }
    }
}
</style>
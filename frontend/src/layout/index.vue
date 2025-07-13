<template>
    <div class="home-container">
        <!-- left menu -->
        <div class="left-menu" :class="{ 'fold': settingStore.fold ? true : false }">
            <Logo> </Logo>

            <!-- left scrollbar -->
            <el-scrollbar class="menu-list">
                <!-- menu items -->
                <!-- dynamic menu generation, 默认获取激活的路由,展开菜单 -->
                <el-menu :default-active="$route.path" active-text-color="#f0b4e3" background-color="#3e6da3"
                    text-color="#fff" class="left-menu-container" :collapse="settingStore.fold" >
                    <Menu :menuList="userStore.menuRoutes"></Menu>
                </el-menu>

            </el-scrollbar>
        </div>

        <!-- top navigation -->
        <div class="top-nav" :class="{ 'fold': settingStore.fold ? true : false }">
            <!--
            <el-icon>
                <HomeFilled />
            </el-icon>
            <svg-icon name="user" width="32px" height="32px" color="red" />
            -->
            <!-- <h1>Welcome to the Checklist Management System</h1> -->
            <TopBar></TopBar>
        </div>

        <!-- main content -->
        <div class="main-content" :class="{ 'fold': settingStore.fold ? true : false }">
            <Main></Main>
            <!-- <p style="height:1000px; background: lightblue;">This is the main content area.</p>  -->
        </div>

    </div>
</template>

<script setup lang="ts">


// dynamic menu generation
import Menu from '@/layout/menu/index.vue'
// add logo component
import Logo from '@/layout/logo/index.vue'
// add main component
import Main from '@/layout/main/index.vue'
// router 
import { useRoute } from 'vue-router'
// get user store
import UseUserStore from '@/store/modules/user'
// layout seetting store
import useSettingStore from '@/store/setup'

// top navigation menu bar
import TopBar from '@/layout/top-bar/index.vue'

let userStore = UseUserStore();
let settingStore = useSettingStore();

let $route = useRoute();


</script>

<script lang="ts">

export default {
    name: 'HomeLayout',
    components: {
        Menu,
        Logo,
        Main,
        TopBar
    }
}

</script>


<style scoped lang='scss'>
@use '@/styles/global_var.scss' as *;

.home-container {
    width: 100%;
    height: 100vh;

    .left-menu {
        width: $menu-width;
        height: 100vh;
        background: $dark-base-color;
        transition: all 0.4s;

        &.fold {
            width: $menu-min-width;
        }

        .menulist {
            width: 100%;
            height: calc(100vh - $menu-logo-height);
            overflow: auto;

            .left-menu {
                border-right: none;
            }
        }


    }

    .top-nav {
        width: calc(100% - $menu-width);
        height: $top-nav-height;
        background: $base-color;
        position: absolute;
        top: 0;
        left: $menu-width;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.4s;

        &.fold {
            width: calc(100vw - $menu-min-width);
            left: $menu-min-width;
        }
    }

    .main-content {
        position: absolute;
        width: calc(100% - $menu-width);
        height: calc(100vh - $top-nav-height);
        background: $light-base-color;
        left: $menu-width;
        top: $top-nav-height;
        padding: 20px;
        overflow: auto;
        transition: all 0.4s;
        &.fold {
            width: calc(100vw - $menu-min-width);
            left: $menu-min-width;
        }
    }
    
}
</style>
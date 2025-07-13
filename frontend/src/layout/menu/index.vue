<!-- 动态路由，获取路由表，自动拉出菜单 -->

<template>

    <!-- <p>{{ menuList }} </p> 这个测试menulist 到这里-->
    <template v-for="item in menuList" :key="item.path">
        <!-- no children route -->
        <template v-if="!item.children">
            <!-- hidden route -->
            <el-menu-item v-if="!item.meta.hidden" :index="item.path" @click="goTo">
                <el-icon style="color: white;">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <template #title>

                    <span>{{ item.meta.title }}</span>
                </template>
            </el-menu-item>
        </template>


        <!-- has 1 children route 这个没啥用-->
        <template v-if="item.children && item.children.length == 1">
            <el-menu-item v-if="!item.children[0].meta.hidden" :index="item.children[0].path" @click="goTo">
                <el-icon style="color: white;">
                    <component :is="item.children[0].meta.icon"></component>
                </el-icon>
                <template #title>

                    <span>{{ item.children[0].meta.title }}</span>
                </template>
            </el-menu-item>
        </template>

        <!-- has more than 1 children route -->
        <el-sub-menu v-if="item.children && item.children.length > 1" :index="item.path">
            <template #title>
                <el-icon style="color: white;">
                    <component :is="item.meta.icon"></component>
                </el-icon>
                <span>{{ item.meta.title }}</span>
            </template>
            <Menu :menuList="item.children"></Menu>
        </el-sub-menu>
    </template>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
let $router = useRouter();

// get menu list route from props, get a array of menu items
defineProps(['menuList'])


const goTo = (path: any) => {
    // navigate to the specified route
    $router.push(path.index);
    //console.log(`Navigating to: ${path.index}`);
    //console.log(path);
}

</script>

<script lang="ts">
export default {
    name: 'Menu'
}
</script>
<style scoped></style>
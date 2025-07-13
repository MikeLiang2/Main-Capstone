<template>

    <div class="top-bar-collapse" @click="changeIcon">
        <el-icon class="topbar-expand-icon" style="color: white;">
            <component :is="settingStore.fold ? 'Expand' : 'Fold'" />
        </el-icon>

        <!-- Reference from https://element-plus.org/zh-CN/component/breadcrumb.html -->
        <el-breadcrumb separator-icon="ArrowRight">
            <el-breadcrumb-item v-for="(item, index) in $route.matched" :key="index">
                {{ item.meta.title }}
            </el-breadcrumb-item>
        </el-breadcrumb>
    </div>

</template>

<script setup lang="ts">
import useSettingStore from '@/store/setup';
import { useRoute } from 'vue-router';
//getlayout setting
const settingStore = useSettingStore();
const $route = useRoute();


const changeIcon = () => {
    // 直接通过改仓库来改状态
    // 所有的组件都可以通过这个仓库来获取状态，管理
    settingStore.fold = !settingStore.fold;
};
</script>


<script lang="ts">
export default {
    name: 'Bread'
}
</script>

<style scoped lang="scss">
@use '@/styles/global_var.scss' as *;


.el-breadcrumb {
    margin: 0 20px;
    color: $light-text-color;
    align-items: center;
}



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
        cursor: pointer;
    }

    .el-icon--right {
        color: $light-text-color;
    }
}

.top-bar-collapse {
    display: flex;
    align-items: center;

}

.topbar-expand-icon {
    color: white;
    font-size: 24px; // icon size
    margin-right: 16px; // right margin
    margin-left: 30px; // left margin
    //cursor: pointer; // mouse hover changes to pointer (optional)
}

// 不知道为啥改不了颜色，只能这样强制改
::v-deep(.el-breadcrumb__inner),
::v-deep(.el-breadcrumb__separator) {
    color: $light-text-color !important;
}
</style>
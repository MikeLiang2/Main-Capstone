<template>
  <!-- Main layout, below for simple transition -->
  <!-- 点击某个东西会把组件搞到这里，然后渲染-->
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in" appear>
      <div v-if="status" :key="$route.fullPath">
        <component :is="Component" />
      </div>
    </transition>
  </router-view>
</template>

<script setup lang="ts">
import useSettingStore from '@/store/setup';
import { watch } from 'vue';
import { ref, nextTick } from 'vue';

let status = ref(true); // Define a reactive variable to hold the refresh status
let settingStore = useSettingStore();
// Listen for changes in the refresh state
// This will trigger a re-render when the refresh state changes
watch(() => settingStore.refresh, () => {
  // Handle the refresh state change
  status.value = false; // Set status to false to trigger re-render
  nextTick(() => {
    status.value = true; // Set status to true after the next DOM update cycle
  });
});

</script>

<script lang="ts">
export default {
  name: 'Main'
}
</script>

<style scoped>
/* 进入/离开都用到的激活态（定义过渡属性与时长） */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 150ms ease;
}

/* 初始进入态 & 最终离开态：透明 */
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 进入结束态 & 离开起始态：不透明 */
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
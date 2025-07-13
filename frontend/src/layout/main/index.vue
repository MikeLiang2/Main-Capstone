<template>
    <!-- Main layout, below for simple transition -->
    <!-- 点击某个东西会把组件搞到这里，然后渲染--> 
    <router-view v-slot="{ Component }">
        <transition name="fade">
            <!-- Render the component dynamically based on the current route -->
            <component :is="Component" v-if="status" />
        </transition>
    </router-view>
</template>

<script setup lang="ts">
import useSettingStore from '@/store/setup';
import { watch } from 'vue';
import { ref, nextTick} from 'vue';

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
/* enter begin */
.fade-enter-from {
  opacity: 0;
}
/* enter process */
.fade-enter-active {
  transition: all 1s;
}
/* begin leave */
.fade-enter-to {
  opacity: 1;
}
</style>

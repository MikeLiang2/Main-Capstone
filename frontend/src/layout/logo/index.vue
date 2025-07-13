<!-- logo component test -->
<template>
    <div class="logo">
        <img :src="setting.logo" alt="Logo" />
        <p>{{ setting.title }}</p>
    </div>
</template>

<script setup lang="ts">

//external imports of seeting pattern
import setting from '@/setting'

</script>

<script lang="ts">
export default {
    name: 'Logo'
}
</script>

<style scoped lang="scss">
@use '@/styles/global_var.scss' as *;

.logo {
    width: 100%;
    height: $menu-logo-height;
    color: white;
    display: flex;
    align-items: center;
    padding: 10px;

    img {
        width: 50px;
        height: 50px;
    }

    p {
        font-size: $menu-logo-text-size;
        font-weight: bold;
        margin-left: 15px;
        color: $menu-logo-text-color;
    }
}
</style>
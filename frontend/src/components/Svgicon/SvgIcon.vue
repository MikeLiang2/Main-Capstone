<!-- src/components/SvgIcon.vue -->
<script setup lang="ts">
import { defineAsyncComponent, computed } from 'vue'

const props = withDefaults(
  defineProps<{
    name: string
    color?: string
    width?: string
    height?: string
    className?: string
  }>(),
  {
    color: '#000000',
    width: '1em',
    height: '1em',
    className: '',
  }
)

// dynamically import the SVG component based on the name prop
// This assumes that the SVG files are located in the `assets/src/icons` directory
//usage in global:     <svg-icon name="user" width="32px" height="32px" />
const SvgComp = defineAsyncComponent(() =>
  import(`@/assets/icons/${props.name}.svg`)
)

const styles = computed(() => ({
  width: props.width || '1em',
  height: props.height || '1em',
  fill: props.color || 'currentColor',
}))
</script>

<template>
  <component :is="SvgComp" :class="className" :style="styles" />
</template>

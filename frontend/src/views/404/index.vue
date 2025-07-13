<template>
  <div class="not-found">
    <h1>404 - Not Found</h1>
    <button @click="goHome">Go Home</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('login')
}
</script>

<style scoped>
.not-found {
  text-align: center;
  padding: 80px;
  font-family: sans-serif;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
}
</style>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref("加载中...")

onMounted(() => {
  axios.get("http://localhost:8000/")
    .then(res => {
      message.value = res.data.message
    })
    .catch(err => {
      message.value = "后端连接失败"
    })
})
</script>

<template>
  <h1>{{ message }}</h1>
</template>
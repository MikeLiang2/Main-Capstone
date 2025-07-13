<template>
  <div class="home-container">
    <!-- Welcome Card -->
    <el-card class="home-card">
      <div class="welcome-section">
        <el-avatar :size="80" :src="userStore.userimage" />
        <div class="welcome-text">
          <h2>Welcome back, {{ userStore.username }}!</h2>
          <p>We're glad to see you again.</p>
        </div>
      </div>
    </el-card>

    <!-- Time Card -->
    <el-card class="time-card">
      <div class="time-display">
        {{ currentTime }}
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import useUserStore from '@/store/modules/user';

const userStore = useUserStore();

const currentTime = ref(new Date().toLocaleString());

onMounted(() => {
  userStore.fetchUserData();

  setInterval(() => {
    currentTime.value = new Date().toLocaleString();
  }, 1000);
});
</script>

<style scoped lang="scss">
.home-container {
  max-width: 800px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.home-card,
.time-card {
  background-color: #b9e2ff;
  border-radius: 12px;
  padding: 24px;
}

.welcome-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome-text h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.welcome-text p {
  margin: 4px 0 0;
  color: #555;
}

.time-display {
  font-size: 32px;
  font-weight: bold;
  color: #1565c0;
  text-align: center;
}
</style>

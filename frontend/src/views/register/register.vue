<template>
  <div class="login">
    <div class="login-left">
      <h1 class="system-title">Checklist Management System</h1>
    </div>

    <div class="login-box">
      <div class="login-title">Register</div>
      <p class="login-subtitle">Create your account</p>

      <el-form ref="registerFormRef" :model="registerData" :rules="registerRules" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="registerData.username" placeholder="Username" :prefix-icon="User" />
        </el-form-item>

        <el-form-item prop="email">
          <el-input v-model="registerData.email" placeholder="Email" :prefix-icon="Message" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="registerData.password" type="password" show-password placeholder="Password"
            :prefix-icon="Lock" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="login-btn" :loading="loading" @click="handleRegister" round>
            Sign Up
          </el-button>
        </el-form-item>

        <el-link type="primary" @click="goLogin">
          Already have an account? Sign in
        </el-link>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Message, Lock, User } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus'
import service from '@/utils/request'
import type { FormRules } from 'element-plus'

const $router = useRouter()
const loading = ref(false)
const registerFormRef = ref()

const registerData = reactive({
  username: '',
  email: '',
  password: '',
  is_active: true,
  is_superuser: false,
  is_verified: false,
  avatar: ''
})

const registerRules: FormRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' }
  ]
}

// let service = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL });

async function handleRegister() {
  await registerFormRef.value.validate()

  loading.value = true
  try {
    await service.post('/auth/register', registerData)
    ElNotification({ title: 'Success', message: 'Registration successful! Please login.', type: 'success' })
    $router.push('/login')
  } catch (error: any) {
    console.error(error)
    ElNotification({
      title: 'Error',
      message: error?.response?.data?.detail || 'Registration failed.',
      type: 'error'
    })
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  $router.push('/login')
}
</script>

<style scoped lang="scss">
.login {
  width: 100%;
  height: 100vh;
  background: url('@/assets/images/logintemp.jpg') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;

  .login-form {
    .el-form-item {
      margin-bottom: 20px;
    }
  }

  .login-left {
    flex: 1;
    text-align: center;
    color: #ffffff;

    .system-title {
      font-size: 2.8rem;
      font-weight: bold;
      text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.4);
    }
  }

  .login-box {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    text-align: center;
    margin-right: 5vw;
  }

  .login-title {
    font-size: 24px;
    font-weight: bold;
    color: #6ca1e7;
    margin-bottom: 10px;
  }

  .login-subtitle {
    font-size: 16px;
    font-weight: bold;
    color: #6ca1e7;
    margin-bottom: 20px;
  }

  @media (max-width: 768px) {
    flex-direction: column;

    .login-left {
      display: none;
    }

    .login-box {
      margin-right: 0;
    }
  }
}
</style>

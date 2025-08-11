<template>
  <div class="login">
    <div class="login-left">
      <h1 class="system-title">Checklist Management System</h1>
    </div>

    <div class="login-box">
      <div class="login-title">Welcome</div>
      <p class="login-subtitle">Please sign in to your account</p>
      <!-- 前端 check rule 设定在下面 -->
      <el-form ref="ruleFormRef" class="login-form" :model="loginData" :rules="checkRules">
        <el-form-item prop="username">
          <el-input v-model="loginData.username" placeholder="Email" :prefix-icon="Message" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="loginData.password" type="password" show-password placeholder="Password"
            :prefix-icon="Lock" />
        </el-form-item>

        <el-form-item>
          <el-button :loading="loading" type="primary" class="login-btn" @click="login" round>
            Sign In
          </el-button>
        </el-form-item>
      </el-form>

      <div class="register-link">
        <el-link type="primary" @click="goRegister">
          Don't have an account? Sign up
        </el-link>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Message, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElNotification } from 'element-plus'
// userstore manage user status
import useUserStore from '@/store/modules/user'

// get loginForm reference
const ruleFormRef = ref()

const loading = ref(false)
// Initialize the user store
let userStore = useUserStore()
// Use the router for navigation
// This is the Vue Router instance, which allows us to navigate between routes
let $router = useRouter()


//用户名收集
//登陆逻辑等
//登陆状态用pinia管理
const loginData = reactive({
  username: 'admin@example.com',
  password: '123456'
})

// form validation rules
const checkRules = {
  username: [
    { required: true, message: 'Please enter your email', trigger: 'blur' },
    { min: 1, max: 40, message: 'Email must be between 1 and 40 characters', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter your password', trigger: 'blur' },
    { min: 1, max: 20, message: 'Password must be between 1 and 20 characters', trigger: 'blur' }
  ]
}

async function login() {

  // Validate the form
  await ruleFormRef.value.validate();

  // 加载动画状态
  loading.value = true;

  //login process
  try {
    // Call the user store's login method
    await userStore.userLogin(loginData);
    loading.value = false;
    // successfully logged in, redirect to checklist page
    $router.push({ name: 'layout' });
    ElNotification({
      title: 'Success',
      message: 'Login successful!',
      type: 'success',
      duration: 3000
    });

  } catch (error) {
    // handle login error
    loading.value = false;
    console.error('Login failed:', error);
    ElNotification({
      title: 'Error',
      message: 'Login failed, please check your username and password.',
      type: 'error',
      duration: 3000
    });
  }
  //const res = userStore.userLogin(loginData);
  //console.log(res)
}

const goRegister = () => {
  $router.push('/register')
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

  //元素间距
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

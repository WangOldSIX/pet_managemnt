<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>宠物管理系统</h2>
          <p>Pet Management System</p>
        </div>
      </template>
      
      <!-- Tab 切换 -->
      <el-tabs v-model="activeTab" class="auth-tabs">
        <!-- 登录 Tab -->
        <el-tab-pane label="登录" name="login">
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            label-position="top"
            @keyup.enter="handleLogin"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                prefix-icon="User"
                size="large"
              />
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                prefix-icon="Lock"
                size="large"
                show-password
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                @click="handleLogin"
                style="width: 100%"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <!-- 注册 Tab -->
        <el-tab-pane label="注册" name="register">
          <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            label-position="top"
            @keyup.enter="handleRegister"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名（至少3位）"
                prefix-icon="User"
                size="large"
              />
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="请输入密码（至少6位）"
                prefix-icon="Lock"
                size="large"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                prefix-icon="Lock"
                size="large"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="registerForm.email"
                placeholder="请输入邮箱（可选）"
                prefix-icon="Message"
                size="large"
              />
            </el-form-item>
            
            <el-form-item label="真实姓名" prop="realName">
              <el-input
                v-model="registerForm.realName"
                placeholder="请输入真实姓名（可选）"
                prefix-icon="UserFilled"
                size="large"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="success"
                size="large"
                :loading="loading"
                @click="handleRegister"
                style="width: 100%"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { register } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('login')
const loginFormRef = ref(null)
const registerFormRef = ref(null)
const loading = ref(false)

// 登录表单
const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 注册表单
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  realName: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度为 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 100, message: '密码长度为 6 到 100 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    const success = await userStore.login(loginForm)
    
    if (success) {
      ElMessage.success('登录成功')
      router.push('/')
    }
  } catch (error) {
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    const res = await register({
      username: registerForm.username,
      password: registerForm.password,
      confirm_password: registerForm.confirmPassword,
      email: registerForm.email || undefined,
      real_name: registerForm.realName || undefined
    })
    
    if (res.code === 200) {
      ElMessage.success('注册成功，请登录')
      // 切换到登录 Tab
      activeTab.value = 'login'
      // 自动填充用户名
      loginForm.username = registerForm.username
      // 清空注册表单
      registerForm.username = ''
      registerForm.password = ''
      registerForm.confirmPassword = ''
      registerForm.email = ''
      registerForm.realName = ''
    } else {
      ElMessage.error(res.msg || '注册失败')
    }
  } catch (error) {
    console.error('Register error:', error)
    ElMessage.error(error.message || '注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 480px;
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 24px;
}

.card-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.el-form-item {
  margin-bottom: 20px;
}

.auth-tabs {
  margin-top: 10px;
}

:deep(.el-tabs__nav-wrap::after) {
  height: 0;
}

:deep(.el-tabs__item) {
  font-size: 16px;
}
</style>

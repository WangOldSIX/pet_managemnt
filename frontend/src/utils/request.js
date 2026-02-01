import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// Request interceptor
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  response => {
    const { code, msg, data } = response.data
    
    if (code === 200 || code === undefined) {
      return response.data
    } else {
      ElMessage.error(msg || '请求失败')
      return Promise.reject(new Error(msg))
    }
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        ElMessage.error('登录已过期，请重新登录')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      } else {
        ElMessage.error(data?.msg || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请稍后重试')
    }
    
    return Promise.reject(error)
  }
)

export default request

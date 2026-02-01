import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (newUser) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  const login = async (credentials) => {
    const res = await loginApi(credentials)
    if (res.data) {
      setToken(res.data.access_token)
      setUser(res.data.user)
      return true
    }
    return false
  }

  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const fetchUserInfo = async () => {
    const res = await getCurrentUser()
    if (res.data) {
      setUser(res.data)
      return res.data
    }
    return null
  }

  return {
    token,
    user,
    setToken,
    setUser,
    login,
    logout,
    fetchUserInfo
  }
})

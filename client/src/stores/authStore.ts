import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const nickname = ref('')
    const accessToken = ref('')

    const setAuth = (data: { nickname: string; access_token: string }): void => {
      nickname.value = data.nickname
      accessToken.value = data.access_token
    }

    return {
      nickname,
      accessToken,
      setAuth
    }
  },
  { persist: { storage: localStorage, key: 'redo-tok' } }
)

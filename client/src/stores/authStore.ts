import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const nickname = ref('')
    const accessToken = ref('')
    const isAuthenticated = computed(() => !!accessToken.value)

    const setAuth = (data: { nickname: string; access_token: string }): void => {
      nickname.value = data.nickname
      accessToken.value = data.access_token
    }

    return {
      nickname,
      accessToken,
      isAuthenticated,
      setAuth
    }
  },
  { persist: { storage: localStorage, key: 'redo-tok' } }
)

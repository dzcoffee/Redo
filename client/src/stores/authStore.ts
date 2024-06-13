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

    const clear = (): void => {
      nickname.value = ''
      accessToken.value = ''
    }

    return {
      nickname,
      accessToken,
      isAuthenticated,
      setAuth,
      clear
    }
  },
  { persist: { storage: localStorage, key: 'redo-tok' } }
)

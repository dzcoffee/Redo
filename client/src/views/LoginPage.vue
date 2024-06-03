<template>
  <v-container id="welcome-page" class="pa-0 ma-0">
    <v-row class="h-100 pa-0 ma-0">
      <v-col id="welcome-pane" class="pa-0 ma-0 d-flex flex-column align-center justify-center">
        <img width="300" src="@/assets/logo.png" class="ma-0" />
        <span class="intro text-h6 text-md-h5 text-lg-h4">Redo가 제공하는 퀴즈로</span>
        <span>
          <span class="intro d-inline text-h6 text-md-h5 text-lg-h4">새로운 </span>
          <span class="intro d-inline keyword text-h6 text-md-h5 text-lg-h4">학습</span>
          <span class="intro d-inline text-h6 text-md-h5 text-lg-h4">을 경험하세요!</span>
        </span>
      </v-col>
      <v-col id="login-pane" class="pa-0 ma-0 d-flex flex-column align-center justify-center">
        <input class="input mb-2 text-subtitle-1 text-md-h6 text-lg-h5" placeholder="아이디" :value="auth.accountID"
          @input="changeId" />
        <input type="password" class="input mt-2 mb-4 text-subtitle-1 text-md-h6 text-lg-h5" placeholder="비밀번호"
          :value="auth.password" @input="changePassword" @keyup.enter="handleLogin" />
        <v-btn class="auth-btn ma-2 text-subtitle-1 text-md-h6 text-lg-h5" @click="handleLogin">로그인</v-btn>
        <v-btn class="auth-btn ma-2 text-subtitle-1 text-md-h6 text-lg-h5" @click="handleSignUp">회원 가입</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from '@/composables/toast'
import { signIn } from '@/api/apis';
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = ref({ accountID: '', password: '' })
const authStore = useAuthStore()

const changeId = (e: Event): void => {
  auth.value.accountID = (e.target as HTMLTextAreaElement).value
}

const changePassword = (e: Event): void => {
  auth.value.password = (e.target as HTMLTextAreaElement).value
}

const handleLogin = async (): Promise<void> => {
  if (auth.value.accountID === '' || auth.value.password === '') {
    showToast('error', '아이디와 비밀번호를 모두 입력해주세요.')
    return
  }
  console.log(auth.value)
  await signIn(auth.value)
    .then((res) => {
      showToast('success', "로그인 성공");
      authStore.setAuth(res);
      router.push('/memo');
    })
    .catch((e) => {
      showToast('error', '아이디 또는 비밀번호가 틀렸습니다.')
      console.log(e);
    });
}
const handleSignUp = (): void => {
  router.push('/signup')
}
</script>

<style scoped>
#welcome-page {
  min-width: 100%;
  height: 100%;
}
#welcome-pane {
  height: 100%;
  background-color: #fdf8ec;
}
#login-pane {
  height: 100%;
  background-color: #67a58d;
}
.auth-btn {
  background-color: #0c3324;
  color: white;
  width: 40%;
  min-width: 80px;
  height: 48px;
  font-weight: 600;
}
.input {
  width: 40%;
  min-width: 80px;
  height: 48px;
  outline: none;
  border: 1px solid grey;
  border-radius: 5px;
  background-color: white;
}
.intro {
  font-weight: 600;
}
.keyword {
  color: #67a58d;
}
</style>

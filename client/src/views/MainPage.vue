<template>
  <v-container id="welcome-page" class="pa-0 ma-0">
    <v-row class="h-100 pa-0 ma-0">
      <v-col id="welcome-pane" class="pa-0 ma-0 d-flex flex-column align-center justify-center">
        <v-img :width="300" :max-height="300" src="src/assets/logo.png" class="ma-0"></v-img>
        <h1>Redo가 제공하는 퀴즈로</h1>
        <span>
          <h1 class="d-inline">새로운 </h1>
          <h1 class="d-inline">학습</h1>
          <h1 class="d-inline">을 경험하세요!</h1>
        </span>

      </v-col>
      <v-col id="login-pane" class="pa-0 ma-0 d-flex flex-column align-center justify-center">
        <input class="input account mb-2" placeholder="아이디">
        <input class="input password mt-2 mb-4" placeholder="비밀번호" @keyup.enter="handleLogin">
        <v-btn class="auth-btn ma-2" @click="handleLogin">로그인</v-btn>
        <v-btn class="auth-btn ma-2">회원 가입</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
const handleLogin = (): void => {
  router.push('/memo');
}
</script>

<style scoped>
#welcome-page {
  min-width: 100%;
  height: 100%;
}
#welcome-pane {
  height: 100%;
  background-color: #FDF8EC;
}
#login-pane {
  height: 100%;
  background-color: #67A58D;
}
.auth-btn {
  background-color: #0C3324;
  color: white;
  width: 30%;
  height: 48px;
  font-size: 24px;
  font-weight: 600;
}
.input {
  width: 30%;
  height: 48px;
  border-radius: 5px;
  background-color: white;
  font-size: 24px;
}
</style>
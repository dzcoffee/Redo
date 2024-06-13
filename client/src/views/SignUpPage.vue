<template>
  <v-container class="signup-page d-flex flex-column align-center justify-center h-100">
    <v-card class="py-5 px-8">
      <v-col class="d-flex flex-column align-center mb-5">
        <img width="80" src="@/assets/logo.png" />
        <span class="info text-subtitle-1 text-md-h6 text-lg-h5">회원가입</span>
        <span class="text-subtitle-1">(특정 특수문자는 입력하실 수 없습니다.)</span>
      </v-col>
      <InfoInput title="닉네임" placeholder="10자 이내" validText="10자 이내로 입력하세요." @update-input="onChangeNickname">
      </InfoInput>
      <InfoInput title="아이디" placeholder="10자 이내" validText="10자 이내로 입력하세요." @update-input="onChangeAccountId">
      </InfoInput>
      <InfoInput title="비밀번호" placeholder="10자 이내" validText="10자 이내로 입력하세요." @update-input="onChangePassword">
      </InfoInput>
      <InfoInput v-bind:valid="isDuplicated" title="비밀번호 확인" placeholder="다시 입력해주세요."
        validText="10자 이내로 비밀번호와 일치하게 입력하세요." @update-input="onChangeCheckPassword"></InfoInput>
      <v-col class="d-flex flex-column align-center">
        <v-btn class="register-btn" elevation="0" @click="handleRegister">회원 가입하기</v-btn>
      </v-col>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import InfoInput from '@/components/login/InfoInput.vue'
import { showToast } from '@/composables/toast'
import { signUp } from '@/api/apis'
import { type User } from '@/domain/type'
import { useRouter } from 'vue-router'

const router = useRouter()
const newUser = ref<User>({ accountID: '', nickname: '', password: '' })
const passwordChecked = ref('')
const LIMIT_LENGTH = 10

const isDuplicated = computed(() => newUser.value.password === passwordChecked.value)
const isValidInput = computed(() => newUser.value.accountID !== '' && newUser.value.nickname !== '' && newUser.value.password !== '')
const isValidInputLength = computed(
  () =>
    newUser.value.accountID.length <= LIMIT_LENGTH && newUser.value.nickname.length <= LIMIT_LENGTH && newUser.value.password.length <= LIMIT_LENGTH
)

const onChangeAccountId = (prop: string): void => {
  newUser.value.accountID = prop
}
const onChangeNickname = (prop: string): void => {
  newUser.value.nickname = prop
}
const onChangePassword = (prop: string): void => {
  newUser.value.password = prop
}
const onChangeCheckPassword = (prop: string): void => {
  passwordChecked.value = prop
}
const handleRegister = async (): Promise<void> => {
  if (!isValidInput.value || !isValidInputLength.value || passwordChecked.value !== newUser.value.password) {
    showToast('error', '입력 형식을 맞춰주세요.')
    return
  }
  await signUp(newUser.value)
    .then(() => {
      showToast('success', '회원가입 성공')
      router.push('/login')
    })
    .catch((e: any) => {
      if (e.response.status === 409) showToast('error', '닉네임 또는 아이디가 중복됐습니다.')
    })
}
</script>

<style scoped>
.info {
  font-weight: 600;
}
.register-btn {
  background-color: #67a58d;
  color: white;
  font-weight: 600;
}
.signup-page {
  background-color: #fdf8ec;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 100%;
  height: 100%;
}
</style>

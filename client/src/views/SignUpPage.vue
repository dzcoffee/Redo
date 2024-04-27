<template>
    <v-container class="signup-page d-flex flex-column align-center justify-center h-100">
        <v-card class="py-5 px-8">
            <v-col class="d-flex flex-column align-center">
                <v-img :width="80" :height="80" src="src/assets/logo.png"></v-img>
                <span class="text-subtitle-1 text-md-h6 text-lg-h5">회원가입</span>
            </v-col>
            <InfoInput title="닉네임" placeholder="10자 이내" buttonName="중복 확인"></InfoInput>
            <InfoInput title="아이디" placeholder="10자 이내" buttonName="중복 확인"></InfoInput>
            <InfoInput title="비밀번호" placeholder="10자 이내"></InfoInput>
            <InfoInput title="비밀번호 확인" placeholder="다시 입력해주세요."></InfoInput>
            <v-col class="d-flex flex-column align-center">
                <v-btn class="register-btn" elevation="0" @click="handleRegister">회원 가입하기</v-btn>
            </v-col>
        </v-card>
    </v-container>
</template>

<script setup lang="ts">
import InfoInput from '@/components/login/InfoInput.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const handleRegister = (): void =>{
    router.push('/memo');
}
</script>

<style scoped>
.register-btn{
    background-color: #67A58D;
    color: white;
    font-weight: 600;
}
.signup-page{
    background-color: #FDF8EC;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 100%;
    height: 100%;
}
</style>
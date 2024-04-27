<template>
    <v-col class="pa-0 my-2 d-flex align-center justify-space-between">
        <label class="mr-7 title">{{ title }}</label>
        <input :type="isSecure ? 'password' : 'text'" class="info-input px-1" :style="{'border-color': validColor}" :placeholder="placeholder">
        <v-btn v-if="buttonName" class="ml-7 check-btn" elevation="0" @click="handler">{{ buttonName }}</v-btn>
    </v-col>
    <v-col class="ma-0 pa-0 py-1">
        <span class="valid-text" :style="{color: validColor}">{{ validText }}</span>
    </v-col>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const {title, placeholder, buttonName, handler} = defineProps({
    title: {type: String, default: "제목", "required": false},
    placeholder: {type: String, default: "입력 조건", "required": false},
    buttonName: {type: String, default: "", "required": false},
    handler: {type: Function, required:false},
    validText: {type: String, default: "사용 가능합니다.", required: false}
})

const isValid = ref(true);
const validColor = computed(() => isValid.value ? "#67A58D" : "#EA4335")
const isSecure = computed(() => title.includes("비밀번호"));
</script>

<style scoped>
.check-btn{
    background-color: #0C3324;
    color: white;
    min-width: 80px;
    font-size: 18px;
    font-weight: 600;
    height: 42px;
}
.info-input{
    border: 1px solid;
    border-radius: 5px;
    height: 42px;
}
.info-input:focus{
    outline: none;
}
.info-input::placeholder{
    color: #67A58D;
}
.title{
    font-weight: 600;
}
.valid-text{
    color: #67A58D;
}
</style>
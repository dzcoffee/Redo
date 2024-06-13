<template>
  <v-col class="pa-0 my-2 d-flex align-center justify-space-between">
    <label class="mr-7 title">{{ title }}</label>
    <input :type="isSecure ? 'password' : 'text'" class="info-input px-1" :style="{ 'border-color': validColor }"
      :placeholder="placeholder" v-model="inputValue" :value="inputValue" @input="changeInput" />
    <v-btn v-if="buttonName" class="ml-7 check-btn" elevation="0" @click="handler">{{ buttonName }}</v-btn>
  </v-col>
  <v-col class="ma-0 pa-0 py-1">
    <span v-if="!(valid && inputValue.length <= 10)" class="valid-text" :style="{ color: '#EA4335' }">{{ validText
      }}</span>
  </v-col>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

const { valid, title, placeholder, buttonName, handler } = defineProps({
  valid: { type: Boolean, default: true, required: false },
  title: { type: String, default: '제목', required: false },
  placeholder: { type: String, default: '입력 조건', required: false },
  buttonName: { type: String, default: '', required: false },
  handler: { type: Function, required: false },
  validText: { type: String, default: '', required: false }
})

const emits = defineEmits(['update-input'])

const isValid = computed(() => {
  return valid && inputValue.value.length <= 10
})
const validColor = computed(() => {
  return isValid.value ? '#67A58D' : '#EA4335'
})
const isSecure = computed(() => title.includes('비밀번호'))
const inputValue = ref('')
const changeInput = (e: Event): void => {
  inputValue.value = (e.target as HTMLTextAreaElement).value.replace(/[,<>[\]\\'":;\s()/]+/g, '')
  emits('update-input', inputValue.value)
}
</script>

<style scoped>
.check-btn {
  background-color: #0c3324;
  color: white;
  min-width: 80px;
  font-size: 18px;
  font-weight: 600;
  height: 42px;
}
.info-input {
  border: 1px solid;
  border-radius: 5px;
  height: 42px;
}
.info-input:focus {
  outline: none;
}
.title {
  font-weight: 600;
}
.valid-text {
  color: #67a58d;
}
</style>

<template>
  <textarea class="short-answer pa-1" label="답을 적으세요." :value="inputValue" @input="changeInput" outlined></textarea>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuizStore } from '@/stores/quizStore'

const { problemNumber } = defineProps({
  problemNumber: { type: Number, reuiqred: false, default: 0 }
})
const quizStore = useQuizStore()
const inputValue = ref('')
const changeInput = (e: Event): void => {
  inputValue.value = (e.target as HTMLTextAreaElement).value
  quizStore.answer[problemNumber] = inputValue.value
}
</script>

<style scoped>
.short-answer {
  border: 1px solid #eaeaea;
  border-radius: 10px;
  resize: none;
  outline: none;
  width: 95%;
  min-height: 10vh;
}
</style>

<template>
  <textarea class="short-answer pa-1" label="답을 적으세요." :value="inputValue" @input="changeInput" outlined></textarea>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const inputValue = ref('');
const changeInput = (e: Event): void => {
  inputValue.value = (e.target as HTMLTextAreaElement).value;
};
</script>

<style scoped>
.short-answer {
  border: 1px solid #EAEAEA;
  border-radius: 10px;
  resize: none;
  outline: none;
  width: 95%;
  min-height: 10vh;
}
</style>
<template>
  <v-row class="my-3" align="center">
    <v-btn class="choice-btn" elevation="0" :color="isSelected ? '#0C3324' : '#67A58D'" @click="onClick">{{ index + 1 }}</v-btn>
    <span class="pl-4">{{ content }}</span>
  </v-row>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useQuizStore } from '@/stores/quizStore';


const { problemNumber, index, content } = defineProps({
  problemNumber: {type: Number, reuiqred: false, default: 0},
  index: { type: Number, required: true, default: 0 },
  content: { type: String, required: true, default: '선택지 내용' }
})

const emits = defineEmits(['select-answer']);
const quizStore = useQuizStore();
const isSelected = computed(() => quizStore.answer[problemNumber] === String(index + 1));

const onClick = (): void => {
  quizStore.answer[problemNumber] = String(index + 1);
}
</script>

<style scoped>
.choice-btn {
  border-radius: 50%;
  padding: 0;
  min-width: 5px;
  aspect-ratio: 1 / 1;
}
</style>
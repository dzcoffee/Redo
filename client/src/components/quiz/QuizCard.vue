<template>
  <v-card width="80%" class="my-4">
    <div style="min-width: 0;">
      <v-card-title class="font-weight-bold">{{ question }}</v-card-title>
      <v-card-subtitle v-if="quizStore.state === QuizState.GRADE">결과 확인</v-card-subtitle>
    </div>
    <v-card-item>
      <v-col v-if="quizStore.quizType === '객관식'">
        <MultipleChoice :content="option" v-for="(option, index) in options"
          :key="index" :index="index"></MultipleChoice>
      </v-col>
      <v-col v-else align="center">
          <ShortAnswer></ShortAnswer>
      </v-col>
    </v-card-item>
    <v-card-actions>
      <v-spacer></v-spacer>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { QuizState, useQuizStore } from '@/stores/quizStore';
import MultipleChoice from '@/components/quiz/MultipleChoice.vue';
import ShortAnswer from '@/components/quiz/ShortAnswer.vue';

const {question, options} = defineProps({
  index: { type: Number, required: true, default: 0 },
  question: {type: String, default: '', required: false},
  options: {type: Array<String>, default: [], required: false}
})

const quizStore = useQuizStore();
</script>

<style scoped>
.submit-btn {
  background-color: #335447;
  color: white;
}
</style>
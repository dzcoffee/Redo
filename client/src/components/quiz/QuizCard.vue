<template>
  <v-card width="80%" class="my-4">
    <div style="min-width: 0">
      <v-card-title class="font-weight-bold" style="white-space: normal">
        <div class="d-flex flex-column">
          {{ question }}
          <v-btn :ripple="false" variance="outlined" elevation="0" rounded color="primary" v-if="problem.correctness <= 100" class="similarity"
            >유사도: {{ problem.correctness }}%</v-btn
          >
        </div>
      </v-card-title>
      <v-card-subtitle v-if="quizStore.state === QuizState.GRADE">결과 확인</v-card-subtitle>
    </div>
    <v-card-item>
      <v-col v-if="quizStore.quizType === '객관식'">
        <MultipleChoice
          :content="option"
          v-for="(option, index) in options"
          :key="index"
          :index="index"
          :problem-number="problemNumber"
          @select-answer="selectAnswer"
        ></MultipleChoice>
      </v-col>
      <v-col v-else align="center">
        <ShortAnswer :problem-number="problemNumber"></ShortAnswer>
      </v-col>
      <v-col v-if="quizStore.state === QuizState.GRADE">
        <p class="answer">* 해설</p>
        <p class="answer mb-2">{{ quizStore.rawAnswer[quizStore.quizType === '단답식' ? index + 1 : index]['reason'] }}</p>
        <QuizReview :data="quizStore.rawAnswer" :problem-id="problemId"></QuizReview>
      </v-col>
    </v-card-item>
    <v-card-actions>
      <v-spacer></v-spacer>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { QuizState, useQuizStore } from '@/stores/quizStore'
import MultipleChoice from '@/components/quiz/MultipleChoice.vue'
import { ref, type PropType } from 'vue'
import QuizReview from '@/components/quiz/QuizReview.vue'
import ShortAnswer from '@/components/quiz/ShortAnswer.vue'

const { problemNumber, problemId, index, question, options } = defineProps({
  problemNumber: { type: Number, required: true, default: 0 },
  problemId: { type: Number, required: true, default: 0 },
  index: { type: Number, required: true, default: 0 },
  question: { type: String, default: '', required: false },
  options: { type: Array as PropType<string[]>, default: () => [], required: false }
})
const quizStore = useQuizStore()
const problem = ref(quizStore.problems[index])
const selectAnswer = (prop: string): void => {
  quizStore.answer[index] = prop
}
</script>

<style scoped>
.answer {
  color: #67a58d;
}
.similarity {
  max-width: 120px;
  font-size: 12px;
  height: 24px;
}
.submit-btn {
  background-color: #335447;
  color: white;
}
</style>

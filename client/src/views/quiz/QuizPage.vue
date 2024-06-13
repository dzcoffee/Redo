<template>
  <v-col class="container d-flex flex-column h-100 ma-0 px-5">
    <div class="pa-2 container back-btn">
      <v-btn icon="mdi-arrow-left" density="comfortable" color="#FDF8EC" @click="() => router.back()"> </v-btn>
    </div>
    <v-spacer></v-spacer>
    <v-card class="container quiz-container">
      <div class="d-flex flex-column align-center">
        <QuizCard
          :question="problem.question"
          :options="problem.options"
          :problem-number="index"
          :problem-id="problem.id"
          v-for="(problem, index) in quizStore.problems"
          :key="index"
          :index="index"
        ></QuizCard>
      </div>
    </v-card>
    <v-col align="center">
      <v-btn width="20%" id="grade-btn" @click="grading" :loading="isLoading">정답 보기</v-btn>
    </v-col>
    <v-spacer></v-spacer>
  </v-col>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { QuizState, useQuizStore } from '@/stores/quizStore'
import { postData } from '@/api/apis'
import QuizCard from '@/components/quiz/QuizCard.vue'
import { showToast } from '@/composables/toast'
import { useRouter } from 'vue-router'

const router = useRouter()
const quizStore = useQuizStore()

const isLoading = ref(false)

const grading = async (): Promise<void> => {
  isLoading.value = true
  console.log(quizStore.problems)
  const res = await postData(`/quiz/game/${quizStore.quizId}`, { problems: quizStore.problems, user_answer: quizStore.answer }).catch(() =>
    showToast('error', '풀이 요청에 실패했습니다.')
  )
  showToast('info', '풀이를 확인하세요.')
  quizStore.rawAnswer = res
  quizStore.state = QuizState.GRADE
  isLoading.value = false
}

onMounted(() => {
  quizStore.answer = new Array<string>(quizStore.problems.length).fill('')
  quizStore.state = QuizState.TEST
})
</script>

<style scoped>
#grade-btn {
  background-color: #0c3324;
  color: white;
}
.container {
  background-color: #fdf8ec;
}
.quiz-container {
  overflow: hidden;
  overflow-y: scroll;
  height: 70vh;
}
.quiz-container::-webkit-scrollbar {
  width: 6px;
  background-color: #67a58d;
  border-radius: 6px;
}
.quiz-container::-webkit-scrollbar-thumb {
  background-color: #0c3324;
  border-radius: 6px;
}
.quiz-container::-webkit-scrollbar-thumb:hover {
  background-color: #888; /* 스크롤바 호버 시 색상 */
}
</style>

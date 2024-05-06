<template>
  <v-col class="container d-flex flex-column h-100 ma-0 px-5">
    <div class="pa-2 container back-btn">
      <v-btn icon="mdi-arrow-left" density="comfortable" color="#FDF8EC" @click="() => router.back()">
      </v-btn>
    </div>
    <v-spacer></v-spacer>
    <v-card class="container quiz-container">
    <div class="d-flex flex-column align-center">
      <QuizCard :question="problem.question" :options="problem.options" v-for="problem, index in quizStore.problems" :key="index" :index="index"></QuizCard>
    </div>
    </v-card>
    <v-col align="center">
      <v-btn width="20%" id="grade-btn" @click="grading" :loading="isLoading">정답 보기</v-btn>
    </v-col>
    <v-spacer></v-spacer>
  </v-col>
</template>

<script setup lang="ts">
import { QuizState, useQuizStore } from '@/stores/quizStore';
import QuizCard from '@/components/quiz/QuizCard.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const quizStore = useQuizStore();

const isLoading = ref(false);

const grading = (): void => {
    isLoading.value = true;
    // TODO: 정답 요청
    quizStore.state = QuizState.GRADE;
    isLoading.value = false;
}
</script>

<style scoped>
#grade-btn{
  background-color: #0C3324;
  color: white;
}
.container {
  background-color: #FDF8EC;
}
.quiz-container{
  overflow: hidden;
  overflow-y: scroll;
  height: 70vh;
}
.quiz-container::-webkit-scrollbar{
    width: 6px;
    background-color: #67A58D;
    border-radius: 6px;
}
.quiz-container::-webkit-scrollbar-thumb{
    background-color: #0C3324; 
    border-radius: 6px; 
}
.quiz-container::-webkit-scrollbar-thumb:hover {
    background-color: #888; /* 스크롤바 호버 시 색상 */
}
</style>
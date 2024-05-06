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
    <v-spacer></v-spacer>
  </v-col>
</template>

<script setup lang="ts">
import QuizCard from '@/components/quiz/QuizCard.vue';
import { useQuizStore } from '@/stores/quizStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const quizStore = useQuizStore();
</script>

<style scoped>
.container {
  background-color: #FDF8EC;
}
.quiz-container{
  overflow: hidden;
  overflow-y: scroll;
  height: 80vh;
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
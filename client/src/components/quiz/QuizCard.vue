<template>
  <v-card min-width="60%" max-width="80%" class="my-4">
    <v-card-title class="font-weight-bold">{{ problemNumber }}. {{ quiz }}</v-card-title>
    <v-card-item>
      <v-col>
        <MultipleChoice v-bind:problemNubmer="index" :content="choice" v-for="(choice, index) in multipleChoices"
          :key="index" :index="index"></MultipleChoice>
      </v-col>
      <v-col align="center">
          <ShortAnswer></ShortAnswer>
      </v-col>
    </v-card-item>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn class="submit-btn" @click="grading">정답 보기</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import MultipleChoice from '@/components/quiz/MultipleChoice.vue';
import { ref } from 'vue';
import ShortAnswer from '@/components/quiz/ShortAnswer.vue';

const isLoading = ref(false);
const problemNumber = ref(1);
const quiz = ref('Git에 대한 특징으로 옳지 않은 것을 고르세요.');
const multipleChoices = ref([
  'git commit을 이용해 브랜치를 병합할 수 있다.',
  'git push를 이용해 원격 레포지토리에 변경 내역을 적용할 수 있다.',
]);

const grading = (): void => {
    isLoading.value = true;
    // TODO: 정답 요청
    isLoading.value = false;
}
</script>

<style scoped>
.submit-btn {
  background-color: #335447;
  color: white;
}
</style>
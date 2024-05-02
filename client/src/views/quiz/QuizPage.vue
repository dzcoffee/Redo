<template>
  <div class="pa-2 container">
    <v-btn icon="mdi-arrow-left" density="comfortable" color="#FDF8EC" @click="() => router.back()">
    </v-btn>
  </div>
  <v-row class="pa-0 ma-0 container" align="center" justify="center">
    <v-col align="center">
      <h1>{{ quiz }}</h1>
      <v-card max-width="70%">
        <v-card-title>답을 골라주세요.</v-card-title>
        <v-card-item>
          <v-col>
            <MultipleChoice v-bind:problemNubmer="index" :content="choice" v-for="(choice, index) in multipleChoices"
              :key="index" :index="index"></MultipleChoice>
          </v-col>
          <ShortAnswer></ShortAnswer>
        </v-card-item>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn class="submit-btn">정답 보기</v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import MultipleChoice from '@/components/quiz/MultipleChoice.vue';
import { ref } from 'vue';
import ShortAnswer from '@/components/quiz/ShortAnswer.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const quiz = ref('Git에 대한 특징으로 옳지 않은 것을 고르세요.');
const multipleChoices = ref([
  'git commit을 이용해 브랜치를 병합할 수 있다.',
  'git push를 이용해 원격 레포지토리에 변경 내역을 적용할 수 있다.',
]);
</script>

<style scoped>
.container {
  background-color: #FDF8EC;
}
.short-answer {
  border: 1px solid #EAEAEA;
  border-radius: 10px;
  resize: none;
  outline: none;
  width: 90%;
  min-height: 10vh;
}
.submit-btn {
  background-color: #335447;
  color: white;
}
</style>
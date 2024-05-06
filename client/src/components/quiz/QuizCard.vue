<template>
  <v-card min-width="60%" max-width="80%" class="my-4">
    <div style="min-width: 0;">
      <v-card-title class="font-weight-bold">{{ question }}</v-card-title>
    </div>
    <v-card-item>
      <v-col v-if="quizStore.quizType === '객관식'">
        <MultipleChoice v-bind:problemNubmer="index" :content="option" v-for="(option, index) in options"
          :key="index" :index="index"></MultipleChoice>
      </v-col>
      <v-col v-else align="center">
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
import { useQuizStore } from '@/stores/quizStore';

const {question, options} = defineProps({
  index: { type: Number, required: true, default: 0 },
  question: {type: String, default: '', required: false},
  options: {type: Array<String>, default: [], required: false}
})

const quizStore = useQuizStore();

const isLoading = ref(false);

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
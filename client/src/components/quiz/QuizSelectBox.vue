<template>
  <v-col class="ma-0 h-100 d-flex flex-column">
    <span class="text-sm-body-1 text-md-h6 text-lg-h5 font-weight-bold">퀴즈 생성을 위한 메모를 선택해주세요.</span>
    <v-spacer></v-spacer>
    <v-card class="memo-list-container" elevation="2">
      <v-card-title class="text-sm-body-1 text-md-h6 text-lg-h5 font-weight-bold">메모 목록</v-card-title>
      <div class="memo-list d-flex flex-column align-center">
        <MemoForQuiz
          :key="memo.id"
          :index="index"
          :memo="memo"
          :is-selected="selectedIndex === index"
          @click="selectMemo(index)"
          v-for="(memo, index) in memos"
        ></MemoForQuiz>
      </div>
    </v-card>
    <v-spacer></v-spacer>
  </v-col>
</template>

<script setup lang="ts">
import MemoForQuiz from '@/components/quiz/MemoForQuiz.vue'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useMemoStore } from '@/stores/memoStore'
import { useQuizSettingStore } from '@/stores/quizStore'

const { memos } = storeToRefs(useMemoStore())
const quizSettingStore = useQuizSettingStore()
const selectedIndex = ref(-1)
const selectMemo = (index: number): void => {
  if (index === selectedIndex.value) {
    selectedIndex.value = -1
    quizSettingStore.memoId = ''
    return
  }
  selectedIndex.value = index
  quizSettingStore.memoId = memos.value[index].id
}
</script>

<style scoped>
.memo-list-container {
  background-color: #fdf8ec;
}
.memo-list {
  height: 60vh;
  overflow-y: auto;
}
.memo-list::-webkit-scrollbar {
  width: 6px;
  background-color: #67a58d;
  border-radius: 6px;
}
.memo-list::-webkit-scrollbar-thumb {
  background-color: #0c3324;
  border-radius: 6px;
}
.memo-list::-webkit-scrollbar-thumb:hover {
  background-color: #888; /* 스크롤바 호버 시 색상 */
}
</style>

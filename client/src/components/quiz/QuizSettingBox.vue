<template>
  <v-col class="ma-0 pa-0 d-flex h-100 flex-column justify-center">
    <div class="option d-flex align-center justify-space-between">
      <span class="text-sm-body-1 text-md-h6 text-lg-h5 font-weight-bold">문제 개수</span>
      <v-menu transition="fade-transition">
        <template v-slot:activator="{ props }">
          <v-btn class="option-btn" v-bind="props" append-icon="mdi-chevron-down" variant="outlined">
            {{ count }}
          </v-btn>
        </template>
        <v-list class="pa-0" density="compact">
          <v-list-item class="py-0" link v-for="option in options.count.items" :key="option">
            <v-list-item-title @click="count = option">{{ option }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
    <div class="option d-flex align-center justify-space-between">
      <span class="text-sm-body-1 text-md-h6 text-lg-h5 font-weight-bold">문제 형식</span>
      <v-menu transition="fade-transition">
        <template v-slot:activator="{ props }">
          <v-btn class="option-btn" v-bind="props" append-icon="mdi-chevron-down" variant="outlined">
            {{ type }}
          </v-btn>
        </template>
        <v-list class="pa-0" density="compact">
          <v-list-item class="py-0" link v-for="option in options.type.items" :key="option">
            <v-list-item-title @click="type = option">{{ option }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
    <div class="option d-flex align-center justify-space-between">
      <span class="text-sm-body-1 text-md-h6 text-lg-h5 font-weight-bold">난이도</span>
      <v-menu transition="fade-transition">
        <template v-slot:activator="{ props }">
          <v-btn class="option-btn" v-bind="props" append-icon="mdi-chevron-down" variant="outlined">
            {{ difficulty }}
          </v-btn>
        </template>
        <v-list class="pa-0" density="compact">
          <v-list-item class="py-0" link v-for="option in options.difficulty.items" :key="option">
            <v-list-item-title @click="difficulty = option">{{ option }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
    <div class="option d-flex align-center justify-end">
      <v-btn :loading="isLoading" id="create-quiz-btn" class="px-6" @click="moveToQuiz">퀴즈 생성</v-btn>
    </div>
  </v-col>
</template>

<script setup lang="ts">
import { getData, postData } from '@/api/apis'
import { onMounted, ref } from 'vue'
import { useQuizSettingStore, useQuizStore } from '@/stores/quizStore'
import { showToast } from '@/composables/toast'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const quizSettingStore = useQuizSettingStore()
const quizStore = useQuizStore()
const { memoId, count, type, difficulty } = storeToRefs(quizSettingStore)
const isLoading = ref(false)

const moveToQuiz = async (): Promise<void> => {
  if (quizSettingStore.memoId === '') {
    showToast('error', '메모를 선택해주세요.')
    return
  }
  try {
    isLoading.value = true
    showToast('info', '퀴즈 생성 중...')
    const res = await postData(`/quiz?quiz_count=${count.value}&difficulty=${difficulty.value}&memoID=${memoId.value}&type=${type.value}`)
    quizStore.quizId = res.quiz_id
    quizStore.quizType = type.value
    quizStore.problems = await getData(`/quiz/game/${res.quiz_id}`)
    isLoading.value = false
    router.push('/quiz/game')
  } catch (e) {
    showToast('error', '퀴즈 생성에 실패했습니다.')
    isLoading.value = false
  }
}

const options = {
  count: {
    items: ['1', '2', '3', '4', '5']
  },
  type: {
    items: ['객관식', '단답식']
  },
  difficulty: {
    items: ['쉬움', '중간', '어려움']
  }
}

onMounted(() => {
  quizSettingStore.$reset()
})
</script>

<style scoped>
#create-quiz-btn {
  background-color: #0c3324;
  color: white;
  border-radius: 10px;
}
.option {
  padding: 4vh 0;
}
.option-btn {
  background-color: #67a58d;
  color: white;
  border: transparent;
  border-radius: 10px;
}
</style>

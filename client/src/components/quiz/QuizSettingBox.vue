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
            <v-btn id="create-quiz-btn" class="px-6" @click="moveToQuiz">퀴즈 생성</v-btn>
        </div>
    </v-col>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { postData } from '@/api/apis';
import { storeToRefs } from 'pinia';
import { useQuizSettingStore } from '@/stores/quizStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const quizSettingStore = useQuizSettingStore();
const {memoId, count, type, difficulty} = storeToRefs(quizSettingStore);

const moveToQuiz = async (): Promise<void> => {
    if(quizSettingStore.memoId === '') return;
    await postData('/quiz', {memoId: memoId.value, count: count.value, type: type.value, difficulty: difficulty.value})
    .then(() => {
      router.push('/quiz/game');
    })
    .catch(() => {}); // TODO: 나중에 없애기
}

const options = {
    count: {
        items: ["1","2","3","4","5"]
    },
    type: {
        items: ['객관식', '단답식']
    },
    difficulty: {
        items: ['쉬움', '중간', '어려움']
    }
}

onMounted(() => {
  quizSettingStore.$reset();
})
</script>

<style scoped>
#create-quiz-btn{
    background-color: #0C3324;
    color: white;
    border-radius: 10px;
}
.option{
    padding: 4vh 0;
}
.option-btn{
    background-color: #67A58D;
    color: white;
    border: transparent;
    border-radius: 10px;
}
</style>
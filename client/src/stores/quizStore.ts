import { defineStore } from 'pinia'
import { type Problem } from '@/domain/type';
import { ref } from 'vue';

export const useQuizSettingStore = defineStore('quizSetting', () => {
    const memoId = ref('');
    const count = ref('1');
    const type = ref('객관식');
    const difficulty = ref('쉬움');
    const toString = ():void => {
        console.log(`memo id: ${memoId.value}, count: ${count.value}, type: ${type.value}, difficulty: ${difficulty.value}`)
    }

    const $reset = ():void => {
        memoId.value = '';
        count.value = '1';
        type.value = '객관식';
        difficulty.value = '쉬움';
    }

    return {
        memoId,
        type,
        count,
        difficulty,
        toString,
        $reset
    }
})

export enum QuizState{
    TEST,
    GRADE
}

export const useQuizStore = defineStore('quiz', () => {
    const quizId = ref('');
    const quizType = ref('');
    const problems = ref<Problem[]>([
    ]);
    const state = ref<QuizState>(QuizState.TEST);
    const answer = ref<string[]>([]);
    const rawAnswer = ref();


    return {
        quizId,
        quizType,
        problems,
        state,
        answer,
        rawAnswer
    }
}, {persist: {storage: localStorage}})

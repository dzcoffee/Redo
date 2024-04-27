import { defineStore } from 'pinia'
import { ref } from 'vue'

type Memo = {
    id: string,
    title: string,
    categories: string[],
    content: string,
    createdAt: number,
    updatedAt: number,
}

export const useMemoStore = defineStore('memo', () => {
    const memos = ref<Memo[]>([]);
    
    return {
    memos
    }
})

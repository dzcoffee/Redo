import { defineStore } from 'pinia'
import type { Memo } from '@/domain/type';
import { ref } from 'vue'

export const useMemoStore = defineStore('memo', () => {
    const memos = ref<Memo[]>([]);
    
    return {
    memos
    }
})

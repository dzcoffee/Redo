import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMarkdownStore = defineStore('markdown', () => {
  const title = ref('')
  const content = ref('')
  const categories = ref<string[]>([]);

  return {
    title,
    content,
    categories
  }
})

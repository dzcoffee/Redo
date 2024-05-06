import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMarkdownStore = defineStore('markdown', () => {
  const title = ref('')
  const content = ref('')
  const categories = ref<string[]>([]);

  const $reset = (): void => {
    title.value = '';
    content.value = '';
    categories.value = [];
  }
  return {
    title,
    content,
    categories,
    $reset
  }
})

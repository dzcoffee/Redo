<template>
  <textarea :value="content" :placeholder="placeholder" class="content pt-2" @input="changeContent"></textarea>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useMarkdownStore } from '@/stores/markdownStore';

const { content } = storeToRefs(useMarkdownStore());

const placeholder = `메모 내용을 적어주세요...

예시)

# 메모 제목
## 메모 내용`;

const changeContent = (e: Event): void => {
  content.value = (e.target as HTMLTextAreaElement).value;
}

onMounted(() => useMarkdownStore().$reset());
</script>

<style scoped>
.content {
  width: 100%;
  outline: none;
  font-size: 16px;
  font-weight: 500;
  line-height: 1.2;
  color: grey;
  resize: none;
  flex-grow: 1;
  overflow-x: hidden;
}
.content::-webkit-scrollbar {
  width: 6px;
  background-color: #f0f0f0;
  border-radius: 6px;
}
.content::-webkit-scrollbar-thumb {
    background-color: #67A58D;
    border-radius: 6px;
}
.content::-webkit-scrollbar-button {
    display: none;
}
</style>
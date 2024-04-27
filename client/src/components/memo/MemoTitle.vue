<template>
  <textarea placeholder="제목을 입력하세요" :value="title" class="title pa-1 text-sm-h6 text-md-h5" rows="1" @input="changeTitle"></textarea>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useMarkdownStore } from "@/stores/markdownStore";

const { title } = storeToRefs(useMarkdownStore());

const changeTitle = (e: Event): void => {
  title.value = (e.target as HTMLTextAreaElement).value;
};
</script>

<style scoped>
.title {
  width: 100%;
  background-color: transparent;
  font-weight: 700;
  line-height: 1.2;
  color: #67a58d;
  outline: none;
  resize: none;
  overflow-y: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.title::placeholder{
  color: #67a58d;
}
.title::-webkit-scrollbar{
  display: none;
}
</style>

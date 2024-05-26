<template>
  <div class="py-2 d-flex category-bar">
    <input placeholder="카테고리 입력" class="category-input text-md-caption" :value="newCategory" @input="onInput" @keyup.enter="onEnter" />
    <!-- <v-chip color="success" :ripple="false">{{ newCategory }}</v-chip> -->
    <v-btn
      rounded
      color="#0C3324"
      append-icon="mdi-close-circle"
      class="category-btn mr-1 category text-md-caption"
      @click="onClick(index)"
      v-for="(category, index) in categories"
      :key="index"
      :ripple="false"
      >{{ category }}</v-btn
    >
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useMarkdownStore } from '@/stores/markdownStore'

const { categories } = storeToRefs(useMarkdownStore())
const newCategory = ref('')

const onClick = (index: number): void => {
  categories.value.splice(index, 1)
}

const onInput = (e: Event): void => {
  newCategory.value = (e.target as HTMLTextAreaElement).value
}

const onEnter = (): void => {
  if (newCategory.value.length <= 0 || categories.value.includes(newCategory.value)) return
  categories.value.push(newCategory.value)
  newCategory.value = ''
}
</script>

<style scoped>
.category {
  height: 24px;
}
.category-btn {
  vertical-align: middle;
}
.category-input {
  min-width: 85px;
  color: #67a58d;
  outline: none;
}
.category-input::placeholder {
  color: #67a58d;
}
.category-bar {
  overflow-x: auto;
}
.category-bar::-webkit-scrollbar {
  height: 5px;
  background-color: #67a58d;
  border-radius: 6px;
}
.category-bar::-webkit-scrollbar-thumb {
  background-color: #0c3324;
  border-radius: 6px;
}
.category-bar::-webkit-scrollbar-button {
  display: none;
}
</style>

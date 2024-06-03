<template>
  <div class="py-2 d-flex category-bar">
    <!-- <input placeholder="카테고리 입력" class="category-input text-md-caption" :value="newCategory" @input="onInput"
      @keyup.enter="onEnter" /> -->
    <v-menu transition="fade-transition">
      <template v-slot:activator="{ props }">
        <v-btn rounded color="#0C3324" class="category-btn mr-1 category text-md-caption" v-bind="props">카테고리 선택</v-btn>
      </template>
      <v-list class="pa-0" density="compact">
        <v-list-item class="py-0" link v-for="(category, index) in CATEGORY_LIST" :key="index">
          <v-list-item-title @click="onClick(category)">{{ category }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-btn rounded color="#0C3324" append-icon="mdi-close-circle" class="category-btn mr-1 category text-md-caption"
      @click="onDelete(index)" v-for="(category, index) in categories" :key="index" :ripple="false">{{ category
      }}</v-btn>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useMarkdownStore } from '@/stores/markdownStore'

const CATEGORY_LIST = [
  '컴퓨터구조',
  '운영체제',
  '자료구조',
  '데이터베이스',
  '네트워크',
  '소프트웨어공학',
  '알고리즘',
  '설계패턴',
  'C',
  'C++',
  'Java',
  'Javascript',
  'Python',
  '웹',
  '모바일',
  '인공지능',
  '보안',
  '빅데이터'
]

const { categories } = storeToRefs(useMarkdownStore())

const onDelete = (index: number): void => {
  categories.value.splice(index, 1)
}

const onClick = (newCategory: string,): void => {
  if (categories.value.includes(newCategory)) {
    categories.value = categories.value.filter((category) => category !== newCategory)
    return;
  }
  categories.value.push(newCategory)
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

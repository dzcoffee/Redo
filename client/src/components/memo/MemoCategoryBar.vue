<template>
  <div class="py-2 d-flex category-bar">
    <v-dialog width="40%" persistent>
      <template #activator="{ props: on }">
        <v-btn
          rounded
          color="primary"
          class="category-btn mr-1 category text-md-caption"
          :class="!isRecClicked ? 'jiggle' : 'jiggle-stop'"
          v-bind="on"
          @mouseover="
            () => {
              isRecClicked = true
            }
          "
          @click="getRecCategory"
          >카테고리 추천!
          <v-tooltip activator="parent" location="bottom"> GPT에게 카테고리를 추천받아보세요! </v-tooltip>
        </v-btn>
      </template>
      <template v-slot:default="{ isActive }">
        <v-card title="추천 카테고리 선택" class="pa-2">
          <v-card-text class="d-flex align-center justify-center">
            <span v-if="recommendedCategories.length === 0 && content.trim() === ''" class="alert-msg">내용이 비어있습니다. 글을 작성해주세요.</span>
            <v-btn v-else-if="recommendedCategories.length === 0" color="#67a58d" loading rounded class="mx-1" width="50%"></v-btn>
            <div v-else class="d-flex flex-column">
              <div class="d-flex mb-3">
                <v-btn
                  :color="selected[index] ? '#0C3324' : '#67a58d'"
                  rounded
                  class="mx-1"
                  @click="selected[index] = !selected[index]"
                  v-for="(category, index) in recommendedCategories"
                  >{{ category }}
                  <v-icon v-if="selected[index]" class="ml-2">mdi-check-circle</v-icon>
                </v-btn>
              </div>
              <span>추천된 카테고리를 선택하세요.</span>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn id="accept-btn" text="확인" @click="onStore(isActive)"></v-btn>
            <v-btn id="cancel-btn" text="취소" @click="onClose(isActive)"></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
    <v-menu transition="fade-transition">
      <template v-slot:activator="{ props }">
        <v-btn rounded color="#0C3324" class="category-btn mr-1 category text-md-caption" v-bind="props">카테고리 선택</v-btn>
      </template>
      <v-list class="category-list pa-0" density="compact">
        <v-list-item class="py-0" link v-for="(category, index) in CATEGORY_LIST" :key="index">
          <v-list-item-title @click="onClick(category)">{{ category }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-btn
      rounded
      color="#0C3324"
      append-icon="mdi-close-circle"
      class="category-btn mr-1 category text-md-caption"
      @click="onDelete(index)"
      v-for="(category, index) in categories"
      :key="index"
      :ripple="false"
      >{{ category }}</v-btn
    >
  </div>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useMarkdownStore } from '@/stores/markdownStore'
import { postData } from '@/api/apis'
import { showToast } from '@/composables/toast'

const CATEGORY_LIST = [
  '컴퓨터구조',
  '운영체제',
  '자료구조',
  '데이터베이스',
  '네트워크',
  '소프트웨어공학',
  '알고리즘',
  '설계패턴',
  'OOP',
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

const { categories, content } = storeToRefs(useMarkdownStore())

const isRecClicked = ref(false)
const recommendedCategories = ref([])
const selected = ref([false, false, false])

const onClose = (prop: Ref<boolean>): void => {
  prop.value = false
}

const onDelete = (index: number): void => {
  categories.value.splice(index, 1)
}

const onClick = (newCategory: string): void => {
  if (categories.value.includes(newCategory)) {
    categories.value = categories.value.filter((category) => category !== newCategory)
    return
  }
  categories.value.push(newCategory)
}

const onStore = (prop: Ref<boolean>): void => {
  categories.value = recommendedCategories.value.filter((_, index) => selected.value[index])
  prop.value = false
}

const getRecCategory = async (): Promise<void> => {
  recommendedCategories.value = []
  selected.value = [false, false, false]
  if (content.value.trim() === '') return
  try {
    const res = await postData('/memo/recommend', { content: content.value })
    recommendedCategories.value = res
  } catch {
    showToast('error', '요청 실패')
  }
}
</script>

<style scoped>
#accept-btn {
  background-color: #0c3324;
  color: white;
}
#cancel-btn {
  background-color: grey;
  color: white;
}
.alert-msg {
  color: #ea4335;
}
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
.category-list::-webkit-scrollbar {
  width: 6px;
  background-color: #67a58d;
  border-radius: 6px;
}
.category-list::-webkit-scrollbar-thumb {
  background-color: #0c3324;
  border-radius: 6px;
}
.category-list::-webkit-scrollbar-button {
  display: none;
}
@keyframes jiggle {
  0% {
    transform: rotate(-2deg);
  }
  25% {
    transform: rotate(2deg);
  }
  50% {
    transform: rotate(-2deg);
  }
  75% {
    transform: rotate(2deg);
  }
  100% {
    transform: rotate(-2deg);
  }
}
.jiggle {
  animation: jiggle 0.5s infinite;
}
.jiggle-stop {
  animation-play-state: paused;
}
</style>

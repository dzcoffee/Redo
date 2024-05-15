<template>
  <h1 class="title px-3">{{ markdownStore.title }}</h1>
  <div class="pa-3 d-flex" v-if="markdownStore.categories">
    <v-btn
      rounded
      color="#0C3324"
      class="mr-1 category text-md-caption"
      v-for="(category, index) in markdownStore.categories"
      :key="index"
      :ripple="false"
      >{{ category }}</v-btn
    >
  </div>
  <div class="preview-box pa-3" v-html="content"></div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { getDataById } from '@/api/apis'
import { marked } from 'marked'
import { useMarkdownStore } from '@/stores/markdownStore'
import { useRoute } from 'vue-router'

const markdownStore = useMarkdownStore()
const route = useRoute()
const content = computed(() => {
  let changedText = marked(markdownStore.content) as string
  changedText = changedText.replaceAll('&lt;', '<')
  changedText = changedText.replaceAll('&gt;', '>')
  changedText = changedText.replaceAll('&quot;', '"')
  return changedText
})

onMounted(async () => {
  marked.setOptions({
    renderer: new marked.Renderer(),
    gfm: true,
    breaks: true,
    pedantic: false
  })
  const res = await getDataById('/memo', route.params.id as string)
  markdownStore.title = res.title
  markdownStore.content = res.content
  markdownStore.categories = res.categories
})
</script>

<style scoped>
.preview-box {
  max-width: 100%;
  height: calc(100vh - 100px);
  text-align: left;
  overflow-wrap: break-word;
  overflow-x: hidden;
  font-size: 18px;
}
.preview-box::-webkit-scrollbar {
  width: 6px;
  background-color: #f0f0f0;
  border-radius: 6px;
}

.preview-box::-webkit-scrollbar-thumb {
  background-color: #67a58d;
  border-radius: 6px;
}
.category {
  height: 24px;
}
.title {
  color: #67a58d;
}
</style>

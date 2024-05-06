<template>
  <h3>{{ title }}</h3>
  <div class="preview-box pt-3" v-html="preview"></div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { marked } from "marked";
import { storeToRefs } from "pinia";
import { useMarkdownStore } from "@/stores/markdownStore";

const { title, content } = storeToRefs(useMarkdownStore());

const preview = computed(() => {
  let changedText = marked(content.value) as string;
  changedText = changedText.replaceAll("&lt;", "<");
  changedText = changedText.replaceAll("&gt;", ">");
  changedText = changedText.replaceAll("&quot;", '"');
  return changedText;
});

onMounted(() => {
  marked.setOptions({
    renderer: new marked.Renderer(),
    gfm: true,
    breaks: true,
    pedantic: false,
  });
});
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
    background-color: #67A58D;
    border-radius: 6px;
}
</style>

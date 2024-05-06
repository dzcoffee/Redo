<template>
  <v-row class="my-3" align="center">
    <v-btn class="choice-btn" elevation="0" color="#67A58D">{{ index + 1 }}</v-btn>
    <span class="pl-4">{{ content }}</span>
  </v-row>
</template>

<script setup lang="ts">

const { index, content } = defineProps({
  index: { type: Number, required: true, default: 0 },
  content: { type: String, required: true, default: '선택지 내용' }
})
</script>

<style scoped>
.choice-btn {
  border-radius: 50%;
  padding: 0;
  min-width: 5px;
  aspect-ratio: 1 / 1;
}
</style>
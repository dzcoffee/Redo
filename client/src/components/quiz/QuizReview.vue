<template>
  <div class="review-container d-flex flex-column align-center justify-center pa-5">
    <span class="mb-2">문제가 마음에 들었나요?</span>
    <div class="d-flex align-center justify-center mb-4">
      <v-icon size="30" v-for="(score, index) in scores" :key="index" class="mx-1 score" :color="scoreColor(score)" @click="onClick(index)"
        >mdi-star</v-icon
      >
    </div>
    <v-btn id="submit-btn">피드백 제출</v-btn>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const { data } = defineProps({
  data: { type: Object, default: () => {}, required: false }
})
const scores = ref([true, true, true, true, true, false, false, false, false, false])
const onClick = (index: number): void => {
  scores.value[index] = true
  scores.value.forEach((_, i) => {
    if (index >= i) scores.value[i] = scores.value[index]
    else scores.value[i] = false
  })
}
const scoreColor = (state: boolean): string => (state ? 'yellow' : 'grey')
console.log(data)
</script>

<style scoped>
#submit-btn {
  background-color: #0c3324;
  color: white;
}
.review-container {
  border-radius: 10px;
  border: 1px solid #999;
}
</style>

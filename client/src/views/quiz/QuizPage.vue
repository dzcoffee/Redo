<template>
  <div class="pa-2 container">
    <v-btn icon="mdi-arrow-left" density="comfortable" color="#FDF8EC" @click="() => router.back()">
    </v-btn>
  </div>
  <v-row class="pa-0 ma-0 container" align="center" justify="center">
    <v-col align="center">
      <h1>문제입니다.</h1>
      <v-card max-width="70%">
        <v-card-title>답을 적으세요.</v-card-title>
        <v-col align="end">
          <v-btn rounded class="submit-btn">정답 보기</v-btn>
        </v-col>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';


const router = useRouter();
</script>

<style scoped>
.container {
  background-color: #FDF8EC;
}
.submit-btn {
  background-color: #335447;
  color: white;
}
</style>
<template>
    <div class="ma-0 pa-2 option-pane">
    <v-btn icon="mdi-arrow-left" density="comfortable" color="#67A58D" @click="() => router.back()">
    </v-btn>
  </div>
  <v-row class="ma-0 preview-pane">
    <v-col cols="6" class="d-flex flex-column">
      <MemoTitle></MemoTitle>
      <hr>
      <MemoCategoryBar></MemoCategoryBar>
      <MemoBox></MemoBox>
      <div class="d-flex justify-end">
        <v-btn class="memo-create-btn mt-2 px-5" @click="onRegister">메모 등록</v-btn>
      </div>
    </v-col>
    <v-col cols="6">
      <MemoPreview></MemoPreview>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { MemoBox, MemoCategoryBar, MemoPreview, MemoTitle } from '@/components/memo';
import { useRouter } from 'vue-router';

const router=  useRouter();

const onRegister = (): void => {
  router.push('/memo');
  }
</script>

<style scoped>
.memo-create-btn{
  background-color: #67A58D;
  color: white;
  font-weight: 600;
}
.option-pane{
  height: 52px;
}
.preview-pane{
  height: calc(100vh - 52px);
}
</style>
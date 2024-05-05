<template>
  <div class="panel user-info">
    <v-row class="info-pane pa-0 ma-0" align="center" justify="space-between">
      <img width="50" src="@/assets/logo.png" class="ma-0" />
      <span class="hello-msg">닉네임의 메모</span>
    </v-row>
    <v-btn class="service-btn ma-1" elevation="1" @click="moveToQuiz">퀴즈 풀기</v-btn>
    <v-col class="d-flex justify-space-between">
      <v-btn class="service-btn memo-create-btn mx-1" elevation="1" @click="moveToMemoList">메모 목록</v-btn>
      <v-btn class="service-btn memo-create-btn" elevation="1" @click="moveToMemoCreate">메모 생성</v-btn>
    </v-col>
  </div>
  <div class="panel memo-list">
    <v-btn v-for="memo, index in memos" :key="index" class="memo-btn my-1" elevation="0" :ripple="false"
      @click="() => moveToMemo(memo.id)">{{ memo.title }}</v-btn>
  </div>
  <div class="panel logout-pane">
    <v-btn class="service-btn my-2" elevation="1" @click="handleLogout">로그아웃</v-btn>
  </div>
</template>

<script setup lang="ts">
import { getData } from '@/api/apis';
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useMemoStore } from '@/stores/memoStore';
import { useRouter } from 'vue-router';

const { memos } = storeToRefs(useMemoStore());
const router = useRouter();
const handleLogout = (): void => {
  router.push('/login');
}
const moveToMemo = (number: string): void => {
  router.push(`/memo/${number}`);
}
const moveToMemoList = (): void => {
  router.push('/memo');
}
const moveToMemoCreate = (): void => {
  router.push(`/memo/create`);
}
const moveToQuiz = (): void => {
  router.push('/quiz');
}

onMounted(async () => {
  memos.value = await getData("/memo");
})
</script>

<style scoped>
.hello-msg {
  color: white;
  font-size: 12px;
  font-weight: 600;
}
.info-pane {
  width: 90%;
  color: white;
  justify-content: space-around;
}
.logout-pane {
  background-color: #0C3324;
  width: 100%;
  height: 70px;
  justify-content: center;
}
.memo-btn {
  width: 225px;
  background-color: #335447;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.memo-btn:hover {
  background-color: #67A58D;
}
.panel {
  padding: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.service-btn {
  font-size: 18px;
  font-weight: 600;
  background-color: #FDF8EC;
}
.memo-create-btn {
  background-color: #335447;
  color: white;
}
.user-info {
  width: 100%;
  height: 160px;
  background-color: #0C3324;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}
.memo-list {
  width: 100%;
  height: calc(100vh - 230px);
  background-color: #335447;
  justify-content: start;
  overflow-y: scroll;
}
.memo-list::-webkit-scrollbar {
  width: 9px;
}
.memo-list::-webkit-scrollbar-thumb {
  background-color: #999;
  /* 스크롤바 채우기 색상 */
  border-radius: 5px;
  /* 스크롤바의 모양 (모서리 둥글기) */
}
.memo-list::-webkit-scrollbar-thumb:hover {
  background-color: #888;
  /* 스크롤바 호버 시 색상 */
}
</style>
<template>
    <v-row class="h-100 pa-0 ma-0" no-gutters>
      <v-col v-if="$route.path !== '/memo/create'" id="welcome-pane" cols="auto" class="pa-0 ma-0 d-flex flex-column align-center justify-start">
        <MainLayout></MainLayout>
      </v-col>
      <v-col id="interact-pane" class="pa-0 ma-0 d-flex flex-column">
        <router-view/>
      </v-col>
    </v-row>
</template>

<script setup lang="ts">
import { getData } from '@/api/apis';
import MainLayout from '@/components/layout/MainLayout.vue';
import { onMounted } from 'vue';
import { useMemoStore } from '@/stores/memoStore';
import { useRoute } from 'vue-router';

const route = useRoute();
const memoStore = useMemoStore();

onMounted(async () => {
  if(route.path.includes('/memo') && (!route.path.includes('create') || !route.path.includes('edit'))){
    memoStore.memos = await getData('/memo');
  }
})
</script>

<style scoped>
#welcome-page {
  min-width: 100%;
  height: 100%;
}
#welcome-pane {
  height: 100%;
  min-width: 260px;
  background-color: #335447;
}
#interact-pane {
  height: 100%;
  background-color: #FBFDFC;
}
</style>
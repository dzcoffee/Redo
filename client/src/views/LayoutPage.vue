<template>
  <v-row class="h-100 pa-0 ma-0" no-gutters>
    <v-col v-if="!isFocused" id="welcome-pane" cols="auto" class="pa-0 ma-0 d-flex flex-column">
      <MainLayout></MainLayout>
    </v-col>
    <v-col id="interact-pane" class="pa-0 ma-0 d-flex flex-column">
      <router-view :key="route.fullPath" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isFocused = computed(() => {
  return route.path.includes('/create') || route.path.includes('/game')
})
</script>

<style scoped>
#welcome-page {
  min-width: 100%;
  height: 100%;
}
#welcome-pane {
  height: 100%;
  min-width: 200px;
  background-color: #335447;
}
#interact-pane {
  height: 100%;
  background-color: #fbfdfc;
}
</style>

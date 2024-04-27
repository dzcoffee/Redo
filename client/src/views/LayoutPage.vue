<template>
    <v-row class="h-100 pa-0 ma-0" no-gutters>
      <v-col id="welcome-pane" cols="auto" class="pa-0 ma-0 d-flex flex-column align-center justify-start">
        <MainLayout></MainLayout>
      </v-col>
      <v-col id="login-pane" cols="auto" class="pa-0 ma-0 d-flex flex-column align-center justify-center">
        <router-view/>
      </v-col>
    </v-row>
</template>

<script setup lang="ts">
import MainLayout from '@/components/layout/MainLayout.vue';
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
#login-pane {
  height: 100%;
  width: calc(100% - 260px);
  background-color: #FBFDFC;
}
</style>
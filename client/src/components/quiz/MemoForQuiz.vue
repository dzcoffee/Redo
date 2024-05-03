<template>
    <v-btn class="memo-for-quiz my-2" elevation="0" :style="{'background-color': isSelected ? '#335447' : '#67A58D'}" 
    @click="isSelected = !isSelected" :append-icon="isSelected ? 'mdi-check-circle' : ''">
    <span class="text-body-1">메모 목록</span>
    </v-btn>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const isSelected = ref(false);
</script>

<style scoped>
.memo-for-quiz{
    width: 90%;
    color: white;
    border-radius: 10px;
}
</style>
<template>
    <v-btn class="memo-for-quiz my-2" elevation="0" :style="{'background-color': isSelected ? '#335447' : '#67A58D'}" 
    :append-icon="isSelected ? 'mdi-check-circle' : ''">
    <span class="text-body-1">{{ memo.title }}</span>
    </v-btn>
</template>

<script setup lang="ts">
import type { Memo } from '@/domain/type';
import { type PropType } from 'vue';

const {isSelected, memo} = defineProps({
    isSelected: {type: Boolean, required: false, default: false},
    memo: {type: Object as PropType<Memo>, default: {} as Memo, required: false}
})
</script>

<style scoped>
.memo-for-quiz{
    width: 90%;
    color: white;
    border-radius: 10px;
}
</style>
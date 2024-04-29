<template>
    <v-row class="ma-0 pa-0">
        <v-col class="ma-0" align="center">
            <QuizSelectBox></QuizSelectBox>
        </v-col>
        <v-col class="ma-0">
            <QuizSettingBox></QuizSettingBox>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
import QuizSelectBox from '@/components/quiz/QuizSelectBox.vue';
import QuizSettingBox from '@/components/quiz/QuizSettingBox.vue';
</script>

<style scoped>

</style>
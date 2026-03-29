<script setup lang="ts">
defineProps<{ loading: boolean }>()
const emit = defineEmits<{ (e: 'submit', topic: string, level: string): void }>()

const topic = ref('')
const level = ref('B1')
const levels = ['A1', 'A2', 'B1', 'B2', 'C1']

function submit() {
  if (!topic.value.trim()) return
  emit('submit', topic.value.trim(), level.value)
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="520" class="pa-6">
      <v-card-title class="text-h5 font-weight-bold mb-2">English Practice</v-card-title>
      <v-card-subtitle class="mb-6">Введи тему для разговора и получи текст для пересказа</v-card-subtitle>
      <v-card-text class="pa-0">
        <v-form @submit.prevent="submit">
          <v-text-field v-model="topic" label="Тема" placeholder="animals, travel, technology..."
            prepend-inner-icon="mdi-book-open-outline" autofocus :disabled="loading" class="mb-4" />
          <div class="d-flex align-center gap-3 mb-6">
            <span class="text-body-2 text-medium-emphasis">Уровень:</span>
            <v-btn-toggle v-model="level" mandatory density="compact" color="primary">
              <v-btn v-for="l in levels" :key="l" :value="l" size="small">{{ l }}</v-btn>
            </v-btn-toggle>
          </div>
          <v-btn type="submit" color="primary" size="large" block :loading="loading"
            :disabled="!topic.trim()" prepend-icon="mdi-play-circle-outline">
            Начать тренировку
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

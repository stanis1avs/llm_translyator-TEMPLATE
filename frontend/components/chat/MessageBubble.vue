<script setup lang="ts">
import type { ChatMessage } from '~/types/protocol'
defineProps<{ message: ChatMessage }>()
function formatTime(date: Date) {
  return new Date(date).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div v-if="message.role === 'assistant'" class="mb-4">
    <v-card color="surface" variant="elevated" class="pa-4">
      <div class="d-flex align-center gap-2 mb-3">
        <v-icon color="primary" size="18">mdi-robot-outline</v-icon>
        <span class="text-caption text-medium-emphasis font-weight-medium">ТЕКСТ ДЛЯ ПЕРЕСКАЗА</span>
        <v-spacer />
        <span class="text-caption text-medium-emphasis">{{ formatTime(message.timestamp) }}</span>
      </div>
      <p class="text-body-1 font-weight-medium mb-3" style="line-height: 1.8">{{ message.content }}</p>
      <v-divider class="mb-3" />
      <p class="text-body-2 text-medium-emphasis" style="line-height: 1.7">{{ message.translation }}</p>
    </v-card>
  </div>
  <div v-else-if="message.role === 'user'" class="mb-4 d-flex justify-end">
    <v-card color="primary" variant="tonal" class="pa-4" style="max-width: 75%">
      <div class="d-flex align-center gap-2 mb-2">
        <v-icon size="16">mdi-microphone</v-icon>
        <span class="text-caption font-weight-medium">ВАШ ПЕРЕСКАЗ</span>
        <v-spacer />
        <span class="text-caption opacity-70">{{ formatTime(message.timestamp) }}</span>
      </div>
      <p class="text-body-2 mb-2">{{ message.content }}</p>
      <p v-if="message.translation" class="text-caption opacity-70">{{ message.translation }}</p>
    </v-card>
  </div>
</template>

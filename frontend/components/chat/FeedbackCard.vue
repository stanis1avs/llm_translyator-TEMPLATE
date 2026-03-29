<script setup lang="ts">
import type { FeedbackCompleteMsg } from '~/types/protocol'
defineProps<{ feedback: FeedbackCompleteMsg; timestamp: Date }>()
function scoreColor(s: number) { return s >= 80 ? 'success' : s >= 60 ? 'warning' : 'error' }
function formatTime(date: Date) {
  return new Date(date).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div class="mb-4">
    <v-card variant="outlined" class="pa-4">
      <div class="d-flex align-center gap-2 mb-4">
        <v-icon color="secondary" size="18">mdi-clipboard-check-outline</v-icon>
        <span class="text-caption text-medium-emphasis font-weight-medium">ОБРАТНАЯ СВЯЗЬ</span>
        <v-spacer />
        <v-chip :color="scoreColor(feedback.score)" size="small" variant="flat" class="font-weight-bold">
          {{ feedback.score }}/100
        </v-chip>
        <span class="text-caption text-medium-emphasis ml-2">{{ formatTime(timestamp) }}</span>
      </div>
      <p class="text-body-2 mb-4">{{ feedback.overall_comment }}</p>
      <div v-if="feedback.grammar_errors.length" class="mb-4">
        <div class="d-flex align-center gap-1 mb-2">
          <v-icon size="14" color="error">mdi-alert-circle-outline</v-icon>
          <span class="text-caption font-weight-bold text-error">Грамматика ({{ feedback.grammar_errors.length }})</span>
        </div>
        <v-card v-for="(err, i) in feedback.grammar_errors" :key="i"
          color="error" variant="tonal" class="pa-3 mb-2" rounded="md">
          <div class="text-body-2">
            <span style="text-decoration: line-through; opacity: 0.7">{{ err.original }}</span>
            <v-icon size="14" class="mx-1">mdi-arrow-right</v-icon>
            <span class="font-weight-medium">{{ err.correction }}</span>
          </div>
          <div class="text-caption text-medium-emphasis mt-1">{{ err.explanation }}</div>
        </v-card>
      </div>
      <div v-if="feedback.vocabulary_suggestions.length" class="mb-4">
        <div class="d-flex align-center gap-1 mb-2">
          <v-icon size="14" color="warning">mdi-lightbulb-outline</v-icon>
          <span class="text-caption font-weight-bold text-warning">Словарь ({{ feedback.vocabulary_suggestions.length }})</span>
        </div>
        <v-card v-for="(s, i) in feedback.vocabulary_suggestions" :key="i"
          color="warning" variant="tonal" class="pa-3 mb-2" rounded="md">
          <div class="text-body-2">
            <span class="opacity-60">{{ s.word }}</span>
            <v-icon size="14" class="mx-1">mdi-arrow-right</v-icon>
            <span class="font-weight-medium">{{ s.alternative }}</span>
          </div>
          <div class="text-caption text-medium-emphasis mt-1 font-italic">{{ s.context }}</div>
        </v-card>
      </div>
      <div v-if="feedback.missed_key_points.length">
        <div class="d-flex align-center gap-1 mb-2">
          <v-icon size="14" color="info">mdi-information-outline</v-icon>
          <span class="text-caption font-weight-bold text-info">Пропущено</span>
        </div>
        <ul class="text-body-2 text-medium-emphasis pl-4">
          <li v-for="(p, i) in feedback.missed_key_points" :key="i">{{ p }}</li>
        </ul>
      </div>
    </v-card>
  </div>
</template>

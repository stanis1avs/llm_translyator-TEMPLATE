<script setup lang="ts">
const emit = defineEmits<{ (e: 'transcript', transcript: string): void }>()
const recorderStore = useRecorderStore()
const { startRecording, stopRecording, isSupported } = useMediaRecorder()
const { uploadAudio } = useAudioUpload()
const error = ref<string | null>(null)

async function toggle() {
  error.value = null
  if (recorderStore.isRecording) { stopRecording(); return }
  if (!isSupported()) { error.value = 'Браузер не поддерживает запись микрофона'; return }
  try {
    await startRecording(async (blob) => {
      try { const t = await uploadAudio(blob); if (t) emit('transcript', t) }
      catch (e: any) { error.value = e.message || 'Ошибка транскрипции' }
    })
  } catch (e: any) { error.value = e.message || 'Нет доступа к микрофону' }
}

function formatTime(sec: number) {
  return `${Math.floor(sec / 60).toString().padStart(2, '0')}:${(sec % 60).toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="d-flex flex-column align-center gap-2">
    <v-btn :color="recorderStore.isRecording ? 'error' : 'primary'" :loading="recorderStore.isUploading"
      size="x-large" :icon="recorderStore.isRecording ? 'mdi-stop' : 'mdi-microphone'"
      :class="{ 'mic-pulse': recorderStore.isRecording }" @click="toggle" />
    <div class="text-center">
      <div v-if="recorderStore.isRecording" class="text-body-2 text-error font-weight-medium">
        Запись {{ formatTime(recorderStore.elapsedSeconds) }}
      </div>
      <div v-else-if="recorderStore.isUploading" class="text-body-2 text-medium-emphasis">Обработка...</div>
      <div v-else class="text-caption text-medium-emphasis">Нажми для записи пересказа</div>
    </div>
    <v-alert v-if="error" type="error" density="compact" variant="tonal" closable @click:close="error = null">
      {{ error }}
    </v-alert>
  </div>
</template>

<style scoped>
@keyframes pulse-ring { 0% { box-shadow: 0 0 0 0 rgba(var(--v-theme-error), 0.5); } 70% { box-shadow: 0 0 0 14px rgba(var(--v-theme-error), 0); } 100% { box-shadow: 0 0 0 0 rgba(var(--v-theme-error), 0); } }
.mic-pulse { animation: pulse-ring 1.5s infinite; }
</style>

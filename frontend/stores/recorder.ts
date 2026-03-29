import { defineStore } from 'pinia'

export const useRecorderStore = defineStore('recorder', () => {
  const isRecording = ref(false)
  const isUploading = ref(false)
  const transcript = ref<string | null>(null)
  const elapsedSeconds = ref(0)
  let timer: ReturnType<typeof setInterval> | null = null

  function startRecording() {
    isRecording.value = true; elapsedSeconds.value = 0
    timer = setInterval(() => { elapsedSeconds.value++ }, 1000)
  }
  function stopRecording() {
    isRecording.value = false
    if (timer) { clearInterval(timer); timer = null }
  }
  function reset() {
    isRecording.value = false; isUploading.value = false
    transcript.value = null; elapsedSeconds.value = 0
    if (timer) { clearInterval(timer); timer = null }
  }

  return { isRecording, isUploading, transcript, elapsedSeconds, startRecording, stopRecording, reset }
})

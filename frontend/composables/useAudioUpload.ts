export const useAudioUpload = () => {
  const config = useRuntimeConfig()
  const recorderStore = useRecorderStore()

  async function uploadAudio(blob: Blob, filename = 'recording.webm'): Promise<string> {
    recorderStore.isUploading = true
    const formData = new FormData()
    formData.append('file', blob, filename)
    try {
      const res = await fetch(`${config.public.apiBase}/api/v1/transcribe`, {
        method: 'POST', body: formData,
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Upload failed' }))
        throw new Error(err.detail || 'Transcription failed')
      }
      const data: { transcript: string } = await res.json()
      recorderStore.transcript = data.transcript
      return data.transcript
    } finally {
      recorderStore.isUploading = false
    }
  }

  return { uploadAudio }
}

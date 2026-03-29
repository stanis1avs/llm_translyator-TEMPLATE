export const useMediaRecorder = () => {
  const recorderStore = useRecorderStore()

  let mediaRecorder: MediaRecorder | null = null
  let chunks: Blob[] = []
  let stream: MediaStream | null = null
  let onStop: ((blob: Blob) => void) | null = null

  async function startRecording(callback: (blob: Blob) => void): Promise<void> {
    onStop = callback
    stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    chunks = []

    const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
      ? 'audio/webm;codecs=opus'
      : MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : ''

    mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined)
    mediaRecorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data) }
    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: mediaRecorder?.mimeType || 'audio/webm' })
      stream?.getTracks().forEach(t => t.stop())
      stream = null
      onStop?.(blob)
    }
    mediaRecorder.start(250)
    recorderStore.startRecording()
  }

  function stopRecording() {
    if (mediaRecorder?.state !== 'inactive') mediaRecorder?.stop()
    recorderStore.stopRecording()
  }

  function isSupported() {
    return typeof MediaRecorder !== 'undefined' && !!navigator.mediaDevices?.getUserMedia
  }

  return { startRecording, stopRecording, isSupported }
}

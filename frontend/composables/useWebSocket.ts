import type { ServerMessage, ClientMessage } from '~/types/protocol'

export const useWebSocket = () => {
  const config = useRuntimeConfig()
  const chatStore = useChatStore()
  const progressStore = useProgressStore()

  let ws: WebSocket | null = null
  const isConnected = ref(false)
  const error = ref<string | null>(null)

  function connect(sessionId: string) {
    ws = new WebSocket(`${config.public.wsBase}/ws/${sessionId}`)
    ws.onopen = () => { isConnected.value = true; error.value = null }
    ws.onclose = () => { isConnected.value = false }
    ws.onerror = () => { error.value = 'WebSocket connection error'; isConnected.value = false }
    ws.onmessage = (event: MessageEvent) => {
      try { handleMessage(JSON.parse(event.data) as ServerMessage) }
      catch { console.error('Failed to parse WS message', event.data) }
    }
  }

  function handleMessage(msg: ServerMessage) {
    switch (msg.type) {
      case 'text_chunk':
        chatStore.isStreaming = true; chatStore.appendStreamingToken(msg.content); break
      case 'text_complete':
        chatStore.finalizeAssistantMessage(msg.text, msg.translation)
        chatStore.phase = 'waiting_speech'; break
      case 'feedback_chunk':
        chatStore.isStreaming = true; chatStore.appendStreamingToken(msg.content); break
      case 'feedback_complete':
        chatStore.streamingContent = ''; chatStore.isStreaming = false
        chatStore.addFeedbackMessage(msg); chatStore.phase = 'waiting_speech'; break
      case 'progress_update':
        progressStore.update(msg.recurring_issues, msg.suggested_focus); break
      case 'error':
        error.value = msg.message; chatStore.isStreaming = false
        chatStore.streamingContent = ''; break
    }
  }

  function send(msg: ClientMessage) {
    if (ws?.readyState === WebSocket.OPEN) ws.send(JSON.stringify(msg))
  }

  function disconnect() { ws?.close(); ws = null; isConnected.value = false }

  function generateText(topic: string, level = 'B1') {
    chatStore.phase = 'generating'; chatStore.isStreaming = true; chatStore.streamingContent = ''
    send({ type: 'generate_text', topic, level: level as any })
  }

  function analyseSpeech(transcript: string) {
    chatStore.phase = 'analysing'; chatStore.isStreaming = true; chatStore.streamingContent = ''
    send({ type: 'analyse_speech', transcript })
  }

  return { isConnected, error, connect, disconnect, generateText, analyseSpeech, send }
}

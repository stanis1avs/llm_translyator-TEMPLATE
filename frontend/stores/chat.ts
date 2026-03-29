import { defineStore } from 'pinia'
import type { ChatMessage, FeedbackCompleteMsg, Session } from '~/types/protocol'

export const useChatStore = defineStore('chat', () => {
  const sessionId = ref<string | null>(null)
  const currentSession = ref<Session | null>(null)
  const messages = ref<ChatMessage[]>([])
  const streamingContent = ref('')
  const isStreaming = ref(false)
  const phase = ref<'idle' | 'generating' | 'waiting_speech' | 'analysing'>('idle')
  const sessions = ref<Session[]>([])

  function addMessage(msg: Omit<ChatMessage, 'id' | 'timestamp'>): ChatMessage {
    const full: ChatMessage = { ...msg, id: crypto.randomUUID(), timestamp: new Date() }
    messages.value.push(full)
    return full
  }

  function appendStreamingToken(token: string) { streamingContent.value += token }

  function finalizeAssistantMessage(text: string, translation: string) {
    streamingContent.value = ''
    isStreaming.value = false
    addMessage({ role: 'assistant', content: text, translation })
  }

  function addUserMessage(transcript: string, translation?: string) {
    addMessage({ role: 'user', content: transcript, translation })
  }

  function addFeedbackMessage(feedback: FeedbackCompleteMsg) {
    addMessage({ role: 'feedback', content: feedback.overall_comment, feedback })
  }

  function startSession(session: Session) {
    sessionId.value = session.id
    currentSession.value = session
    messages.value = []
    streamingContent.value = ''
    isStreaming.value = false
    phase.value = 'idle'
  }

  function loadSession(session: Session, history: ChatMessage[]) {
    sessionId.value = session.id
    currentSession.value = session
    messages.value = history
    streamingContent.value = ''
    isStreaming.value = false
    phase.value = 'idle'
  }

  function reset() {
    sessionId.value = null; currentSession.value = null; messages.value = []
    streamingContent.value = ''; isStreaming.value = false; phase.value = 'idle'
  }

  return {
    sessionId, currentSession, messages, streamingContent, isStreaming, phase, sessions,
    addMessage, appendStreamingToken, finalizeAssistantMessage,
    addUserMessage, addFeedbackMessage, startSession, loadSession, reset,
  }
})

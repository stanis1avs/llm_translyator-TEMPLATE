<script setup lang="ts">
import type { ChatMessage } from '~/types/protocol'

const props = defineProps<{
  messages: ChatMessage[]; streamingContent: string; isStreaming: boolean; phase: string
}>()

const container = ref<HTMLElement | null>(null)

function scrollToBottom() {
  nextTick(() => { if (container.value) container.value.scrollTop = container.value.scrollHeight })
}

watch(() => props.messages.length, scrollToBottom)
watch(() => props.streamingContent, scrollToBottom)
</script>

<template>
  <div ref="container" class="chat-container">
    <template v-for="msg in messages" :key="msg.id">
      <ChatFeedbackCard v-if="msg.role === 'feedback' && msg.feedback" :feedback="msg.feedback" :timestamp="msg.timestamp" />
      <ChatMessageBubble v-else :message="msg" />
    </template>
    <div v-if="isStreaming && streamingContent" class="mb-4">
      <v-card color="surface" variant="elevated" class="pa-4">
        <div class="d-flex align-center gap-2 mb-2">
          <v-icon color="primary" size="18">mdi-robot-outline</v-icon>
          <ChatTypingIndicator :label="phase === 'analysing' ? 'Анализирую...' : 'Генерирую текст...'" />
        </div>
        <p class="text-body-2 text-medium-emphasis" style="white-space: pre-wrap">{{ streamingContent }}</p>
      </v-card>
    </div>
    <div v-else-if="isStreaming" class="mb-4 px-2">
      <ChatTypingIndicator :label="phase === 'analysing' ? 'Анализирую пересказ...' : 'Генерирую текст...'" />
    </div>
  </div>
</template>

<style scoped>
.chat-container { flex: 1; overflow-y: auto; padding: 16px; scroll-behavior: smooth; }
.chat-container::-webkit-scrollbar { width: 6px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 3px; }
</style>

<script setup lang="ts">
const chatStore = useChatStore()
const progressStore = useProgressStore()
const recorderStore = useRecorderStore()
const { createSession, listSessions, loadSession, deleteSession } = useSession()
const ws = useWebSocket()

const loading = ref(false)
const wsError = ref<string | null>(null)
const drawer = ref(false)

watchEffect(() => { wsError.value = ws.error.value })
onMounted(() => listSessions().catch(() => {}))

async function handleTopicSubmit(topic: string, level: string) {
  loading.value = true; wsError.value = null
  try {
    const session = await createSession(topic, level)
    await listSessions()
    ws.connect(session.id)
    await new Promise<void>((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('WS connection timeout')), 5000)
      const stop = watch(ws.isConnected, (connected) => {
        if (connected) { clearTimeout(timeout); stop(); resolve() }
      })
    })
    ws.generateText(topic, level)
  } catch (e: any) {
    wsError.value = e.message || 'Ошибка подключения'; chatStore.reset()
  } finally {
    loading.value = false
  }
}

async function handleLoadSession(sessionId: string) {
  if (chatStore.sessionId === sessionId) return
  ws.disconnect(); await loadSession(sessionId); ws.connect(sessionId); drawer.value = false
}

async function handleTranscript(transcript: string) {
  recorderStore.reset(); ws.analyseSpeech(transcript)
}

function handleNextCycle() {
  const topic = chatStore.currentSession?.topic || ''
  const level = chatStore.currentSession?.level || 'B1'
  chatStore.isStreaming = true; chatStore.streamingContent = ''; chatStore.phase = 'generating'
  ws.generateText(topic, level)
}

function handleNewSession() {
  ws.disconnect(); chatStore.reset(); progressStore.reset(); recorderStore.reset()
}

const showMic = computed(() => chatStore.phase === 'waiting_speech' && !recorderStore.isUploading)
const showNextCycle = computed(() =>
  chatStore.phase === 'waiting_speech' && chatStore.messages.some(m => m.role === 'feedback')
)
</script>

<template>
  <v-layout style="height: 100vh; background: rgb(var(--v-theme-background))">
    <v-navigation-drawer v-model="drawer" temporary width="300">
      <v-list-item title="История сессий" prepend-icon="mdi-history" class="py-4" />
      <v-divider />
      <v-list density="compact" nav>
        <v-list-item
          v-for="s in chatStore.sessions" :key="s.id"
          :title="s.topic" :subtitle="new Date(s.created_at).toLocaleDateString('ru-RU')"
          :active="chatStore.sessionId === s.id" active-color="primary"
          rounded="lg" class="mb-1" @click="handleLoadSession(s.id)"
        >
          <template #append>
            <v-btn icon="mdi-delete-outline" size="x-small" variant="text" @click.stop="deleteSession(s.id)" />
          </template>
        </v-list-item>
        <v-list-item v-if="!chatStore.sessions.length" class="text-medium-emphasis text-caption">
          Нет сохранённых сессий
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main style="display: flex; flex-direction: column; height: 100vh">
      <v-app-bar flat border="b" density="compact" color="surface">
        <v-app-bar-nav-icon @click="drawer = !drawer" />
        <v-app-bar-title>
          <span class="font-weight-bold">llmTranslyator</span>
          <v-chip v-if="chatStore.currentSession" size="x-small" class="ml-2" variant="tonal" color="primary">
            {{ chatStore.currentSession.topic }} · {{ chatStore.currentSession.level }}
          </v-chip>
        </v-app-bar-title>
        <template #append>
          <v-btn v-if="chatStore.sessionId" size="small" variant="text" prepend-icon="mdi-plus" @click="handleNewSession">
            Новая сессия
          </v-btn>
        </template>
      </v-app-bar>

      <TopicInput v-if="!chatStore.sessionId" :loading="loading" @submit="handleTopicSubmit" />

      <template v-else>
        <div v-if="progressStore.recurringIssues.length"
          class="d-flex flex-wrap gap-2 px-4 py-2"
          style="border-bottom: 1px solid rgba(255,255,255,0.08)"
        >
          <v-chip v-for="issue in progressStore.recurringIssues.slice(0, 4)" :key="issue.description"
            size="x-small" variant="tonal" color="warning" prepend-icon="mdi-alert-outline"
          >{{ issue.description }}</v-chip>
        </div>

        <ChatContainer
          :messages="chatStore.messages" :streaming-content="chatStore.streamingContent"
          :is-streaming="chatStore.isStreaming" :phase="chatStore.phase"
          style="flex: 1; overflow-y: auto"
        />

        <div class="pa-4 d-flex flex-column align-center gap-3" style="border-top: 1px solid rgba(255,255,255,0.08)">
          <RecorderMicButton v-if="showMic" @transcript="handleTranscript" />
          <v-btn v-if="showNextCycle && !recorderStore.isRecording"
            color="secondary" variant="tonal" prepend-icon="mdi-refresh" @click="handleNextCycle"
          >Следующий текст</v-btn>
          <v-alert v-if="wsError" type="error" density="compact" variant="tonal" closable @click:close="wsError = null">
            {{ wsError }}
          </v-alert>
        </div>
      </template>
    </v-main>
  </v-layout>
</template>

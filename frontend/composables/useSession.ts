import type { Session, ChatMessage } from '~/types/protocol'

export const useSession = () => {
  const config = useRuntimeConfig()
  const chatStore = useChatStore()
  const base = config.public.apiBase

  async function createSession(topic: string, level = 'B1'): Promise<Session> {
    const res = await fetch(`${base}/api/v1/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, level }),
    })
    if (!res.ok) throw new Error('Failed to create session')
    const session: Session = await res.json()
    chatStore.startSession(session)
    return session
  }

  async function listSessions(): Promise<Session[]> {
    const res = await fetch(`${base}/api/v1/sessions`)
    if (!res.ok) throw new Error('Failed to list sessions')
    const sessions: Session[] = await res.json()
    chatStore.sessions = sessions
    return sessions
  }

  async function loadSession(sessionId: string): Promise<void> {
    const res = await fetch(`${base}/api/v1/sessions/${sessionId}`)
    if (!res.ok) throw new Error('Session not found')
    const data = await res.json()
    const history: ChatMessage[] = data.messages.map((m: any) => ({
      id: String(m.id), role: m.role, content: m.content,
      translation: m.translation ?? undefined, timestamp: new Date(m.created_at),
    }))
    chatStore.loadSession(
      { id: data.id, topic: data.topic, level: data.level, created_at: data.created_at },
      history,
    )
  }

  async function deleteSession(sessionId: string): Promise<void> {
    await fetch(`${base}/api/v1/sessions/${sessionId}`, { method: 'DELETE' })
    chatStore.sessions = chatStore.sessions.filter(s => s.id !== sessionId)
  }

  return { createSession, listSessions, loadSession, deleteSession }
}

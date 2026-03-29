// ── Client → Server ──────────────────────────────────────────────────────────

export interface GenerateTextMsg {
  type: 'generate_text'
  topic: string
  level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1'
}

export interface AnaliseSpeechMsg {
  type: 'analyse_speech'
  transcript: string
}

export type ClientMessage = GenerateTextMsg | AnaliseSpeechMsg | { type: 'next_cycle'; topic?: string } | { type: 'ping' }

// ── Server → Client ──────────────────────────────────────────────────────────

export interface TextChunkMsg { type: 'text_chunk'; content: string }
export interface TextCompleteMsg {
  type: 'text_complete'; text: string; translation: string
  key_vocabulary: { word: string; translation: string }[]
  target_structures: string[]; message_id: number
}
export interface FeedbackChunkMsg { type: 'feedback_chunk'; content: string }

export interface GrammarError { original: string; correction: string; explanation: string }
export interface VocabSuggestion { word: string; alternative: string; context: string }

export interface FeedbackCompleteMsg {
  type: 'feedback_complete'
  grammar_errors: GrammarError[]
  vocabulary_suggestions: VocabSuggestion[]
  missed_key_points: string[]
  overall_comment: string
  score: number
  new_difficulties: string[]
}

export interface RecurringIssue { category: string; description: string; occurrences: number }

export interface ProgressUpdateMsg {
  type: 'progress_update'; recurring_issues: RecurringIssue[]; suggested_focus: string[]
}

export interface ErrorMsg { type: 'error'; code: string; message: string }

export type ServerMessage =
  | TextChunkMsg | TextCompleteMsg | FeedbackChunkMsg
  | FeedbackCompleteMsg | ProgressUpdateMsg | ErrorMsg | { type: 'pong' }

// ── UI model ─────────────────────────────────────────────────────────────────

export type MessageRole = 'assistant' | 'user' | 'feedback'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  translation?: string
  feedback?: FeedbackCompleteMsg
  timestamp: Date
}

export interface Session {
  id: string; topic: string; level: string; created_at: string
}

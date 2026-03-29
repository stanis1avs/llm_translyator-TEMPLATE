from pydantic import BaseModel
from typing import Literal, Optional


# ── Client → Server ──────────────────────────────────────────────────────────

class GenerateTextMsg(BaseModel):
    type: Literal["generate_text"]
    topic: str
    level: Literal["A1", "A2", "B1", "B2", "C1"] = "B1"


class AnaliseSpeechMsg(BaseModel):
    type: Literal["analyse_speech"]
    transcript: str


class NextCycleMsg(BaseModel):
    type: Literal["next_cycle"]
    topic: Optional[str] = None


# ── Server → Client ──────────────────────────────────────────────────────────

class TextChunkMsg(BaseModel):
    type: Literal["text_chunk"] = "text_chunk"
    content: str


class TextCompleteMsg(BaseModel):
    type: Literal["text_complete"] = "text_complete"
    text: str
    translation: str
    key_vocabulary: list[dict] = []
    target_structures: list[str] = []
    message_id: int


class FeedbackChunkMsg(BaseModel):
    type: Literal["feedback_chunk"] = "feedback_chunk"
    content: str


class GrammarError(BaseModel):
    original: str
    correction: str
    explanation: str


class VocabSuggestion(BaseModel):
    word: str
    alternative: str
    context: str


class IdentifiedDifficulty(BaseModel):
    category: str
    description: str
    example: str


class FeedbackCompleteMsg(BaseModel):
    type: Literal["feedback_complete"] = "feedback_complete"
    grammar_errors: list[GrammarError] = []
    vocabulary_suggestions: list[VocabSuggestion] = []
    missed_key_points: list[str] = []
    overall_comment: str
    score: int
    new_difficulties: list[str] = []


class RecurringIssue(BaseModel):
    category: str
    description: str
    occurrences: int


class ProgressUpdateMsg(BaseModel):
    type: Literal["progress_update"] = "progress_update"
    recurring_issues: list[RecurringIssue] = []
    suggested_focus: list[str] = []


class ErrorMsg(BaseModel):
    type: Literal["error"] = "error"
    code: str
    message: str


class PongMsg(BaseModel):
    type: Literal["pong"] = "pong"

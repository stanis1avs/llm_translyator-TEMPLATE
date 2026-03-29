"""
Progress tracking service.

Tracks recurring difficulties across training cycles and builds
context for adaptive text generation.

This file contains the core learning adaptation logic.
Implement the following functions according to the DB schema.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import Difficulty, Suggestion
from ..schemas.ws_protocol import IdentifiedDifficulty, RecurringIssue


async def extract_and_store_difficulties(
    db: AsyncSession,
    session_id: str,
    identified: list[IdentifiedDifficulty],
) -> None:
    """
    Persist difficulties from LLM feedback.

    TODO: implement matching logic (substring match or embedding similarity).
    """
    raise NotImplementedError


async def get_top_difficulties(
    db: AsyncSession,
    session_id: str,
    limit: int = 5,
) -> list[Difficulty]:
    """Return difficulties ordered by occurrences DESC."""
    raise NotImplementedError


async def get_unshown_suggestions(
    db: AsyncSession,
    session_id: str,
    limit: int = 3,
) -> list[Suggestion]:
    """Return suggestions not yet shown to the user."""
    raise NotImplementedError


async def mark_suggestions_shown(db: AsyncSession, suggestion_ids: list[int]) -> None:
    """Mark suggestions as shown after injecting them into a prompt."""
    raise NotImplementedError


async def build_progress_context_data(
    db: AsyncSession,
    session_id: str,
) -> tuple[list[dict], list[str], list[int]]:
    """
    Returns (difficulties_dicts, suggestion_strings, suggestion_ids_to_mark).
    Called before each text generation to build the adaptive prompt injection.
    """
    raise NotImplementedError


async def build_recurring_issues(
    db: AsyncSession,
    session_id: str,
) -> list[RecurringIssue]:
    """Build progress_update payload for WebSocket response on session connect."""
    raise NotImplementedError

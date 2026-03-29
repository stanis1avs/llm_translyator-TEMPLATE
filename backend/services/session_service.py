import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from ..database.models import TrainingSession, Message


async def create_session(db: AsyncSession, topic: str, level: str = "B1") -> TrainingSession:
    session = TrainingSession(id=str(uuid.uuid4()), topic=topic, level=level)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def get_session(db: AsyncSession, session_id: str) -> TrainingSession | None:
    result = await db.execute(select(TrainingSession).where(TrainingSession.id == session_id))
    return result.scalar_one_or_none()


async def list_sessions(db: AsyncSession) -> list[TrainingSession]:
    result = await db.execute(select(TrainingSession).order_by(desc(TrainingSession.created_at)))
    return list(result.scalars().all())


async def delete_session(db: AsyncSession, session_id: str) -> bool:
    session = await get_session(db, session_id)
    if session is None:
        return False
    await db.delete(session)
    await db.commit()
    return True


async def add_message(
    db: AsyncSession,
    session_id: str,
    role: str,
    content: str,
    translation: str | None = None,
) -> Message:
    result = await db.execute(
        select(Message.sequence_num)
        .where(Message.session_id == session_id)
        .order_by(desc(Message.sequence_num))
        .limit(1)
    )
    last_seq = result.scalar_one_or_none()
    message = Message(
        session_id=session_id,
        role=role,
        content=content,
        translation=translation,
        sequence_num=(last_seq or 0) + 1,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_session_messages(db: AsyncSession, session_id: str) -> list[Message]:
    result = await db.execute(
        select(Message).where(Message.session_id == session_id).order_by(Message.sequence_num)
    )
    return list(result.scalars().all())

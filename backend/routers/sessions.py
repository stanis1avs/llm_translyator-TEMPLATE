from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.engine import get_db
from ..schemas.session import SessionCreate, SessionResponse, SessionWithMessages, MessageResponse
from ..services import session_service

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(body: SessionCreate, db: AsyncSession = Depends(get_db)):
    return await session_service.create_session(db, body.topic, body.level)


@router.get("", response_model=list[SessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    return await session_service.list_sessions(db)


@router.get("/{session_id}", response_model=SessionWithMessages)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    session = await session_service.get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = await session_service.get_session_messages(db, session_id)
    return SessionWithMessages(
        **SessionResponse.model_validate(session).model_dump(),
        messages=[MessageResponse.model_validate(m) for m in messages],
    )


@router.delete("/{session_id}", status_code=204)
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    if not await session_service.delete_session(db, session_id):
        raise HTTPException(status_code=404, detail="Session not found")

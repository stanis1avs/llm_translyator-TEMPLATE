import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..database.engine import AsyncSessionLocal
from ..services import session_service, progress_service
from ..services.llm_service import stream_chat_with_accumulator
from ..prompts.text_generation import build_text_generation_prompt
from ..prompts.feedback import build_feedback_prompt
from ..prompts.progress_context import build_progress_context
from ..schemas.ws_protocol import (
    FeedbackCompleteMsg, ProgressUpdateMsg, TextCompleteMsg,
    ErrorMsg, IdentifiedDifficulty,
)

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    async with AsyncSessionLocal() as db:
        session = await session_service.get_session(db, session_id)
        if session is None:
            await websocket.send_json(
                ErrorMsg(code="session_not_found", message="Session not found").model_dump()
            )
            await websocket.close()
            return

        # TODO: send progress_update on connect if session has difficulty history

        try:
            while True:
                raw = await websocket.receive_text()
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    await websocket.send_json(
                        ErrorMsg(code="invalid_json", message="Message must be valid JSON").model_dump()
                    )
                    continue

                msg_type = msg.get("type")

                if msg_type == "generate_text":
                    # TODO: implement
                    raise NotImplementedError

                elif msg_type == "analyse_speech":
                    # TODO: implement

                    raise NotImplementedError

                elif msg_type == "ping":
                    await websocket.send_json({"type": "pong"})

                else:
                    await websocket.send_json(
                        ErrorMsg(code="unknown_type", message=f"Unknown type: {msg_type}").model_dump()
                    )

        except WebSocketDisconnect:
            pass
        except Exception as e:
            try:
                await websocket.send_json(ErrorMsg(code="server_error", message=str(e)).model_dump())
            except Exception:
                pass

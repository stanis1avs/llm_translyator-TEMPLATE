from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from ..services import stt_service

router = APIRouter(prefix="/api/v1", tags=["transcribe"])


class TranscribeResponse(BaseModel):
    transcript: str


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio type")

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")

    try:
        await stt_service.load_model()
        transcript = stt_service.transcribe(audio_bytes, file.filename or "audio.webm")
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    return TranscribeResponse(transcript=transcript)

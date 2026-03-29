import tempfile
import os
from faster_whisper import WhisperModel
from ..config import settings

_model: WhisperModel | None = None


async def load_model() -> None:
    """Load the Whisper model. Called lazily on first transcription request."""
    global _model
    if _model is None:
        print(f"[stt] Loading model '{settings.stt_model}' on {settings.stt_device}/{settings.stt_compute_type}...")
        _model = WhisperModel(
            settings.stt_model,
            device=settings.stt_device,
            compute_type=settings.stt_compute_type,
        )
        print("[stt] Model loaded.")


def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    if _model is None:
        raise RuntimeError("STT model not loaded. Call load_model() first.")

    suffix = os.path.splitext(filename)[-1] or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        segments, _info = _model.transcribe(
            tmp_path,
            language=settings.stt_language,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
        )
        text = " ".join(seg.text.strip() for seg in segments).strip()
    finally:
        os.unlink(tmp_path)

    return text

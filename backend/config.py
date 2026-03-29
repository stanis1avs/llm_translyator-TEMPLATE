from pydantic import field_validator
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # LLM — set OLLAMA_HOST to remote machine IP if Ollama runs elsewhere
    ollama_model: str = "qwen2.5:7b"
    ollama_host: str = "http://localhost:11434"

    # STT — use "cuda"/"float16" for GPU, "cpu"/"int8" for CPU-only server
    stt_model: str = "small"
    stt_device: str = "cpu"
    stt_compute_type: str = "int8"
    stt_language: str = "en"

    # Database
    db_path: str = str(BASE_DIR / "data" / "app.db")

    # Server CORS — accepts "http://a" or "http://a,http://b" or '["http://a"]'
    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, list):
            return v
        v = str(v).strip().lstrip("[").rstrip("]")
        return [o.strip().strip('"').strip("'") for o in v.split(",") if o.strip()]

    class Config:
        env_file = (
            str(Path(__file__).parent / "dev.env"),
            str(Path(__file__).parent / ".env"),
        )


settings = Settings()

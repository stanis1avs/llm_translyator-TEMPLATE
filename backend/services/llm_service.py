from typing import AsyncGenerator
from ollama import AsyncClient
from ..config import settings

_client = AsyncClient(host=settings.ollama_host)


async def stream_chat(system_prompt: str, user_message: str) -> AsyncGenerator[str, None]:
    """Stream raw token strings from Ollama."""
    async for chunk in await _client.chat(
        model=settings.ollama_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        stream=True,
        options={"temperature": 0.7},
    ):
        token = chunk["message"]["content"]
        if token:
            yield token


async def stream_chat_with_accumulator(
    system_prompt: str,
    user_message: str,
) -> AsyncGenerator[tuple[str, str], None]:
    """Yields (token, accumulated_so_far) tuples for simultaneous streaming and collection."""
    accumulated = ""
    async for token in stream_chat(system_prompt, user_message):
        accumulated += token
        yield token, accumulated

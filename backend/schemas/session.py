from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SessionCreate(BaseModel):
    topic: str
    level: str = "B1"


class SessionResponse(BaseModel):
    id: str
    created_at: datetime
    topic: str
    level: str

    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    translation: Optional[str] = None
    created_at: datetime
    sequence_num: int

    model_config = {"from_attributes": True}


class SessionWithMessages(SessionResponse):
    messages: list[MessageResponse] = []

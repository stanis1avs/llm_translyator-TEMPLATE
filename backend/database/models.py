from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .engine import Base


class TrainingSession(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    topic: Mapped[str] = mapped_column(Text)
    level: Mapped[str] = mapped_column(String(3), default="B1")

    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="session", cascade="all, delete-orphan"
    )
    difficulties: Mapped[list["Difficulty"]] = relationship(
        "Difficulty", back_populates="session", cascade="all, delete-orphan"
    )
    suggestions: Mapped[list["Suggestion"]] = relationship(
        "Suggestion", back_populates="session", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    translation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    sequence_num: Mapped[int] = mapped_column(Integer, default=0)

    session: Mapped["TrainingSession"] = relationship("TrainingSession", back_populates="messages")


class Difficulty(Base):
    __tablename__ = "difficulties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id", ondelete="CASCADE"))
    category: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(Text)
    examples: Mapped[str] = mapped_column(Text, default="[]")
    occurrences: Mapped[int] = mapped_column(Integer, default=1)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    session: Mapped["TrainingSession"] = relationship("TrainingSession", back_populates="difficulties")
    suggestions: Mapped[list["Suggestion"]] = relationship("Suggestion", back_populates="source_difficulty")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id", ondelete="CASCADE"))
    suggestion: Mapped[str] = mapped_column(Text)
    source_difficulty_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("difficulties.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    shown: Mapped[bool] = mapped_column(Boolean, default=False)

    session: Mapped["TrainingSession"] = relationship("TrainingSession", back_populates="suggestions")
    source_difficulty: Mapped["Difficulty | None"] = relationship("Difficulty", back_populates="suggestions")

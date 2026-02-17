from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st
from sqlalchemy import DateTime, Integer, String, Text, create_engine, func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, Session, declarative_base, mapped_column, sessionmaker


@dataclass
class JokeRecord:
    id: int
    created_at: str
    template_key: str
    template_name: str
    user_input: str
    add_on: str
    generated_joke: str


def _secret_or_env(name: str) -> str | None:
    try:
        if name in st.secrets:
            value = st.secrets[name]
            if value is not None and str(value).strip():
                return str(value).strip()
    except Exception:
        pass

    value = os.getenv(name)
    if value is not None and value.strip():
        return value.strip()
    return None


def _default_sqlite_url() -> str:
    base_dir = Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "jokes.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{db_path}"


def _resolve_database_url() -> str:
    raw = _secret_or_env("DATABASE_URL") or _secret_or_env("SUPABASE_DB_URL")
    if raw:
        return raw
    return _default_sqlite_url()


def _normalize_database_url(raw_url: str) -> str:
    if raw_url.startswith("postgres://"):
        return raw_url.replace("postgres://", "postgresql+psycopg://", 1)
    if raw_url.startswith("postgresql://"):
        return raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return raw_url


DATABASE_URL = _normalize_database_url(_resolve_database_url())
IS_SQLITE = DATABASE_URL.startswith("sqlite://")
Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)


class Joke(Base):
    __tablename__ = "jokes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    template_key: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_input: Mapped[str] = mapped_column(Text, nullable=False)
    add_on: Mapped[str] = mapped_column(Text, nullable=False, default="")
    generated_joke: Mapped[str] = mapped_column(Text, nullable=False)


def get_storage_label() -> str:
    if IS_SQLITE:
        return "SQLite (local file)"

    normalized = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://", 1)
    parsed = urlparse(normalized)
    host = parsed.hostname or "supabase"
    return f"Postgres ({host})"


def _to_iso_utc(value: datetime | None) -> str:
    if value is None:
        return ""

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)

    return value.isoformat(timespec="seconds")


def _to_record(joke: Joke) -> JokeRecord:
    return JokeRecord(
        id=joke.id,
        created_at=_to_iso_utc(joke.created_at),
        template_key=joke.template_key,
        template_name=joke.template_name,
        user_input=joke.user_input,
        add_on=joke.add_on,
        generated_joke=joke.generated_joke,
    )


def _session() -> Session:
    return SessionLocal()


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as error:
        raise RuntimeError(f"Could not initialize database ({get_storage_label()}).") from error


def save_joke(
    *,
    template_key: str,
    template_name: str,
    user_input: str,
    add_on: str,
    generated_joke: str,
) -> int:
    session = _session()
    try:
        joke = Joke(
            template_key=template_key,
            template_name=template_name,
            user_input=user_input.strip(),
            add_on=add_on.strip(),
            generated_joke=generated_joke,
        )
        session.add(joke)
        session.commit()
        session.refresh(joke)
        return int(joke.id)
    except SQLAlchemyError as error:
        session.rollback()
        raise RuntimeError("Could not save joke to database.") from error
    finally:
        session.close()


def list_jokes(
    *,
    search_text: str = "",
    template_keys: list[str] | None = None,
    limit: int = 50,
) -> list[JokeRecord]:
    normalized_limit = max(1, min(limit, 500))

    session = _session()
    try:
        statement = select(Joke)

        if search_text.strip():
            like = f"%{search_text.strip()}%"
            statement = statement.where(
                or_(
                    Joke.user_input.ilike(like),
                    Joke.add_on.ilike(like),
                    Joke.generated_joke.ilike(like),
                    Joke.template_name.ilike(like),
                )
            )

        if template_keys:
            statement = statement.where(Joke.template_key.in_(template_keys))

        statement = statement.order_by(Joke.id.desc()).limit(normalized_limit)
        rows = list(session.scalars(statement).all())
        return [_to_record(row) for row in rows]
    except SQLAlchemyError as error:
        raise RuntimeError("Could not read jokes from database.") from error
    finally:
        session.close()


def get_stats() -> tuple[int, str]:
    session = _session()
    try:
        total = session.scalar(select(func.count(Joke.id))) or 0
        latest = session.scalar(select(func.max(Joke.created_at)))
        latest_label = _to_iso_utc(latest) if latest else "No jokes yet"
        return int(total), latest_label
    except SQLAlchemyError as error:
        raise RuntimeError("Could not read database stats.") from error
    finally:
        session.close()

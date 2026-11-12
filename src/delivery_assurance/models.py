"""ORM models for the core schema (ADR 0002).

Only the bookkeeping tables exist so far; the rest arrive in piece 4.
Per ADR 0002 there is no relationship(): foreign keys are plain columns.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Project(Base):
    """One source project, e.g. REFERENCE (the 11 CSVs) or SET_A (Jira)."""

    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(Text, unique=True)
    name: Mapped[str] = mapped_column(Text)


class IngestionRun(Base):
    """One execution of a loader: which adapter, which loader version, when."""

    __tablename__ = "ingestion_run"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    adapter: Mapped[str] = mapped_column(Text)
    loader_version: Mapped[str] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SourceFile(Base):
    """One file read during a run, fingerprinted so a load can be tied to exact bytes."""

    __tablename__ = "source_file"
    id: Mapped[int] = mapped_column(primary_key=True)
    ingestion_run_id: Mapped[int] = mapped_column(ForeignKey("ingestion_run.id"))
    path: Mapped[str] = mapped_column(Text)
    sha256: Mapped[str] = mapped_column(String(64))
    row_count: Mapped[int]

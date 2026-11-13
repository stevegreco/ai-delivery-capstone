"""ORM models for the core schema (ADR 0002).

Per ADR 0002 there is no relationship(): foreign keys are plain columns.
Mapped[str] means NOT NULL; Mapped[str | None] means the column is optional.
"""

from datetime import date, datetime
from typing import Any

from sqlalchemy import (CheckConstraint, Date, DateTime, ForeignKey, MetaData,
                        String, Text, UniqueConstraint)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Readable constraint names in the DDL and in error messages,
# e.g. ck_requirement_priority instead of an auto-generated one.
NAMING = {"ck": "ck_%(table_name)s_%(constraint_name)s",
          "uq": "uq_%(table_name)s_%(column_0_N_name)s",
          "fk": "fk_%(table_name)s_%(column_0_name)s"}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING)


# The agreed values for every enum column, defined once (data profile, W2-02).
# Used by the CHECK constraints below and by the data-quality checks.
ALLOWED: dict[str, dict[str, tuple[str, ...]]] = {
    "requirement": {"priority": ("P0", "P1", "P2", "P3"),
                    "status": ("DRAFT", "REVIEW", "APPROVED"),
                    "approval_status": ("PENDING_REVIEW", "APPROVED")},
    "acceptance_criterion": {"status": ("DRAFT", "APPROVED")},
    "test_case": {"status": ("ACTIVE", "NEEDS_REVIEW")},
    "trace_link": {"link_type": ("VERIFIES",), "status": ("ACTIVE",)},
    "test_execution": {"outcome": ("PASS", "FAIL", "NOT_RUN", "BLOCKED")},
    "defect": {"severity": ("S1", "S2", "S3", "S4"),
               "status": ("OPEN", "IN_PROGRESS", "FIXED", "CLOSED")},
    "dq_issue": {"severity": ("ERROR", "WARNING")},
    "source_document": {"status": ("CURRENT", "ARCHIVED")},
}
ORIGINS = ("HUMAN", "AI_SUGGESTED", "AI_APPROVED")


def in_list(column: str, values: tuple[str, ...]) -> CheckConstraint:
    listed = ", ".join(f"'{v}'" for v in values)
    return CheckConstraint(f"{column} IN ({listed})", name=column)


def allowed(table: str) -> tuple[CheckConstraint, ...]:
    """One CHECK per enum column of a table, from ALLOWED."""
    return tuple(in_list(col, values) for col, values in ALLOWED.get(table, {}).items())


# --- Bookkeeping -------------------------------------------------------------

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



class DqIssue(Base):
    """One data-quality problem found by a check, traceable to a staging row."""

    __tablename__ = "dq_issue"
    __table_args__ = allowed("dq_issue")
    id: Mapped[int] = mapped_column(primary_key=True)
    ingestion_run_id: Mapped[int] = mapped_column(ForeignKey("ingestion_run.id"))
    check_name: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(Text)  # ERROR: row kept out of core
    table_name: Mapped[str] = mapped_column(Text)  # staging table (= CSV file name)
    source_row: Mapped[int | None]
    external_id: Mapped[str | None] = mapped_column(Text)
    column_name: Mapped[str | None] = mapped_column(Text)
    value: Mapped[str | None] = mapped_column(Text)
    message: Mapped[str] = mapped_column(Text)

# --- Shared column sets (mixins) ---------------------------------------------

class Keyed:
    """Internal id + the source's own ID, unique within a project."""

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    external_id: Mapped[str] = mapped_column(Text)  # e.g. REQ-013; the only ID reports show


class Provenance:
    """Where a loaded row came from: file, data row, and the original row as read."""

    source_file_id: Mapped[int] = mapped_column(ForeignKey("source_file.id"))
    source_row: Mapped[int]
    source_payload: Mapped[dict[str, Any]] = mapped_column(JSONB)


class AIOrigin:
    """Who created a row: a human, or an AI (suggested, or approved by a human)."""

    origin: Mapped[str] = mapped_column(Text, server_default="HUMAN")
    created_by: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    model: Mapped[str | None] = mapped_column(Text)
    prompt_version: Mapped[str | None] = mapped_column(Text)
    approved_by: Mapped[str | None] = mapped_column(Text)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


def ai_origin_checks() -> tuple[CheckConstraint, ...]:
    """The ADR 0002 rules: AI rows name model + prompt version; approved rows an approver."""
    return (
        in_list("origin", ORIGINS),
        CheckConstraint("origin = 'HUMAN' OR (model IS NOT NULL AND prompt_version IS NOT NULL)",
                        name="ai_has_model"),
        CheckConstraint("origin <> 'AI_APPROVED' OR "
                        "(approved_by IS NOT NULL AND approved_at IS NOT NULL)",
                        name="approved_has_approver"),
    )


# --- Core: releases and requirements -----------------------------------------

class Release(Base, Keyed):
    """Built from release values seen in the files; there is no release file."""

    __tablename__ = "release"
    __table_args__ = (UniqueConstraint("project_id", "external_id"),)


class Requirement(Base, Keyed, Provenance):
    __tablename__ = "requirement"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
        *allowed("requirement"),
    )
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("requirement.id"))  # epic
    domain: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    requirement_type: Mapped[str | None] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    approval_status: Mapped[str] = mapped_column(Text)
    version: Mapped[str | None] = mapped_column(Text)
    effective_date: Mapped[date | None] = mapped_column(Date)
    owner: Mapped[str | None] = mapped_column(Text)
    source_document_id: Mapped[int | None] = mapped_column(ForeignKey("source_document.id"))
    source_section: Mapped[str | None] = mapped_column(Text)


class ReleaseScope(Base, Provenance):
    """Which requirements are in which release. Keyed by the pair, so no external_id."""

    __tablename__ = "release_scope"
    __table_args__ = (UniqueConstraint("release_id", "requirement_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    release_id: Mapped[int] = mapped_column(ForeignKey("release.id"))
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirement.id"))
    in_scope: Mapped[bool]
    release_blocking: Mapped[bool]
    criticality: Mapped[str | None] = mapped_column(Text)  # Set A only
    business_owner: Mapped[str | None] = mapped_column(Text)


# --- Core: criteria, tests and the coverage path ------------------------------

class AcceptanceCriterion(Base, Keyed, Provenance, AIOrigin):
    __tablename__ = "acceptance_criterion"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
        *allowed("acceptance_criterion"),
        *ai_origin_checks(),
    )
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirement.id"))
    criterion: Mapped[str] = mapped_column(Text)
    criterion_type: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)


class TestCase(Base, Keyed, Provenance, AIOrigin):
    __test__ = False  # not a pytest test class, despite the name
    __tablename__ = "test_case"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
        *allowed("test_case"),
        *ai_origin_checks(),
    )
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirement.id"))
    domain: Mapped[str | None] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    test_type: Mapped[str | None] = mapped_column(Text)
    preconditions: Mapped[str | None] = mapped_column(Text)
    steps: Mapped[str | None] = mapped_column(Text)
    expected_result: Mapped[str | None] = mapped_column(Text)
    automation_status: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)


class TraceLink(Base, Keyed, Provenance, AIOrigin):
    """The coverage path: requirement -> (optional AC) -> test, all real foreign keys."""

    __tablename__ = "trace_link"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
        *allowed("trace_link"),
        *ai_origin_checks(),
    )
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirement.id"))
    acceptance_criterion_id: Mapped[int | None] = mapped_column(
        ForeignKey("acceptance_criterion.id"))  # NULL for Set A / Set C (no ACs)
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_case.id"))
    link_type: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)


# --- Core: evidence --------------------------------------------------------------

class TestExecution(Base, Keyed, Provenance):
    __test__ = False  # not a pytest test class, despite the name
    __tablename__ = "test_execution"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
        *allowed("test_execution"),
    )
    test_case_id: Mapped[int] = mapped_column(ForeignKey("test_case.id"))
    release_id: Mapped[int] = mapped_column(ForeignKey("release.id"))
    environment: Mapped[str | None] = mapped_column(Text)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    outcome: Mapped[str] = mapped_column(Text)
    duration_seconds: Mapped[int | None]
    build_id: Mapped[str | None] = mapped_column(Text)
    evidence_uri: Mapped[str | None] = mapped_column(Text)


class Defect(Base, Keyed, Provenance):
    __tablename__ = "defect"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id"),
        *allowed("defect"),
    )
    test_case_id: Mapped[int | None] = mapped_column(ForeignKey("test_case.id"))
    requirement_id: Mapped[int | None] = mapped_column(ForeignKey("requirement.id"))
    release_id: Mapped[int] = mapped_column(ForeignKey("release.id"))
    severity: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    detected_in_build: Mapped[str | None] = mapped_column(Text)
    owner_team: Mapped[str | None] = mapped_column(Text)



# --- Supporting: loaded and validated, no decision rules on them yet ---------------

class SourceDocument(Base, Keyed, Provenance):
    """A document from document_registry.csv; requirements cite it."""

    __tablename__ = "source_document"
    __table_args__ = (UniqueConstraint("project_id", "external_id"), *allowed("source_document"))
    file_name: Mapped[str] = mapped_column(Text)
    document_type: Mapped[str | None] = mapped_column(Text)
    domain: Mapped[str | None] = mapped_column(Text)  # may list several, e.g. "payments,refunds"
    version: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    effective_date: Mapped[date | None] = mapped_column(Date)
    classification: Mapped[str | None] = mapped_column(Text)


class ApiEndpoint(Base, Keyed, Provenance):
    __tablename__ = "api_endpoint"
    __table_args__ = (UniqueConstraint("project_id", "external_id"),)
    path: Mapped[str] = mapped_column(Text)
    method: Mapped[str] = mapped_column(Text)
    domain: Mapped[str | None] = mapped_column(Text)
    purpose: Mapped[str | None] = mapped_column(Text)
    response_codes: Mapped[str | None] = mapped_column(Text)  # kept as text, e.g. "200,404"
    authentication: Mapped[str | None] = mapped_column(Text)
    idempotency_required: Mapped[bool | None]


if __name__ == "__main__":
    # Print the schema as Postgres DDL: `uv run python -m delivery_assurance.models`
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in Base.metadata.sorted_tables:
        print(f"{CreateTable(table).compile(dialect=postgresql.dialect())};".strip() + "\n")

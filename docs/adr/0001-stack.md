# ADR 0001: Choose the stack

- **Status:** Accepted
- **Date:** 2026-11-10
- **Decider:** Steve Greco
- **Issue:** W1-04

## Context

The project needs a language, a data store, a way for code to talk to that store, and (eventually) an API. The workloads, in order of arrival:

- **Week 2:** relational traceability and coverage queries over 11 reference CSVs (~2,000 rows), plus deterministic readiness rules.
- **Week 3:** LLM calls with structured output, token/cost logging, and an evaluation runner.
- **Week 4:** PDF parsing, chunking, embeddings, and hybrid (keyword + vector) search.
- **Week 8:** a reviewer view that drills down from a readiness decision to its evidence.

Constraints:

- 8–10 hours a week, and the project is about two weeks behind at the time of this decision.
- It's a learning project: every part must be explainable by its owner.
- The build is agentic (Claude Code writes the code), and some sessions run in cloud containers. Those have Postgres 16 installed but **no Docker daemon**.

## Options considered

### Language
| Option | For | Against |
|---|---|---|
| **Python** | Strongest ecosystem for LLM SDKs, PDF parsing, embeddings and evaluation | None significant for this project |
| TypeScript | Matches the existing Eleventy site (Node) | Thinner AI/PDF/eval libraries; more wiring later |

### Data store
| Option | For | Against |
|---|---|---|
| **Postgres** | `pgvector` + built-in full-text search allow Week 4 hybrid search in one store; foreign keys, enums and constraints always enforced; realistic production choice | Setup cost (Docker Compose, `.env` connection settings); must be running for anything to work |
| SQLite | Zero setup, built into Python, single file | Foreign keys off by default; vector search needs an add-on; not what a team would deploy |
| DuckDB | Reads CSVs directly, fast analytics | Analytics engine rather than an app store; one more dependency |

### Database access
| Option | For | Against |
|---|---|---|
| **SQLAlchemy 2.0** | Standard in FastAPI apps; models define tables and relationships in Python; supports both ORM and SQL-expression styles; easy to swap databases in tests | Abstraction can hide the SQL actually run, which matters when queries must be explained |
| psycopg + raw SQL | Every query is plain, visible SQL | More boilerplate; tables and mapping written by hand; less common in FastAPI apps |
| **SQLAlchemy + hand-written SQL for decisions** | Realistic app plumbing *and* readable decision logic; a common split (ORM for CRUD, plain SQL for reporting) | Two styles in one codebase; the boundary between them must be kept clear |

### API layer
| Option | For | Against |
|---|---|---|
| **FastAPI** | Typed request/response models, automatic API docs, async support, the common 2026 choice for Python APIs | Not needed until a feature has to be served over HTTP |
| CLI only | Simplest | No path to the Week 8 reviewer view |

## Decision

- **Python 3.13**, with dependencies and the virtual environment managed by **uv**.
- **Postgres 16**, run with **Docker Compose** on the laptop. Cloud sessions use the natively installed Postgres 16 instead, since they have no Docker daemon. Both read the same connection settings from `.env`.
- **SQLAlchemy 2.0** for database access, split by purpose:
  - **App plumbing** (connections, transactions, table definitions, the loader's inserts) uses SQLAlchemy.
  - **Decision logic** (traceability chains, coverage gaps, readiness rules) is hand-written SQL, kept in its own files or functions and run through SQLAlchemy's `text()`. These are the answers the architect must defend, so each one must be readable line by line.
- **FastAPI** as the API layer. It's added when an issue first needs HTTP (expected: W8-01). Until then, Week 2 logic runs as Python functions and a command-line entry point.

## Consequences

**Positive**
- Week 4 retrieval can stay inside Postgres (`pgvector` + full-text search) instead of adding a separate vector database.
- The database enforces referential integrity, which supports W2-02's data-quality checks.
- The stack matches what a real team would build, so the defense can be framed around production trade-offs.

**Negative / risks**
- More setup than SQLite while already behind. W2-02 absorbs roughly an extra hour for Compose and connection settings.
- Laptop (Docker) and cloud (native) setups can drift. Mitigation: pin Postgres 16 in both and keep all settings in `.env`.
- Two query styles in one codebase. Mitigation: the rule above. If a query decides coverage or readiness, it's hand-written SQL. Engine logging can show the SQL behind everything else.

**Postponed decisions** (safe to defer because nothing in Week 2 depends on them)
- Tables as ORM model classes vs plain SQLAlchemy `Table` definitions. Decide in W2-01.
- Schema migrations (e.g. Alembic) vs recreating the schema on each load. Decide in W2-02, where the idempotent loader is designed.
- Installing `pgvector`. Decide in W4-03.
- Which LLM provider and SDK. Decide in W3-01.

**Dependency rule:** each library (SQLAlchemy, the Postgres driver, FastAPI, …) is added by the issue that first needs it, after its purpose is explained and approved, not up front.

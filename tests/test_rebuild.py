"""W2-02 'done when', as tests. They rebuild the database in DATABASE_URL.

Run: `uv run pytest`
"""

import pytest
from sqlalchemy import text

from delivery_assurance import models
from delivery_assurance.checks import KEYS, REQUIRED, STAGING_OF
from delivery_assurance.db import get_engine
from delivery_assurance.promote import STEPS
from delivery_assurance.rebuild import rebuild

# Row counts recorded in docs/notes/data-profile.md.
PROFILE_COUNTS = {
    "acceptance_criteria": 421, "api_endpoints": 11, "defects": 114,
    "document_registry": 8, "release_scope": 135, "requirement_changes": 45,
    "requirements": 135, "test_cases": 183, "test_executions": 569,
    "traceability_links": 183, "user_stories": 110,
}
CORE_TABLES = ["release"] + [core for core, _, _ in STEPS]


def do_rebuild() -> None:
    with get_engine().begin() as conn:
        rebuild(conn)


def snapshot() -> dict:
    """A fingerprint of every core row (all columns) plus every dq_issue."""
    with get_engine().connect() as conn:
        tables = {t: conn.execute(text(
            f"SELECT count(*), md5(coalesce(string_agg(to_jsonb(x)::text, '|' ORDER BY id), ''))"
            f" FROM {t} x")).one() for t in CORE_TABLES}
        issues = conn.execute(text("""SELECT check_name, severity, table_name, source_row,
            external_id, column_name, value FROM dq_issue ORDER BY 1, 3, 4, 6""")).all()
    return {"tables": tables, "issues": issues}


@pytest.fixture(scope="module")
def conn():
    do_rebuild()
    with get_engine().connect() as c:
        yield c


def test_rebuild_twice_gives_identical_database():
    do_rebuild()
    first = snapshot()
    do_rebuild()
    assert snapshot() == first


def test_staging_counts_match_profile(conn):
    for table, expected in PROFILE_COUNTS.items():
        assert conn.execute(text(f'SELECT count(*) FROM staging."{table}"')).scalar() == expected, table


def test_every_staging_row_is_in_core_or_rejected(conn):
    for core, staging, _ in STEPS:
        n_staging, n_core, n_rejected = conn.execute(text(f"""
            SELECT (SELECT count(*) FROM staging."{staging}"), (SELECT count(*) FROM {core}),
                   (SELECT count(DISTINCT source_row) FROM dq_issue
                    WHERE table_name = '{staging}' AND severity = 'ERROR')""")).one()
        assert n_staging == n_core + n_rejected, core


def test_required_matches_not_null_columns():
    """REQUIRED (checks.py) and NOT NULL (models.py) must describe the same columns,
    or a blank value slips past the checks and fails the whole rebuild at promote."""
    bookkeeping = {"id", "project_id", "source_file_id", "source_row", "source_payload", "origin"}
    staging_to_core = {v: k for k, v in STAGING_OF.items()} | {"release_scope": "release_scope"}
    for staging, required in REQUIRED.items():
        table = models.Base.metadata.tables[staging_to_core[staging]]
        rename = {"external_id": KEYS[staging][1], "release_id": "release",
                  "target_release_id": "target_release"}
        not_null = {rename.get(c.name, c.name) for c in table.columns
                    if not c.nullable and c.name not in bookkeeping}
        assert set(required) == not_null, staging

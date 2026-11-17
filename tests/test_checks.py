"""Every check is proven on known-bad input (W2-02).

The reference data is clean, so a broken check and a working check would both
report "no issues". These tests plant one bad row per check in staging and
assert the check fires. Each test runs in a transaction that is rolled back,
so the database is left as it was.

Run: `uv run pytest`
"""

import pytest
from sqlalchemy import text

from delivery_assurance.checks import run_checks
from delivery_assurance.db import get_engine
from delivery_assurance.promote import promote
from delivery_assurance.staging import load_staging

COPY_REQ_003 = """INSERT INTO staging.requirements
    SELECT source_file_id, 999, requirement_id, epic_id, domain, title, description,
           requirement_type, priority, source_document_id, source_section, status,
           release, owner, version, effective_date, approval_status
    FROM staging.requirements WHERE requirement_id = 'REQ-003'"""

# (plant SQL, expected issue: check_name, severity, staging table, source_row, column)
CASES = {
    "duplicate_id": (COPY_REQ_003,
        ("duplicate_id", "ERROR", "requirements", 999, "requirement_id")),
    "missing_required": ("UPDATE staging.requirements SET title = '  ' WHERE source_row = 5",
        ("missing_required", "ERROR", "requirements", 5, "title")),
    "invalid_enum": ("UPDATE staging.requirements SET priority = 'p0' WHERE source_row = 1",
        ("invalid_enum", "ERROR", "requirements", 1, "priority")),
    "unconvertible": (
        "UPDATE staging.requirements SET effective_date = '2026-02-30' WHERE source_row = 4",
        ("unconvertible", "ERROR", "requirements", 4, "effective_date")),
    "dangling_reference_error": (
        "UPDATE staging.traceability_links SET test_case_id = 'TC-9999' WHERE source_row = 1",
        ("dangling_reference", "ERROR", "traceability_links", 1, "test_case_id")),
    "dangling_reference_warning": (
        "UPDATE staging.defects SET requirement_id = 'REQ-999' WHERE source_row = 3",
        ("dangling_reference", "WARNING", "defects", 3, "requirement_id")),
    "requirement_mismatch": (
        "UPDATE staging.traceability_links SET requirement_id = 'REQ-099' WHERE source_row = 1",
        ("requirement_mismatch", "WARNING", "traceability_links", 1, "requirement_id")),
}


@pytest.fixture
def conn():
    """Fresh staging inside a transaction that is always rolled back."""
    with get_engine().connect() as c:
        tx = c.begin()
        load_staging(c)
        yield c
        tx.rollback()


def issues(conn) -> set[tuple]:
    return set(conn.execute(text("""
        SELECT check_name, severity, table_name, source_row, column_name FROM dq_issue""")).all())


def test_clean_data_has_no_issues(conn):
    run_checks(conn)
    assert issues(conn) == set()


@pytest.mark.parametrize("plant, expected", CASES.values(), ids=CASES.keys())
def test_check_fires_on_planted_row(conn, plant, expected):
    conn.execute(text(plant))
    run_checks(conn)
    assert expected in issues(conn)


def test_rejected_test_case_cascades(conn):
    """TC-0001 rejected: its runs and link stay out, its defects load with a warning."""
    conn.execute(text("UPDATE staging.test_cases SET status = 'RETIRED' "
                      "WHERE test_case_id = 'TC-0001'"))
    run_checks(conn)
    promote(conn)

    def count(sql: str) -> int:
        return conn.execute(text(sql)).scalar_one()

    runs = count("SELECT count(*) FROM staging.test_executions WHERE test_case_id = 'TC-0001'")
    defects = count("SELECT count(*) FROM staging.defects WHERE test_case_id = 'TC-0001'")
    assert runs > 0 and defects > 0  # the plant must actually have dependents

    assert count("SELECT count(*) FROM test_case WHERE external_id = 'TC-0001'") == 0
    assert count("""SELECT count(*) FROM dq_issue WHERE check_name = 'parent_rejected'
                    AND table_name = 'test_executions'""") == runs
    assert count("""SELECT count(*) FROM defect WHERE test_case_id IS NULL
                    AND source_payload->>'test_case_id' = 'TC-0001'""") == defects
    assert count("""SELECT count(*) FROM dq_issue WHERE check_name = 'reference_emptied'
                    AND table_name = 'defects' AND column_name = 'test_case_id'""") == defects

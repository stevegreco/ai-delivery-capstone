"""Data-quality checks on the staging tables (W2-02).

Each check is one SQL query that returns the rows breaking a rule, with these
columns: table_name, source_row, external_id, column_name, value, message.
No rows returned = check passed. The runner stores results in dq_issue.
Run after the staging load: `uv run python -m delivery_assurance.checks`
"""

from dataclasses import dataclass

from sqlalchemy import Connection, text

from delivery_assurance.db import get_engine
from delivery_assurance.models import ALLOWED

# The ID of each staging table: (label shown in reports, SQL expression).
# release_scope has no ID column, so its key is the pair, e.g. R26.10/REQ-001.
KEYS = {
    "acceptance_criteria": ("acceptance_criterion_id", "acceptance_criterion_id"),
    "api_endpoints": ("endpoint_id", "endpoint_id"),
    "defects": ("defect_id", "defect_id"),
    "document_registry": ("document_id", "document_id"),
    "release_scope": ("release+requirement_id", "release || '/' || requirement_id"),
    "requirement_changes": ("change_id", "change_id"),
    "requirements": ("requirement_id", "requirement_id"),
    "test_cases": ("test_case_id", "test_case_id"),
    "test_executions": ("execution_id", "execution_id"),
    "traceability_links": ("link_id", "link_id"),
    "user_stories": ("story_id", "story_id"),
}


# Columns that are NOT NULL in core (models.py), by staging table and staging
# column name. Keep in step with models.py; supporting tables arrive in piece 8.
REQUIRED = {
    "requirements": ["requirement_id", "title", "priority", "status", "approval_status"],
    "acceptance_criteria": ["acceptance_criterion_id", "requirement_id", "criterion", "status"],
    "test_cases": ["test_case_id", "requirement_id", "title", "status"],
    "traceability_links": ["link_id", "requirement_id", "test_case_id", "link_type", "status"],
    "test_executions": ["execution_id", "test_case_id", "release", "executed_at", "outcome"],
    "defects": ["defect_id", "release", "severity", "status", "summary"],
    "release_scope": ["release", "requirement_id", "in_scope", "release_blocking"],
}

# Core table -> staging table, for tables whose enum columns keep their names.
STAGING_OF = {
    "requirement": "requirements", "acceptance_criterion": "acceptance_criteria",
    "test_case": "test_cases", "trace_link": "traceability_links",
    "test_execution": "test_executions", "defect": "defects",
}
YES_NO = {"release_scope": ["in_scope", "release_blocking"]}  # become booleans in core

# Columns that must convert to a Postgres type. executed_at has no time zone in
# the source; the loader treats it as UTC (see docs/notes/data-profile.md).
CONVERTIBLE = {
    ("requirements", "effective_date"): "date",
    ("test_executions", "executed_at"): "timestamp",
    ("test_executions", "duration_seconds"): "integer",
}

@dataclass
class Check:
    name: str
    severity: str  # ERROR or WARNING
    sql: str


def duplicate_id_checks() -> list[Check]:
    """Every row whose ID appears more than once. All copies are flagged,
    because nothing tells us which copy is the right one."""
    return [Check("duplicate_id", "ERROR", f"""
        SELECT '{table}' AS table_name, source_row, key AS external_id,
               '{label}' AS column_name, key AS value,
               'ID appears ' || n || ' times' AS message
        FROM (SELECT source_row, {key} AS key,
                     count(*) OVER (PARTITION BY {key}) AS n
              FROM staging."{table}") s
        WHERE n > 1""") for table, (label, key) in KEYS.items()]


def missing_required_checks() -> list[Check]:
    """Rows where a required column is NULL or blank ('' is how CSV shows empty)."""
    return [Check("missing_required", "ERROR", f"""
        SELECT '{table}' AS table_name, source_row, {KEYS[table][1]} AS external_id,
               '{column}' AS column_name, "{column}" AS value,
               'required field is blank' AS message
        FROM staging."{table}"
        WHERE coalesce(trim("{column}"), '') = ''""")
        for table, columns in REQUIRED.items() for column in columns]


def bad_value_query(table: str, column: str, condition: str, message: str) -> str:
    """Shared shape: non-blank values in table.column for which condition is true."""
    return f"""
        SELECT '{table}' AS table_name, source_row, {KEYS[table][1]} AS external_id,
               '{column}' AS column_name, "{column}" AS value, {message} AS message
        FROM staging."{table}"
        WHERE coalesce(trim("{column}"), '') <> '' AND {condition}"""


def invalid_enum_checks() -> list[Check]:
    """Values outside the agreed list. Near misses (p0, 'APPROVED ') count too:
    mapping source values is the adapter's job, not something core guesses."""
    lists = [(STAGING_OF[t], col, vals) for t, cols in ALLOWED.items() if t in STAGING_OF
             for col, vals in cols.items()]
    lists += [(t, col, ("YES", "NO")) for t, cols in YES_NO.items() for col in cols]
    checks = []
    for table, column, values in lists:
        listed = ", ".join(f"'{v}'" for v in values)
        checks.append(Check("invalid_enum", "ERROR", bad_value_query(
            table, column, f'"{column}" NOT IN ({listed})',
            f"'not one of: {', '.join(values)}'")))
    return checks


def unconvertible_checks() -> list[Check]:
    """Values Postgres cannot read as the core type, e.g. 2026-02-30 as a date."""
    return [Check("unconvertible", "ERROR", bad_value_query(
        table, column, f"""NOT pg_input_is_valid("{column}", '{pg_type}')""",
        f"'not a valid {pg_type}'"))
        for (table, column), pg_type in CONVERTIBLE.items()]


def all_checks() -> list[Check]:
    return (duplicate_id_checks() + missing_required_checks()
            + invalid_enum_checks() + unconvertible_checks())


def run_checks(conn: Connection) -> None:
    """Run every check for the latest ingestion run and store its findings."""
    run_id = conn.execute(text("SELECT max(id) FROM ingestion_run")).scalar_one()
    conn.execute(text("DELETE FROM dq_issue WHERE ingestion_run_id = :r"), {"r": run_id})
    for check in all_checks():
        conn.execute(text(f"""
            INSERT INTO dq_issue (ingestion_run_id, check_name, severity, table_name,
                                  source_row, external_id, column_name, value, message)
            SELECT :run_id, :name, :severity, q.* FROM ({check.sql}) q"""),
            {"run_id": run_id, "name": check.name, "severity": check.severity})


def print_summary(conn: Connection) -> None:
    rows = conn.execute(text("""
        SELECT check_name, severity, table_name, count(*) FROM dq_issue
        GROUP BY 1, 2, 3 ORDER BY 2, 1, 3""")).all()
    print(f"{len(all_checks())} check queries run; " + (f"{sum(r[3] for r in rows)} issue(s):" if rows else "no issues."))
    for name, severity, table, n in rows:
        print(f"  {severity:<8}{name:<22}{table:<22}{n:>5}")


if __name__ == "__main__":
    with get_engine().begin() as conn:
        run_checks(conn)
        print_summary(conn)

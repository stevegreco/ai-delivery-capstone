"""Data-quality checks on the staging tables (W2-02).

Each check is one SQL query that returns the rows breaking a rule, with these
columns: table_name, source_row, external_id, column_name, value, message.
No rows returned = check passed. The runner stores results in dq_issue.
Run after the staging load: `uv run python -m delivery_assurance.checks`
"""

from dataclasses import dataclass

from sqlalchemy import Connection, text

from delivery_assurance.db import get_engine

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


def all_checks() -> list[Check]:
    return duplicate_id_checks()


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
    print(f"{len(all_checks())} checks run; " + (f"{sum(r[3] for r in rows)} issue(s):" if rows else "no issues."))
    for name, severity, table, n in rows:
        print(f"  {severity:<8}{name:<22}{table:<22}{n:>5}")


if __name__ == "__main__":
    with get_engine().begin() as conn:
        run_checks(conn)
        print_summary(conn)

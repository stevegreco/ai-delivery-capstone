"""One command to rebuild the database from the reference CSVs: `uv run rebuild-db`.

Staging load, checks and promotion run in ONE transaction: if anything fails,
the database is left exactly as it was. Running it twice gives the same result.
"""

from sqlalchemy import Connection, text

from delivery_assurance.checks import run_checks
from delivery_assurance.db import get_engine
from delivery_assurance.promote import print_counts, promote
from delivery_assurance.staging import load_staging

EXAMPLES = 5  # issue rows shown per check in the report


def rebuild(conn: Connection) -> None:
    load_staging(conn)
    run_checks(conn)
    promote(conn)
    # clock_timestamp(), not now(): now() is frozen at the start of the transaction.
    conn.execute(text("UPDATE ingestion_run SET finished_at = clock_timestamp()"))


def print_report(conn: Connection) -> None:
    """Data-quality report: issues grouped by severity, check and table, with examples."""
    groups = conn.execute(text("""
        SELECT severity, check_name, table_name, count(*) FROM dq_issue
        GROUP BY 1, 2, 3 ORDER BY severity, check_name, table_name""")).all()
    print("\nData-quality report")
    if not groups:
        print("  No issues: every check passed and every row reached core.")
    for severity, check, table, n in groups:
        print(f"\n  {severity} {check} in {table}: {n} row(s)")
        for row in conn.execute(text("""
                SELECT source_row, external_id, column_name, value, message FROM dq_issue
                WHERE severity = :s AND check_name = :c AND table_name = :t
                ORDER BY source_row LIMIT :n"""),
                {"s": severity, "c": check, "t": table, "n": EXAMPLES}):
            source_row, external_id, column, value, message = row
            where = f"row {source_row} {external_id or ''}".strip()
            what = f"{column}={value!r}: " if column else ""
            print(f"    - {where}: {what}{message}")
        if n > EXAMPLES:
            print(f"    … and {n - EXAMPLES} more")


def main() -> None:
    with get_engine().begin() as conn:
        rebuild(conn)
        print_counts(conn)
        print_report(conn)

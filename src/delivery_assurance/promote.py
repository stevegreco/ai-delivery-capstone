"""Promote clean rows from staging into the core tables (W2-02).

Tables are copied parents-first, each with one INSERT ... SELECT. A row is
copied only if it has no ERROR in dq_issue and its parents reached core
(the JOINs to core tables enforce that). Every staging row ends up either
in core or in dq_issue: rows that were clean but still missed core are
recorded as parent_rejected.
"""

from sqlalchemy import Connection, text

from delivery_assurance.checks import KEYS
from delivery_assurance.db import get_engine

# The original row, minus the two bookkeeping columns, kept as JSON.
PAYLOAD = "to_jsonb(s) - 'source_file_id' - 'source_row'"


def clean(staging_table: str) -> str:
    """SQL condition: staging row s has no ERROR for this run."""
    return f"""NOT EXISTS (SELECT 1 FROM dq_issue d
        WHERE d.ingestion_run_id = :run_id AND d.severity = 'ERROR'
          AND d.table_name = '{staging_table}' AND d.source_row = s.source_row)"""


RELEASES = """
    INSERT INTO release (project_id, external_id)
    SELECT DISTINCT :project_id, v.release FROM (
        SELECT release FROM staging.requirements
        UNION SELECT release FROM staging.release_scope
        UNION SELECT release FROM staging.test_executions
        UNION SELECT release FROM staging.defects) v
    WHERE coalesce(trim(v.release), '') <> ''"""

# (core table, staging table, INSERT ... SELECT), in dependency order.
STEPS = [
    ("requirement", "requirements", f"""
    INSERT INTO requirement (project_id, external_id, source_file_id, source_row,
        source_payload, domain, title, description, requirement_type, priority, status,
        approval_status, version, effective_date, owner, source_section)
    SELECT :project_id, s.requirement_id, s.source_file_id, s.source_row, {PAYLOAD},
        nullif(s.domain, ''), s.title, nullif(s.description, ''),
        nullif(s.requirement_type, ''), s.priority, s.status, s.approval_status,
        nullif(s.version, ''), nullif(s.effective_date, '')::date,
        nullif(s.owner, ''), nullif(s.source_section, '')
    FROM staging.requirements s
    WHERE {clean("requirements")}
    ORDER BY s.source_row"""),

    ("release_scope", "release_scope", f"""
    INSERT INTO release_scope (release_id, requirement_id, source_file_id, source_row,
        source_payload, in_scope, release_blocking, business_owner)
    SELECT rl.id, r.id, s.source_file_id, s.source_row, {PAYLOAD},
        s.in_scope = 'YES', s.release_blocking = 'YES', nullif(s.business_owner, '')
    FROM staging.release_scope s
    JOIN release rl ON rl.project_id = :project_id AND rl.external_id = s.release
    JOIN requirement r ON r.project_id = :project_id AND r.external_id = s.requirement_id
    WHERE {clean("release_scope")}
    ORDER BY s.source_row"""),
]


def record_parent_rejected(conn: Connection, core: str, staging: str, params: dict) -> None:
    """Clean staging rows that did not reach core: a parent they need was kept out."""
    conn.execute(text(f"""
        INSERT INTO dq_issue (ingestion_run_id, check_name, severity, table_name,
                              source_row, external_id, message)
        SELECT :run_id, 'parent_rejected', 'ERROR', '{staging}', s.source_row,
               {KEYS[staging][1]},
               'a row this one refers to was kept out of core'
        FROM staging."{staging}" s
        WHERE {clean(staging)}
          AND NOT EXISTS (SELECT 1 FROM {core} c WHERE c.source_file_id = s.source_file_id
                                                   AND c.source_row = s.source_row)"""),
        params)


def promote(conn: Connection) -> None:
    run_id, project_id = conn.execute(text(
        "SELECT id, project_id FROM ingestion_run ORDER BY id DESC LIMIT 1")).one()
    params = {"run_id": run_id, "project_id": project_id}
    conn.execute(text(RELEASES), params)
    for core, staging, sql in STEPS:
        conn.execute(text(sql), params)
        record_parent_rejected(conn, core, staging, params)


def print_counts(conn: Connection) -> None:
    print(f"{'core table':<22}{'staging':>8}{'core':>6}{'kept out':>10}")
    for core, staging, _ in STEPS:
        n_stg, n_core, n_out = conn.execute(text(f"""
            SELECT (SELECT count(*) FROM staging."{staging}"), (SELECT count(*) FROM {core}),
                   (SELECT count(DISTINCT source_row) FROM dq_issue
                    WHERE table_name = '{staging}' AND severity = 'ERROR')""")).one()
        print(f"{core:<22}{n_stg:>8}{n_core:>6}{n_out:>10}")


if __name__ == "__main__":
    # Until piece 7's rebuild command: staging -> checks -> promote, in order.
    from delivery_assurance.checks import run_checks  # noqa: E402
    from delivery_assurance.staging import load_staging

    load_staging()
    with get_engine().begin() as conn:
        run_checks(conn)
        promote(conn)
        print_counts(conn)

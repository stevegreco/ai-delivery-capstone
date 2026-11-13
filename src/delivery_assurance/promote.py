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

    ("acceptance_criterion", "acceptance_criteria", f"""
    INSERT INTO acceptance_criterion (project_id, external_id, source_file_id, source_row,
        source_payload, requirement_id, criterion, criterion_type, status)
    SELECT :project_id, s.acceptance_criterion_id, s.source_file_id, s.source_row, {PAYLOAD},
        r.id, s.criterion, nullif(s.criterion_type, ''), s.status
    FROM staging.acceptance_criteria s
    JOIN requirement r ON r.project_id = :project_id AND r.external_id = s.requirement_id
    WHERE {clean("acceptance_criteria")}
    ORDER BY s.source_row"""),

    ("test_case", "test_cases", f"""
    INSERT INTO test_case (project_id, external_id, source_file_id, source_row,
        source_payload, requirement_id, domain, title, test_type, preconditions, steps,
        expected_result, automation_status, status)
    SELECT :project_id, s.test_case_id, s.source_file_id, s.source_row, {PAYLOAD},
        r.id, nullif(s.domain, ''), s.title, nullif(s.test_type, ''),
        nullif(s.preconditions, ''), nullif(s.steps, ''), nullif(s.expected_result, ''),
        nullif(s.automation_status, ''), s.status
    FROM staging.test_cases s
    JOIN requirement r ON r.project_id = :project_id AND r.external_id = s.requirement_id
    WHERE {clean("test_cases")}
    ORDER BY s.source_row"""),

    # The AC is optional: blank means "no AC". A named AC that was kept out
    # keeps the link out too, rather than loading it without its AC.
    ("trace_link", "traceability_links", f"""
    INSERT INTO trace_link (project_id, external_id, source_file_id, source_row,
        source_payload, requirement_id, acceptance_criterion_id, test_case_id,
        link_type, status)
    SELECT :project_id, s.link_id, s.source_file_id, s.source_row, {PAYLOAD},
        r.id, a.id, t.id, s.link_type, s.status
    FROM staging.traceability_links s
    JOIN requirement r ON r.project_id = :project_id AND r.external_id = s.requirement_id
    JOIN test_case t ON t.project_id = :project_id AND t.external_id = s.test_case_id
    LEFT JOIN acceptance_criterion a ON a.project_id = :project_id
                                    AND a.external_id = s.acceptance_criterion_id
    WHERE {clean("traceability_links")}
      AND (coalesce(s.acceptance_criterion_id, '') = '' OR a.id IS NOT NULL)
    ORDER BY s.source_row"""),

    ("test_execution", "test_executions", f"""
    INSERT INTO test_execution (project_id, external_id, source_file_id, source_row,
        source_payload, test_case_id, release_id, environment, executed_at, outcome,
        duration_seconds, build_id, evidence_uri)
    SELECT :project_id, s.execution_id, s.source_file_id, s.source_row, {PAYLOAD},
        t.id, rl.id, nullif(s.environment, ''),
        s.executed_at::timestamp AT TIME ZONE 'UTC',  -- source has no zone: read as UTC
        s.outcome, nullif(s.duration_seconds, '')::int, nullif(s.build_id, ''),
        nullif(s.evidence_uri, '')
    FROM staging.test_executions s
    JOIN test_case t ON t.project_id = :project_id AND t.external_id = s.test_case_id
    JOIN release rl ON rl.project_id = :project_id AND rl.external_id = s.release
    WHERE {clean("test_executions")}
    ORDER BY s.source_row"""),

    # Test and requirement are optional (LEFT JOIN): a defect is never dropped
    # for a bad pointer, because that would make readiness look better.
    ("defect", "defects", f"""
    INSERT INTO defect (project_id, external_id, source_file_id, source_row,
        source_payload, test_case_id, requirement_id, release_id, severity, status,
        summary, detected_in_build, owner_team)
    SELECT :project_id, s.defect_id, s.source_file_id, s.source_row, {PAYLOAD},
        t.id, r.id, rl.id, s.severity, s.status, s.summary,
        nullif(s.detected_in_build, ''), nullif(s.owner_team, '')
    FROM staging.defects s
    JOIN release rl ON rl.project_id = :project_id AND rl.external_id = s.release
    LEFT JOIN test_case t ON t.project_id = :project_id AND t.external_id = s.test_case_id
    LEFT JOIN requirement r ON r.project_id = :project_id AND r.external_id = s.requirement_id
    WHERE {clean("defects")}
    ORDER BY s.source_row"""),
]

# Defect references that were named in the file but emptied in core because the
# target was kept out (a dangling target already has its own WARNING).
DEFECT_REFS_EMPTIED = """
    INSERT INTO dq_issue (ingestion_run_id, check_name, severity, table_name,
                          source_row, external_id, column_name, value, message)
    SELECT :run_id, 'reference_emptied', 'WARNING', 'defects', d.source_row,
           d.external_id, ref.col, ref.val, 'target was kept out of core; loaded empty'
    FROM defect d
    CROSS JOIN LATERAL (VALUES
        ('test_case_id', d.source_payload->>'test_case_id', d.test_case_id),
        ('requirement_id', d.source_payload->>'requirement_id', d.requirement_id)
    ) AS ref(col, val, core_id)
    WHERE coalesce(ref.val, '') <> '' AND ref.core_id IS NULL
      AND NOT EXISTS (SELECT 1 FROM dq_issue x
                      WHERE x.ingestion_run_id = :run_id AND x.table_name = 'defects'
                        AND x.source_row = d.source_row AND x.column_name = ref.col)"""


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
    conn.execute(text(DEFECT_REFS_EMPTIED), params)


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
    from delivery_assurance.checks import run_checks
    from delivery_assurance.staging import load_staging

    load_staging()
    with get_engine().begin() as conn:
        run_checks(conn)
        promote(conn)
        print_counts(conn)

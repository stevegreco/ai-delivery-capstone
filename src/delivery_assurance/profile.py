"""Profile the staging tables and print Markdown for docs/notes/data-profile.md.

Describes the data only; deciding what is a problem is the checks' job.
Run after the staging load: `uv run python -m delivery_assurance.profile`
"""

from sqlalchemy import Connection, text

from delivery_assurance.db import get_engine

MAX_DISTINCT = 15  # columns with this many distinct values or fewer get a value list
BOOKKEEPING = ("source_file_id", "source_row")
# Key used for the uniqueness check; default is the CSV's first column.
KEYS = {"release_scope": ["release", "requirement_id"]}


def staging_columns(conn: Connection) -> dict[str, list[str]]:
    """{table: [data columns in CSV order]}, read from Postgres' own catalog."""
    rows = conn.execute(text("""
        SELECT table_name, column_name FROM information_schema.columns
        WHERE table_schema = 'staging' ORDER BY table_name, ordinal_position"""))
    tables: dict[str, list[str]] = {}
    for table, column in rows:
        if column not in BOOKKEEPING:
            tables.setdefault(table, []).append(column)
    return tables


def profile_table(conn: Connection, table: str, columns: list[str]) -> None:
    q = lambda sql: conn.execute(text(sql))  # identifiers come from the catalog above
    total = q(f'SELECT count(*) FROM staging."{table}"').scalar_one()
    key = KEYS.get(table, columns[:1])
    key_sql = ", ".join(f'"{c}"' for c in key)
    distinct_keys = q(f'SELECT count(DISTINCT ({key_sql})) FROM staging."{table}"').scalar_one()
    dupes = total - distinct_keys
    print(f"\n### {table} ({total} rows)\n")
    print(f"Key `{', '.join(key)}`: " + ("unique" if dupes == 0 else f"**{dupes} duplicate(s)**") + "\n")
    print("| Column | Blank | Distinct | Values (count) |\n|---|---:|---:|---|")
    for col in columns:
        blank, distinct = q(f"""SELECT count(*) FILTER (WHERE coalesce("{col}", '') = ''),
                                       count(DISTINCT nullif("{col}", ''))
                                FROM staging."{table}" """).one()
        values = ""
        if distinct <= MAX_DISTINCT:
            values = ", ".join(f"`{v}` ({n})" for v, n in q(f"""
                SELECT "{col}", count(*) FROM staging."{table}"
                WHERE coalesce("{col}", '') <> '' GROUP BY 1 ORDER BY 2 DESC, 1"""))
        print(f"| `{col}` | {blank or ''} | {distinct} | {values} |")


if __name__ == "__main__":
    with get_engine().connect() as conn:
        for table, columns in staging_columns(conn).items():
            profile_table(conn, table, columns)

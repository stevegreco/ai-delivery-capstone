"""Run the hand-written decision SQL in src/delivery_assurance/sql/ (ADR 0001).

Each question is one .sql file, readable on its own and runnable in psql
(replace :name parameters by hand). This module only loads and runs them.
"""

from pathlib import Path

from sqlalchemy import Connection, RowMapping, text

SQL_DIR = Path(__file__).parent / "sql"


def load_sql(name: str) -> str:
    """name is a path under sql/ without .sql, e.g. 'chain/links'."""
    return (SQL_DIR / f"{name}.sql").read_text()


def run(conn: Connection, name: str, **params) -> list[RowMapping]:
    return list(conn.execute(text(load_sql(name)), params).mappings())

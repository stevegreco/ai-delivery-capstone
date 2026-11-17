"""Database connection: one place that turns DATABASE_URL into a SQLAlchemy engine."""

import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text


def get_engine(echo: bool = False) -> Engine:
    """Build an engine from DATABASE_URL (read from .env if present).

    echo=True logs every SQL statement SQLAlchemy sends, which is how you
    see the SQL behind ORM calls (ADR 0001).
    """
    load_dotenv()
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set. Copy .env.example to .env.")
    return create_engine(url, echo=echo)


if __name__ == "__main__":
    # Connection check: `uv run python -m delivery_assurance.db`
    with get_engine().connect() as conn:
        print(conn.execute(text("SELECT version()")).scalar_one())

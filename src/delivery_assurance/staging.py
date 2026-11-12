"""Staging load: copy each reference CSV, unchanged, into staging.<file name>.

Every column is text, so nothing is rejected here. Validation runs on the
staging tables later (W2-02 option A). Each row keeps source_file_id and
source_row so any value can be traced back to its file and line.
"""

import csv
import hashlib
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import Column, Integer, MetaData, Table, Text, text
from sqlalchemy.orm import Session

from delivery_assurance.db import get_engine
from delivery_assurance.models import Base, IngestionRun, Project, SourceFile

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "Capstone4_AI_Delivery_Assurance_Test_Engineering_Dataset" / "data"
LOADER_VERSION = "0.1.0"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def stage_file(session: Session, path: Path, source_file_id: int, rows, header) -> None:
    """Create staging.<name> with one text column per CSV header, then insert."""
    table = Table(
        path.stem, MetaData(schema="staging"),
        Column("source_file_id", Integer, nullable=False),
        Column("source_row", Integer, nullable=False),  # 1 = first data row
        *[Column(name, Text) for name in header],
    )
    table.create(session.connection())
    session.execute(table.insert(), [
        {"source_file_id": source_file_id, "source_row": i, **row}
        for i, row in enumerate(rows, start=1)
    ])


def load_staging() -> None:
    """Rebuild bookkeeping + staging from scratch, in one transaction."""
    with Session(get_engine()) as session, session.begin():
        conn = session.connection()
        conn.execute(text("DROP SCHEMA IF EXISTS staging CASCADE"))
        conn.execute(text("CREATE SCHEMA staging"))
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)

        project = Project(key="REFERENCE", name="Reference CSVs")
        session.add(project)
        session.flush()  # assigns project.id
        run = IngestionRun(project_id=project.id, adapter="reference_csv",
                           loader_version=LOADER_VERSION, started_at=datetime.now(UTC))
        session.add(run)
        session.flush()

        for path in sorted(DATA_DIR.glob("*.csv")):
            header, rows = read_csv(path)
            source_file = SourceFile(ingestion_run_id=run.id,
                                     path=str(path.relative_to(REPO_ROOT)),
                                     sha256=sha256_of(path), row_count=len(rows))
            session.add(source_file)
            session.flush()
            stage_file(session, path, source_file.id, rows, header)

        run.finished_at = datetime.now(UTC)


def print_counts() -> None:
    """Count rows in the database (not in memory) and compare with source_file."""
    with get_engine().connect() as conn:
        for name, expected in conn.execute(text(
            "SELECT path, row_count FROM source_file ORDER BY path")):
            table = Path(name).stem
            actual = conn.execute(text(f'SELECT count(*) FROM staging."{table}"')).scalar_one()
            flag = "" if actual == expected else "  <-- MISMATCH"
            print(f"{table:<22}{actual:>5}{flag}")


if __name__ == "__main__":
    load_staging()
    print_counts()

"""Traceability: the full chain under a requirement (W2-03).

`uv run python -m delivery_assurance.traceability REQ-001`
"""

import sys

from sqlalchemy import Connection

from delivery_assurance.db import get_engine
from delivery_assurance.queries import run

PROJECT = "REFERENCE"


def requirement_chain(conn: Connection, requirement: str, project: str = PROJECT) -> dict | None:
    """Requirement -> scope, ACs, links -> tests -> runs, and defects. All by external ID."""
    p = {"project": project, "requirement": requirement}
    found = run(conn, "chain/requirement", **p)
    if not found:
        return None
    runs = run(conn, "chain/executions", **p)
    links = [dict(link, executions=[e for e in runs if e["test_case"] == link["test_case"]])
             for link in run(conn, "chain/links", **p)]
    return {
        **found[0],
        "scope": run(conn, "chain/scope", **p),
        "acceptance_criteria": [dict(ac, links=[l for l in links
                                                if l["acceptance_criterion"] == ac["external_id"]])
                                for ac in run(conn, "chain/acceptance_criteria", **p)],
        "links_without_ac": [l for l in links if l["acceptance_criterion"] is None],
        "defects": run(conn, "chain/defects", **p),
    }


def print_chain(c: dict) -> None:
    print(f"{c['external_id']} [{c['priority']} {c['status']}] {c['title']}")
    for s in c["scope"]:
        print(f"  scope {s['release']}" + (" (release-blocking)" if s["release_blocking"] else ""))

    def print_links(links: list, indent: str) -> None:
        for l in links:
            print(f"{indent}{l['test_case']} [{l['test_status']}] via {l['link']}")
            for e in l["executions"]:
                print(f"{indent}  {e['external_id']} {e['outcome']:<8}{e['release']} "
                      f"{e['environment']} {e['executed_at']:%Y-%m-%d}")

    for ac in c["acceptance_criteria"]:
        print(f"  {ac['external_id']} [{ac['status']}] {ac['criterion_type']}"
              + ("" if ac["links"] else "  (no test)"))
        print_links(ac["links"], "    ")
    if c["links_without_ac"]:
        print("  (tests linked without an AC)")
        print_links(c["links_without_ac"], "    ")
    for d in c["defects"]:
        print(f"  defect {d['external_id']} [{d['severity']} {d['status']}] {d['release']}"
              + (f" via {d['test_case']}" if d["test_case"] else ""))


if __name__ == "__main__":
    with get_engine().connect() as conn:
        chain = requirement_chain(conn, sys.argv[1] if len(sys.argv) > 1 else "REQ-001")
        print_chain(chain) if chain else print("not found")

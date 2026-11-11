# Manual baseline (W1-03)

My own answers to 3 golden scenarios, solved by hand before any query code existed. Every later version of the system is compared against these answers and times.

**Rules I followed**
- Only the reference data (`data/` CSVs) and the PDFs in `documents/`. No code, no AI.
- I didn't look at the `expected_*` columns in `golden_delivery_assurance_scenarios.csv` until all three were done.
- Each scenario was timed from first look to written answer.

**Tools used:** Datasette (a local web browser for the CSVs, loaded into SQLite), browsing and filtering only. No SQL until the answer was recorded.

---

## G-002 · TRACEABILITY

> Which release-blocking requirements have no active test coverage?

- **Started / finished:**
- **Time taken:**

### My answer

**REQ-065 and REQ-117.** These are the release-blocking requirements with no test cases at all.

### Evidence
| ID | File / document | Column or section | What it showed |
|---|---|---|---|
| REQ-065 | `release_scope.csv` | `release_blocking` | YES for release R26.10 |
| REQ-065 | `test_cases.csv` | `requirement_id` | No test case points to it |
| REQ-117 | `release_scope.csv` | `release_blocking` | YES for release R27.01 |
| REQ-117 | `test_cases.csv` | `requirement_id` | No test case points to it |

### How I got there
1. Filtered `release_scope` to `release_blocking = YES`. That's 60 rows across R26.10, R26.11 and R27.01.
2. Clicked through to each requirement's row page and checked whether any test case linked to it.
3. Listed the requirements with no linked test cases.

### Confidence and doubts
- **Confidence (low / medium / high):**
- **What I wasn't sure about:**
- **What "release-blocking" and "active" meant in my answer:** "Release-blocking" meant `release_blocking = YES` in any release. I didn't limit it to one release. I treated **any linked test as coverage** and didn't check the test's `status`.
- **Experience:** slow and tedious. Every blocking requirement needed its own page visit, with no way to see them all at once.

### Checked with SQL (after recording my answer)

Run in Datasette's SQL box once my answer above was written down:

```sql
SELECT rs.release, rs.requirement_id, r.priority
FROM release_scope rs
JOIN requirements r ON r.requirement_id = rs.requirement_id
WHERE rs.release_blocking = 'YES'
  AND NOT EXISTS (
        SELECT 1 FROM test_cases tc
        WHERE tc.requirement_id = rs.requirement_id
          AND tc.status = 'ACTIVE'
  )
ORDER BY rs.release, rs.requirement_id;
```

It returned **8** requirements: my 2, plus 6 that have tests whose status is only `NEEDS_REVIEW`.

| Release | Requirement | Priority | Tests (all `NEEDS_REVIEW`) |
|---|---|---|---|
| R26.10 | REQ-005 | P1 | TC-0009, TC-0010 |
| R26.10 | REQ-021 | P1 | TC-0029, TC-0030 |
| R26.10 | REQ-059 | P1 | TC-0081, TC-0082 |
| R26.10 | REQ-065 | P1 | *(none, in my answer)* |
| R26.10 | REQ-072 | P1 | TC-0097, TC-0098 |
| R26.11 | REQ-074 | P1 | TC-0100, TC-0101 |
| R26.11 | REQ-090 | **P0** | TC-0119, TC-0120 |
| R27.01 | REQ-117 | P1 | *(none, in my answer)* |

Removing the line `AND tc.status = 'ACTIVE'` returns only my 2. That single condition is the whole difference.

**What I learned:** I answered "which have *no tests*?" when the question asked "which have *no active tests*?" A test under review isn't verified coverage, which is the glossary's point that having a test isn't the same as being verified. REQ-090 is the clearest case: a P0 requirement that blocks R26.11 and looks covered but has no test ready.

**Decisions this raises for W2-03:**
- Does "active" mean `status = ACTIVE` only, or does a test also need a recent passing execution?
- Should the report cover every release, or only the next one?

---

## G-011 · COVERAGE_GAP

> Assess coverage for REQ-013.

- **Started / finished:**
- **Time taken:**

### My answer

**REQ-013 has no test coverage.** It has no test cases and no traceability links. Its two acceptance criteria are both still `DRAFT`. It's a P2 requirement, in scope for R27.01 but not release-blocking, and it has no defects.

- **Verdict (covered / partial / gap):**
- **What should happen next, and in what order:**

### Evidence
| ID | File / document | Column or section | What it showed |
|---|---|---|---|
| REQ-013 | `requirements.csv` | `priority`, `release` | P2, R27.01 |
| REQ-013 | `release_scope.csv` | `in_scope`, `release_blocking` | In scope for R27.01, not blocking |
| AC-0040, AC-0041 | `acceptance_criteria.csv` | `status` | Both `DRAFT` |
| REQ-013 | `test_cases.csv` | `requirement_id` | No test case points to it |
| REQ-013 | `traceability_links.csv` | `requirement_id` | No links |
| REQ-013 | `defects.csv` | `requirement_id` | No defects |

### How I got there
1. Opened REQ-013's row page in Datasette and read its priority and release.
2. Checked the tables linking to it: release scope, ACs, test cases, traceability links and defects.
3. Checked the status of each linked AC.

### Confidence and doubts
- **Confidence (low / medium / high):**
- **What I wasn't sure about:**

---

## G-007 · RELEASE

> Can we release with an open S1 defect?

- **Started / finished:**
- **Time taken:**

### My answer
- **Decision (e.g. GO / NO-GO / CONDITIONAL):**
- **Reasons:**

### Evidence
| ID | File / document | Column or section | What it showed |
|---|---|---|---|
| | | | |

### How I got there
1.

### Confidence and doubts
- **Confidence (low / medium / high):**
- **What I wasn't sure about:**

---

## Summary

| Scenario | Category | Time | Needed PDFs? | Hard because of lookup or judgment? |
|---|---|---|---|---|
| G-002 | TRACEABILITY | | | |
| G-011 | COVERAGE_GAP | | | |
| G-007 | RELEASE | | | |

## After checking the answer key

Fill this in only after all three are done.

| Scenario | Matched expected? | What I missed or got differently |
|---|---|---|
| G-002 | | |
| G-011 | | |
| G-007 | | |

## Check yourself
- Which scenarios needed the PDFs, and which needed only the CSVs?
- Which were hard because of judgment rather than lookup?

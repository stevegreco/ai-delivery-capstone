# Issue backlog template

## File header

```markdown
# Issue backlog

These are draft issues, grouped by week. Each week becomes a milestone, and each `###` heading becomes an issue.

**Labels**
- Type: `learn` (reading/exploring), `build` (code), `decide` (ADR), `eval` (measurement)
- Week: `week-N`
- `stretch`: optional, and the first to cut if behind

**Template:** each issue has **Learn** (the concept), **Do** (the tasks), **Done when** (exit criteria) and **Check yourself** (questions you should be able to answer afterward).
```

## One issue

```markdown
### W<week>-<nn> · <imperative title>
`week-<n>` `<type>` [`stretch`]
- **Learn:** <the concept this issue teaches, in one sentence>
- **Do:** <concrete tasks, naming the files or data involved>
- **Done when:** <checkable exit criteria, usually a file that exists or a number that matches>
- **Check yourself:** <1–2 questions that test the concept, not the task>
```

## Example

```markdown
### W1-02 · Explore the reference data by hand
`week-1` `learn`
- **Learn:** How to profile a dataset before trusting it.
- **Do:** Load the CSVs into a notebook, SQLite or a spreadsheet. Count rows, look at the enum values, and follow one record end to end.
- **Done when:** `docs/notes/data-profile.md` lists row counts, the key columns, the enum values and at least 3 data oddities.
- **Check yourself:** Which columns tell you a record is *active*? What does an orphaned link look like in this data?
```

## Guidance

- **Week 1** is mostly `learn` and one `eval` issue where the learner solves target tasks by hand. That is the first baseline.
- Every design choice the learner must own (stack, data model, chunking, metrics, model choice) is a `decide` issue whose output is an ADR in `docs/adr/NNNN-title.md`.
- Introduce an `eval` issue in the same week as the first AI `build` issue.
- "Done when" must be checkable by someone else. Avoid "understands X".
- "Check yourself" questions should have a wrong answer that sounds right. Example: "Why isn't *has a test* the same as *is verified*?"

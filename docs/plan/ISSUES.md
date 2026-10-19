# Issue backlog

These are draft GitHub issues, grouped by week. Each week becomes a milestone, and each `###` heading becomes an issue.

**Labels**
- Type: `learn` (reading/exploring), `build` (code), `decide` (ADR), `eval` (measurement)
- Week: `week-N`
- `stretch`: optional

**Template:** each issue has **Learn** (the concept), **Do** (the tasks), **Done when** (exit criteria) and **Check yourself** (questions you should be able to answer afterward).

---

## Week 1: Orientation & domain

### W1-01 · Map the domain: build a glossary and concept diagram
`week-1` `learn`
- **Learn:** The vocabulary of delivery assurance (requirement, AC, test, execution, defect, traceability, release scope, readiness) and how the pieces relate.
- **Do:** Read `PROJECT_BRIEF.md` and §1–§3 and §9 of the use-case definition. Write `docs/glossary.md`. Sketch an entity-relationship diagram by hand or in Mermaid.
- **Done when:** The glossary and diagram exist, and you can describe the Requirement → AC → Test → Result chain without notes.
- **Check yourself:** What's the difference between *coverage* and *readiness*? Why isn't "has a test" the same as "is verified"?

### W1-02 · Explore the reference data by hand
`week-1` `learn`
- **Learn:** How to profile a dataset before trusting it.
- **Do:** Load the `data/` CSVs into a notebook, SQLite or a spreadsheet. Count rows, look at the values of status, priority and type, and follow one requirement end to end (REQ → ACs → tests → executions → defects).
- **Done when:** `docs/notes/data-profile.md` lists row counts, the key columns, the enum values and at least 3 data oddities you noticed.
- **Check yourself:** Which columns tell you a test is *active*? What does an orphaned link look like in this data?

### W1-03 · Solve 5 golden scenarios manually
`week-1` `eval`
- **Learn:** What a correct answer looks like. You're the first "model."
- **Do:** Choose 5 scenarios from `developer_aid/golden_delivery_assurance_scenarios.csv` in different categories. Answer each using only the data and PDFs. Time yourself.
- **Done when:** Your answers, the evidence you used and the time taken are recorded in `docs/notes/manual-baseline.md`.
- **Check yourself:** Which scenarios needed the PDFs and which needed only the CSVs? Which were hard because of judgment rather than lookup?

### W1-04 · ADR 0001: choose the stack
`week-1` `decide`
- **Learn:** How to make and record a technical decision.
- **Do:** Compare at least two options (e.g. Python vs TypeScript, SQLite vs Postgres) on learning value, AI library support and your own familiarity. Write `docs/adr/0001-stack.md`.
- **Done when:** The ADR is merged. Only now do you create the minimal project skeleton for the chosen stack.
- **Check yourself:** Which decisions can you safely postpone, and why?

---

## Week 2: Delivery model & structured ingestion

### W2-01 · ADR 0002: design the normalized delivery model
`week-2` `decide`
- **Learn:** Separating the *internal model* from *source formats* (§1C, §1O of the use-case definition).
- **Do:** Define the core entities and fields. Compare them to `schema_ddl.sql` and decide what to keep, rename or add (e.g. version, source, provenance).
- **Done when:** The ADR includes the model and explains how Set A's "Issue Key" would map onto it.
- **Check yourself:** Where does *provenance* (the source file, row and version) live in your model?

### W2-02 · Load the reference CSVs into the model
`week-2` `build`
- **Learn:** Writing a loader: parse, type-check, insert, and make it idempotent.
- **Do:** Write a loader for the 11 CSVs into your store, with a command to rebuild the database from scratch.
- **Done when:** One command rebuilds the database, and the row counts match your Week 1 profile.
- **Check yourself:** What happens if you run the loader twice?

### W2-03 · Data-quality checks
`week-2` `build`
- **Learn:** Referential integrity and why you validate inputs before analysis.
- **Do:** Write checks for dangling foreign keys, duplicate IDs, invalid enum values and missing required fields. Output a report.
- **Done when:** The report runs and lists the problems actually present in the data.
- **Check yourself:** Which of these problems are deliberate test cases planted in the dataset, and which are just noise?

---

## Week 3: Deterministic traceability & readiness

### W3-01 · Traceability queries
`week-3` `build`
- **Learn:** Graph-like traversal over relational data.
- **Do:** Write functions that return the full chain for a requirement, plus reverse lookup from a test or defect back to its requirement.
- **Done when:** Given REQ-001 you get its ACs, tests, latest run results and defects, with IDs.
- **Check yourself:** Should "latest result" mean the newest run per release or per environment?

### W3-02 · Coverage gap and orphan report
`week-3` `build`
- **Learn:** Coverage as a set of rules rather than a single number.
- **Do:** Find P0/P1 in-scope requirements with no active test, ACs with no test, tests with no AC or requirement, and deprecated tests still linked to requirements.
- **Done when:** The report answers the COVERAGE_GAP and TRACEABILITY golden scenarios. Compare it with your W1-03 answers.
- **Check yourself:** How do release scope and priority change what counts as a gap?

### W3-03 · Readiness rules v0
`week-3` `build`
- **Learn:** Encoding a go/no-go policy (see Doc 05) as explicit rules.
- **Do:** Define rules such as "an open Critical defect on an in-scope P0 means BLOCKED." Return the decision, the list of reasons and the evidence IDs.
- **Done when:** It produces a readiness decision for release R26.10 with every reason traceable to rows.
- **Check yourself:** Why must this logic stay deterministic even after you add an LLM?

---

## Week 4: First LLM calls with structured outputs

### W4-01 · LLM client wrapper with TokenOps logging
`week-4` `build`
- **Learn:** API basics such as messages, system prompts and temperature, plus what tokens are and how they're priced.
- **Do:** Write a thin wrapper that logs model, input and output tokens, latency, estimated cost and a prompt version to a local log or table for every call.
- **Done when:** A test call writes a log row. `.env.example` is committed and `.env` is not.
- **Check yourself:** Why log a prompt *version*?

### W4-02 · Hand-label 40 acceptance criteria
`week-4` `eval`
- **Learn:** Labeling is part of design, and your labels define "correct."
- **Do:** Choose 40 ACs, mixing obvious and borderline cases. Label each as testable, ambiguous or incomplete, with a reason.
- **Done when:** The labels are saved as a CSV with a short labeling guide.
- **Check yourself:** Which cases were you unsure about? Those are where the model will struggle too.

### W4-03 · AC quality classifier with schema-validated output
`week-4` `build`
- **Learn:** Structured outputs, JSON schemas, validation and retries.
- **Do:** Prompt the LLM to classify an AC and return `{label, reasons[], suggested_rewrite, confidence}`. Validate against a schema and reject malformed output.
- **Done when:** It runs on your 40 labeled ACs, and you have an agreement rate plus a list of disagreements.
- **Check yourself:** When the model disagrees with you, who is right? Did the disagreements lead you to change your labels?

---

## Week 5: Evaluation harness

### W5-01 · Golden-scenario evaluation runner
`week-5` `eval`
- **Learn:** Repeatable evaluation: fixed inputs, versioned system, comparable outputs.
- **Do:** Write a runner that takes each golden scenario, calls the matching capability and stores the output alongside the expected values.
- **Done when:** One command runs all 30 scenarios. Ones whose capability isn't built yet are marked `NOT_IMPLEMENTED` instead of failing.
- **Check yourself:** Why build this *before* RAG?

### W5-02 · Metrics per category
`week-5` `eval` `decide`
- **Learn:** Precision and recall on IDs, decision-state accuracy, and when to use an LLM as a judge (and when not to).
- **Do:** Define a scoring method for each category, e.g. precision and recall on `expected_requirement_ids` and exact match on `expected_decision_state`. Record the choices in an ADR.
- **Done when:** The runner outputs a scorecard, and the baseline is saved to `eval/baselines/`.
- **Check yourself:** What does a 100% score *not* tell you?

---

## Week 6: Document ingestion

### W6-01 · PDF text and table extraction
`week-6` `build`
- **Learn:** Why PDF parsing is lossy, and how tables are different from prose.
- **Do:** Extract text and tables from all 8 PDFs while keeping section headings. Compare at least two parsing approaches on one document.
- **Done when:** Each PDF yields structured sections, and you've noted where extraction fails.
- **Check yourself:** How would you tell that a table was extracted wrong?

### W6-02 · Diagram ingestion (Doc 05 workflow)
`week-6` `build`
- **Learn:** Multimodal input: turning a diagram into text the system can use.
- **Do:** Extract the release-governance workflow from Doc 05 with a vision model or by manual transcription, and represent it as text or structured steps.
- **Done when:** The workflow steps and gates exist as data with a citation to Doc 05.
- **Check yourself:** What information is only in the diagram?

### W6-03 · Chunking and metadata
`week-6` `build` `decide`
- **Learn:** Chunking trade-offs (fixed size, by section, semantic) and why metadata matters as much as text.
- **Do:** Chunk all documents. Attach `document_id`, section, version, status and effective_date from `document_registry.csv`. Record your strategy in an ADR.
- **Done when:** Every chunk has complete metadata, and Doc 98 chunks are marked `ARCHIVED`.
- **Check yourself:** What breaks if chunks are too small? Too large?

---

## Week 7: Retrieval (RAG)

### W7-01 · Embeddings and a vector index
`week-7` `build`
- **Learn:** What embeddings are, cosine similarity, and how a vector store works.
- **Do:** Embed the chunks, store them, and write a `search(query, k)` function.
- **Done when:** Queries return chunks with scores and metadata.
- **Check yourself:** Why might "refund window" match the archived spec more strongly than the current one?

### W7-02 · Keyword vs vector vs hybrid search
`week-7` `eval`
- **Learn:** Lexical vs semantic retrieval, and how to merge their results (e.g. reciprocal rank fusion, RRF).
- **Do:** Run all three methods on 10 queries taken from the golden scenarios. Measure recall@k against `expected_document_ids`.
- **Done when:** A results table exists and you've chosen a default method.
- **Check yourself:** When does keyword search beat vectors? Think about IDs like `REQ-042`.

### W7-03 · Version-aware retrieval
`week-7` `build`
- **Learn:** Filtering on metadata and why similarity alone is unsafe here (§6).
- **Do:** Exclude or down-rank archived and superseded documents by default, and allow them only when asked explicitly ("what changed since v1?").
- **Done when:** The VERSIONING golden scenario passes, and archived content never appears in a default answer.
- **Check yourself:** Is it better to filter before ranking or after? Why?

---

## Week 8: Grounded generation & human review

### W8-01 · Citations and unsupported-claim checks
`week-8` `build`
- **Learn:** Grounding, citation formats, and checking claims against the source.
- **Do:** Require every generated statement to cite chunk or row IDs. Add a check that flags claims without support in the cited text.
- **Done when:** A deliberately ungrounded prompt gets flagged or blocked.
- **Check yourself:** Is a citation that exists the same as a claim that's supported?

### W8-02 · Generate acceptance criteria for uncovered requirements
`week-8` `build`
- **Learn:** Combining retrieval with generation for a specific task.
- **Do:** For requirements with missing or ambiguous ACs, generate Given/When/Then candidates using retrieved standards (Doc 04) as context.
- **Done when:** The candidates are stored as `DRAFT` with citations, and your W4 classifier rates them testable.
- **Check yourself:** How do you stop the model from inventing business rules?

### W8-03 · Generate test cases
`week-8` `build`
- **Learn:** Test design techniques (positive, negative, boundary, exception) and API tests driven by OpenAPI.
- **Do:** Generate tests from approved ACs, plus API scenarios from `openapi_sample.json` and `samples/`. Link each one to its AC.
- **Done when:** The TEST_GENERATION scenario passes, and each generated test carries its traceability link.
- **Check yourself:** Which boundary values came from the spec, and which did the model guess?

### W8-04 · Human review gate
`week-8` `build`
- **Learn:** Human-in-the-loop design, and audit trails.
- **Do:** Build a review queue where you can approve, edit or reject generated ACs and tests. Record the reviewer, timestamp and diff. Only approved items enter the traceability graph.
- **Done when:** Nothing generated becomes `ACTIVE` without an approval record.
- **Check yourself:** What should happen to approvals when the source requirement changes?

---

## Week 9: Change impact & release readiness

### W9-01 · Change impact analysis
`week-9` `build`
- **Learn:** How a change propagates through a dependency graph.
- **Do:** For each change in `requirement_changes.csv` (and Doc 07), find the impacted ACs, tests, runs and defects. Classify each as regenerate, revalidate or no action.
- **Done when:** The CHANGE_IMPACT scenario passes, with the evidence IDs listed.
- **Check yourself:** When should a deterministic check catch the impact, and when do you need the LLM's judgment?

### W9-02 · Stale test detection
`week-9` `build`
- **Learn:** Staleness defined by versions and dates (§15).
- **Do:** Flag tests whose last passing run is older than their requirement's current version or effective date.
- **Done when:** You have a stale-test list with reasons.
- **Check yourself:** Is a passing run from before the change still evidence?

### W9-03 · Readiness explanation layer
`week-9` `build`
- **Learn:** Rules make the decision and the LLM explains it, which keeps it safe and auditable.
- **Do:** Feed the v0 readiness result (with W9 additions) to the LLM to produce a cited summary for a release manager. The LLM may not change the decision.
- **Done when:** The RELEASE and DELIVERY_READINESS scenarios pass, and every sentence in the summary cites evidence.
- **Check yourself:** How would you catch the LLM softening a BLOCKED decision?

---

## Week 10: Multi-model comparison & TokenOps

### W10-01 · Compare two or more models
`week-10` `eval`
- **Learn:** Trade-offs between quality, cost and latency, and choosing a model per task.
- **Do:** Run the full evaluation on at least two models, perhaps one large and one small. Produce a per-category comparison table.
- **Done when:** An ADR records which model handles which task, and why.
- **Check yourself:** Where is the cheaper model good enough?

### W10-02 · Context minimization and caching
`week-10` `build` `eval`
- **Learn:** Prompt caching, trimming context, and how much retrieved context is actually needed.
- **Do:** Cache the repeated system and standards context. Experiment with smaller k and summarized context. Measure the token savings and the effect on quality.
- **Done when:** You have a before/after table of tokens, cost, latency and evaluation score.
- **Check yourself:** At what point does cutting context start to hurt quality?

### W10-03 · Observability report
`week-10` `build`
- **Learn:** Tracing AI calls: which request, which prompt, which chunks, and what it cost.
- **Do:** Link each output to its trace (prompt version, model, retrieved chunk IDs, tokens). Add a simple usage summary.
- **Done when:** For any generated artifact you can show exactly how it was produced.
- **Check yourself:** What would you look at first if quality suddenly dropped?

---

## Week 11: Generalization (Sets A, B, C)

### W11-01 · Adapter interface and Set A (Jira)
`week-11` `build` `decide`
- **Learn:** The adapter pattern, and putting mapping in config instead of code.
- **Do:** Define the adapter contract. Onboard Set A (Jira CSVs, xlsx tests, PDF) through mapping config.
- **Done when:** Coverage and readiness run on Set A **without editing core logic**.
- **Check yourself:** What was hardest to map, and why?

### W11-02 · Set B (Kanban) and Set C (Mobile Banking)
`week-11` `build`
- **Learn:** Testing how well your model generalizes: workflow-state history (B) and JSON stories plus NFR/security requirements (C).
- **Do:** Onboard both sets. Log every core-logic change you were tempted to make in an ADR.
- **Done when:** Gap and readiness reports run for all three sets.
- **Check yourself:** Did your Week 2 model hold up? What would you redesign?

---

## Week 12: Reviewer experience & defense

### W12-01 · Coverage and readiness dashboard
`week-12` `build`
- **Learn:** Presenting evidence to a reviewer so the reasoning is visible, not just the verdict.
- **Do:** Build a minimal UI showing coverage by priority, the readiness decision and reasons, and drill-down to evidence.
- **Done when:** A reviewer can go from "BLOCKED" to the exact defect or run in two clicks.

### W12-02 · Traceability graph view
`week-12` `build` `stretch`
- **Do:** Visualize Requirement → AC → Test → Run → Defect for a selected requirement or release.

### W12-03 · Agentic test execution with approval gates
`week-12` `build` `stretch`
- **Learn:** Agent loops, tool calling, and stop conditions.
- **Do:** Let an agent propose test runs through `api/mock_test_runner_contract.json`. Require human approval before execution. Capture the results as evidence. Stop when evidence is missing or a gate fails.
- **Done when:** The EXECUTION and AI_SAFETY scenarios pass.

### W12-04 · Final walkthrough and defense prep
`week-12` `learn`
- **Do:** Rerun the full evaluation and compare it with the Week 5 baseline. Prepare answers to §1P ("What the team should be able to explain"). Write the retrospective.
- **Done when:** You can demo the end-to-end scenario (§26) and explain every design decision from your ADRs.

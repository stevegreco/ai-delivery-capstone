# Issue backlog

These are draft GitHub issues, grouped by week. Each week becomes a milestone, and each `###` heading becomes an issue.

**Labels**
- Type: `learn` (reading/exploring), `build` (code), `decide` (ADR), `eval` (measurement)
- Week: `week-N`
- `stretch`: optional, and the first to cut if behind

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

## Week 2: Delivery model & deterministic core

### W2-01 · ADR 0002: design the normalized delivery model
`week-2` `decide`
- **Learn:** Separating the *internal model* from *source formats* (§1C, §1O of the use-case definition).
- **Do:** Define the core entities and fields. Compare them to `schema_ddl.sql` and decide what to keep, rename or add (e.g. version, source, provenance). Give every artifact and traceability link an **origin**: `HUMAN`, `AI_SUGGESTED` or `AI_APPROVED`, plus who created it, when, and (for AI) the model and prompt version.
- **Done when:** The ADR includes the model, explains how Set A's "Issue Key" would map onto it, and defines the origin fields.
- **Check yourself:** Where does *provenance* (the source file, row and version) live in your model? How would you list every link the AI created?

### W2-02 · Load and validate the reference CSVs
`week-2` `build`
- **Learn:** Writing an idempotent loader, and checking referential integrity before analysis.
- **Do:** Load the 11 CSVs into your store with one rebuild command. Add checks for dangling foreign keys, duplicate IDs, invalid enum values and missing required fields.
- **Done when:** One command rebuilds the database, the row counts match your Week 1 profile, and a data-quality report lists the problems actually in the data.
- **Check yourself:** What happens if you run the loader twice? Which data problems are deliberate test cases planted in the dataset?

### W2-03 · Traceability queries and coverage gap report
`week-2` `build`
- **Learn:** Graph-like traversal over relational data, and coverage as a set of rules rather than a single number.
- **Do:** Write functions that return the full chain for a requirement, plus reverse lookup from a test or defect. Report P0/P1 in-scope requirements with no active test, ACs with no test, orphaned tests, and deprecated tests still linked to requirements.
- **Done when:** Given REQ-001 you get its full chain with IDs, and the report answers the COVERAGE_GAP and TRACEABILITY golden scenarios. Compare it with your W1-03 answers.
- **Check yourself:** How do release scope and priority change what counts as a gap?

### W2-04 · Readiness rules v0
`week-2` `build`
- **Learn:** Encoding a go/no-go policy (see Doc 05) as explicit rules.
- **Do:** Define rules such as "an open Critical defect on an in-scope P0 means BLOCKED." Return the decision, the list of reasons and the evidence IDs.
- **Done when:** It produces a readiness decision for release R26.10 with every reason traceable to rows.
- **Check yourself:** Why must this logic stay deterministic even after you add an LLM?

---

## Week 3: First LLM calls & evaluation harness

### W3-01 · LLM client wrapper with TokenOps logging
`week-3` `build`
- **Learn:** API basics such as messages, system prompts and temperature, plus what tokens are and how they're priced.
- **Do:** Write a thin wrapper that logs model, input and output tokens, latency, estimated cost and a prompt version to a local log or table for every call.
- **Done when:** A test call writes a log row. `.env.example` is committed and `.env` is not.
- **Check yourself:** Why log a prompt *version*?

### W3-02 · Hand-label 30 acceptance criteria
`week-3` `eval`
- **Learn:** Labeling is part of design, and your labels define "correct."
- **Do:** Choose 30 ACs, mixing obvious and borderline cases. Label each as testable, ambiguous or incomplete, with a reason.
- **Done when:** The labels are saved as a CSV with a short labeling guide.
- **Check yourself:** Which cases were you unsure about? Those are where the model will struggle too.

### W3-03 · AC quality classifier with schema-validated output
`week-3` `build`
- **Learn:** Structured outputs, JSON schemas, validation and retries.
- **Do:** Prompt the LLM to classify an AC and return `{label, reasons[], suggested_rewrite, confidence}`. Validate against a schema and reject malformed output.
- **Done when:** It runs on your 30 labeled ACs, and you have an agreement rate plus a list of disagreements.
- **Check yourself:** When the model disagrees with you, who is right?

### W3-04 · Golden-scenario evaluation runner and metrics
`week-3` `eval` `decide`
- **Learn:** Repeatable evaluation, precision and recall on IDs, decision-state accuracy, and when to use an LLM as a judge (and when not to).
- **Do:** Write a runner over the 30 golden scenarios. Mark capabilities that aren't built yet as `NOT_IMPLEMENTED`. Define a scoring method for each category and record the choices in an ADR.
- **Done when:** One command produces a scorecard, and the baseline (covering the W2 rules and W3 classifier) is saved to `eval/baselines/`.
- **Check yourself:** Why build this *before* RAG? What does a 100% score *not* tell you?

---

## Week 4: Document ingestion & retrieval

### W4-01 · PDF extraction: text, tables and diagram
`week-4` `build`
- **Learn:** Why PDF parsing is lossy, how tables differ from prose, and multimodal input.
- **Do:** Extract text and tables from all 8 PDFs while keeping section headings. Extract the Doc 05 workflow diagram as structured steps, using a vision model or manual transcription.
- **Done when:** Each PDF yields structured sections, the Doc 05 workflow exists as data with a citation, and you've noted where extraction fails.
- **Check yourself:** How would you tell that a table was extracted wrong? What information is only in the diagram?

### W4-02 · Chunking and metadata
`week-4` `build` `decide`
- **Learn:** Chunking trade-offs (fixed size, by section, semantic) and why metadata matters as much as text.
- **Do:** Chunk all documents. Attach `document_id`, section, version, status and effective_date from `document_registry.csv`. Record your strategy in an ADR.
- **Done when:** Every chunk has complete metadata, and Doc 98 chunks are marked `ARCHIVED`.
- **Check yourself:** What breaks if chunks are too small? Too large?

### W4-03 · Embeddings and hybrid search
`week-4` `build` `eval`
- **Learn:** What embeddings are, cosine similarity, lexical vs semantic retrieval, and how to merge their results (e.g. reciprocal rank fusion, RRF).
- **Do:** Embed and index the chunks. Implement keyword, vector and hybrid search, and measure recall@k for each on 10 queries taken from the golden scenarios.
- **Done when:** A results table exists and you've chosen a default method.
- **Check yourself:** When does keyword search beat vectors? Think about IDs like `REQ-042`.

### W4-04 · Version-aware retrieval
`week-4` `build`
- **Learn:** Filtering on metadata and why similarity alone is unsafe here (§6).
- **Do:** Exclude or down-rank archived and superseded documents by default, and allow them only when asked explicitly ("what changed since v1?").
- **Done when:** The VERSIONING golden scenario passes, and archived content never appears in a default answer.
- **Check yourself:** Is it better to filter before ranking or after? Why?

### W4-05 · Extract requirements from documents and reconcile with the CSV
`week-4` `build` `stretch`
- **Learn:** Extracting entities from unstructured text (requirements, actors, rules, dependencies), and reconciling two sources of truth.
- **Do:** Use the LLM to extract requirements from the current PDFs into the delivery model, with citations. Compare them with `requirements.csv`: what's in the documents but missing from the CSV, what's in the CSV with no document support, and where the two disagree.
- **Done when:** A reconciliation report lists each mismatch with document and row citations.
- **Check yourself:** When the document and the CSV disagree, which should win, and who decides?

---

## Week 5: Grounded generation & human review

### W5-01 · Citations and unsupported-claim checks
`week-5` `build`
- **Learn:** Grounding, citation formats, and checking claims against the source.
- **Do:** Require every generated statement to cite chunk or row IDs. Add a check that flags claims without support in the cited text. Record the model, prompt version and retrieved chunk IDs with each output.
- **Done when:** A deliberately ungrounded prompt gets flagged or blocked, and every output can be traced back to how it was produced.
- **Check yourself:** Is a citation that exists the same as a claim that's supported?

### W5-02 · Generate acceptance criteria for uncovered requirements
`week-5` `build`
- **Learn:** Combining retrieval with generation for a specific task.
- **Do:** For requirements with missing or ambiguous ACs, generate Given/When/Then candidates using retrieved standards (Doc 04) as context.
- **Done when:** The candidates are stored as `DRAFT` with citations, and your W3 classifier rates them testable.
- **Check yourself:** How do you stop the model from inventing business rules?

### W5-03 · Generate test cases
`week-5` `build`
- **Learn:** Test design techniques (positive, negative, boundary, exception) and API tests driven by OpenAPI.
- **Do:** Generate tests from approved ACs, plus API scenarios from `openapi_sample.json` and `samples/`. Link each one to its AC.
- **Done when:** The TEST_GENERATION scenario passes, and each generated test carries its traceability link.
- **Check yourself:** Which boundary values came from the spec, and which did the model guess?

### W5-04 · Human review gate
`week-5` `build`
- **Learn:** Human-in-the-loop design, and audit trails.
- **Do:** Build a review queue, a CLI being enough, where you can approve, edit or reject generated ACs and tests. Record the reviewer, timestamp and diff. Only approved items enter the traceability graph.
- **Done when:** Nothing generated becomes `ACTIVE` without an approval record.
- **Check yourself:** What should happen to approvals when the source requirement changes?

### W5-05 · Detect conflicts between current documents
`week-5` `build`
- **Learn:** Comparing statements across sources, and the difference between a real conflict and different wording.
- **Do:** For each domain, retrieve related statements from the current documents (e.g. an NFR limit in Doc 06 vs a functional spec) and ask the LLM to flag contradictions. Output each conflict with citations to both sides and a suggested question for the requirement owner.
- **Done when:** A conflict report exists and you've checked at least 5 flagged conflicts by hand. No golden scenario covers conflicts between current documents, so add 2–3 of your own to the evaluation set.
- **Check yourself:** How many flagged conflicts were real? What made the false ones look like conflicts?

---

## Week 6: Change impact, readiness & model comparison

### W6-01 · Change impact and stale test detection
`week-6` `build`
- **Learn:** How a change propagates through a dependency graph, and staleness defined by versions and dates (§14–§15).
- **Do:** For each change in `requirement_changes.csv` (and Doc 07), find the impacted ACs, tests, runs and defects, and classify each as regenerate, revalidate or no action. Flag tests whose last passing run predates their requirement's current version.
- **Done when:** The CHANGE_IMPACT scenario passes, and you have an impact list and a stale-test list, both with evidence IDs.
- **Check yourself:** Is a passing run from before the change still evidence?

### W6-02 · Readiness explanation layer
`week-6` `build`
- **Learn:** Rules make the decision and the LLM explains it, which keeps it safe and auditable.
- **Do:** Feed the readiness result (v0 rules plus W6-01 findings) to the LLM to produce a cited summary for a release manager. The LLM may not change the decision.
- **Done when:** The RELEASE and DELIVERY_READINESS scenarios pass, and every sentence in the summary cites evidence.
- **Check yourself:** How would you catch the LLM softening a BLOCKED decision?

### W6-03 · Compare two or more models
`week-6` `eval`
- **Learn:** Trade-offs between quality, cost and latency, and choosing a model per task.
- **Do:** Run the full evaluation on at least two models, perhaps one large and one small. Produce a per-category comparison table.
- **Done when:** An ADR records which model handles which task, and why.
- **Check yourself:** Where is the cheaper model good enough?

---

## Week 7: TokenOps & generalization

### W7-01 · Context minimization and caching
`week-7` `build` `eval`
- **Learn:** Prompt caching, trimming context, and how much retrieved context is actually needed.
- **Do:** Cache the repeated system and standards context. Experiment with smaller k and summarized context. Measure the token savings and the effect on quality.
- **Done when:** You have a before/after table of tokens, cost, latency and evaluation score.
- **Check yourself:** At what point does cutting context start to hurt quality?

### W7-02 · Adapter interface and Set A (Jira)
`week-7` `build` `decide`
- **Learn:** The adapter pattern, and putting mapping in config instead of code.
- **Do:** Define the adapter contract. Onboard Set A (Jira CSVs, xlsx tests, PDF) through mapping config.
- **Done when:** Coverage and readiness run on Set A **without editing core logic**, and any core change you had to make is recorded in an ADR.
- **Check yourself:** What was hardest to map, and why? Did your Week 2 model hold up?

### W7-03 · Sets B (Kanban) and C (Mobile Banking)
`week-7` `build` `stretch`
- **Learn:** Testing how well your model generalizes: workflow-state history (B) and JSON stories plus NFR/security requirements (C).
- **Do:** Onboard both sets through adapters.
- **Done when:** Gap and readiness reports run for all three sets.

---

## Week 8: Reviewer experience & defense

### W8-01 · Coverage and readiness view
`week-8` `build`
- **Learn:** Presenting evidence to a reviewer so the reasoning is visible, not just the verdict.
- **Do:** Build a minimal UI or HTML report showing coverage by priority, the readiness decision and reasons, and drill-down to evidence.
- **Done when:** A reviewer can go from "BLOCKED" to the exact defect or run in two clicks.

### W8-02 · Final evaluation and defense prep
`week-8` `learn` `eval`
- **Do:** Rerun the full evaluation and compare it with the Week 3 baseline. Prepare answers to §1P ("What the team should be able to explain"). Write the retrospective.
- **Done when:** You can demo the end-to-end scenario (§26) and explain every design decision from your ADRs.

### W8-03 · Traceability graph view
`week-8` `build` `stretch`
- **Do:** Visualize Requirement → AC → Test → Run → Defect for a selected requirement or release.

### W8-04 · Agentic test execution with approval gates
`week-8` `build` `stretch`
- **Learn:** Agent loops, tool calling, and stop conditions.
- **Do:** Let an agent propose test runs through `api/mock_test_runner_contract.json`. Require human approval before execution. Capture the results as evidence. Stop when evidence is missing or a gate fails.
- **Done when:** The EXECUTION and AI_SAFETY scenarios pass.

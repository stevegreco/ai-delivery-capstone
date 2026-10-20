# Poteto review of the learning plan

A plain-language review of the 8-week plan against the project requirements and the supplied dataset. No code was changed. Read this if you want the consensus and the decisions worth making before Week 2 hardens.

Sources. [ROADMAP.md](ROADMAP.md), [ISSUES.md](ISSUES.md), [SUGGESTIONS.md](SUGGESTIONS.md), [PROJECT_BRIEF.md](../../PROJECT_BRIEF.md), [Capstone4_usecase_definition.md](../../Capstone4_usecase_definition.md), and the Capstone 4 dataset.

---

## Legend

Use this table whenever a short code appears later in the plan files or in older notes.

### Plan and issue codes

| Code | Meaning |
|---|---|
| W1 … W8 | Week 1 through Week 8 in the roadmap |
| W2-03 | An issue ID. Week number, then issue number that week. Example. W2-03 is the third issue in Week 2 |
| ADR | Architecture Decision Record. A short write-up of a choice you made and why. Lives under `docs/adr/` |
| stretch | Optional work. Cut first when time is short |
| cut order | The planned drop list when you fall behind. See [ROADMAP.md](ROADMAP.md) |

### Requirement shorthand (from PROJECT_BRIEF.md)

The brief lists ten **Required** capabilities. Older review notes called them R1 to R10. Prefer the plain name.

| Short | Plain name |
|---|---|
| R1 | Extract requirements and entities from documents, and return structured outputs |
| R2 | Detect ambiguity, conflicts, and missing information |
| R3 | Generate acceptance criteria, with human review |
| R4 | Keep Requirement → Acceptance criterion → Test → Result links |
| R5 | Generate test scenarios and test cases |
| R6 | Change impact analysis and delivery readiness |
| R7 | Retrieval (RAG) over specs, standards, and approved examples |
| R8 | Golden-set evaluation and multi-model comparison |
| R9 | TokenOps. Track tokens, cost, latency, and manage context |
| R10 | Citations and controls for unsupported claims |

The brief also has **Recommended** items (nice to have) and **Optional / Stretch** items (agentic test runs, graph view, and similar).

### Dataset and evaluation codes

| Code | Meaning |
|---|---|
| REQ-001 | A requirement ID in `requirements.csv` |
| AC-0001 | An acceptance criterion ID in `acceptance_criteria.csv` |
| DOC-01 … DOC-07 | Current source PDFs in the document registry |
| DOC-98 | The archived checkout PDF. Must not win over current guidance |
| G-001 | A golden evaluation scenario ID (there are 30, G-001 to G-030) |
| golden set | The 30 evaluation scenarios used as smoke tests |
| RAG | Retrieval-augmented generation. Search documents, then generate with that context |
| TokenOps | Measuring and controlling token use, cost, and latency for LLM calls |
| Set A / B / C | Three extra project packs used to test whether your model generalizes (Jira, Kanban, mobile banking) |

### Suggestion codes

[SUGGESTIONS.md](SUGGESTIONS.md) lists known plan concerns as S1 to S14.

| Code | One-line meaning | Status |
|---|---|---|
| S1 | Golden set is too small to rank models | Open |
| S2 | Data is synthetic and some labels are wrong | Open |
| S3 | “Block unsupported claims” cannot be a hard guarantee | Open |
| S4 / S7 | No clear quality bar for generated tests | Open |
| S5 | Add requirement extraction from PDFs | Decided → W4-05 (stretch) |
| S6 | Add conflict detection between current documents | Decided → W5-05 |
| S8 | Protect the 8-week schedule with a cut order | Decided |
| S9 | Record where every artifact and link came from | Decided → W2-01 |
| S10 | Don’t let generated tests inflate coverage | Open |
| S11 | Design the review queue against rubber-stamping | Open |
| S12 | Respect document classification (e.g. CONFIDENTIAL) | Open |
| S13 | Treat source text as untrusted (prompt injection) | Open |
| S14 | Expect Sets A/B/C to force some core model changes | Open |

### Other words used in this review

| Word | Meaning here |
|---|---|
| readiness | Go / no-go for a release, with reasons and evidence |
| coverage gap | An in-scope requirement (or AC) that lacks an active test |
| provenance / origin | Who created an artifact (human, AI suggested, AI approved), when, and which model or prompt |
| hold-out set | Evaluation items you do not tune against, saved for the final score |
| defense | The final walkthrough where you explain design choices (§1P in the use-case doc) |

---

## Bottom line

The plan is a good learning plan. Keep it.

The big ideas are right.

1. Learn the domain before you code.
2. Build the deterministic core (data, links, readiness rules) before any LLM.
3. Build the evaluation harness at the same time as the first LLM feature.
4. Generalize to Sets A/B/C only after the reference project works.

The problems are bookkeeping. Wrong cut targets, a few issues out of order, and an evaluation set that cannot honestly rank models. Fix those on paper before Week 2 hardens.

---

## What the plan gets right

**Order.** Domain → rules with no AI → first LLM plus eval → document retrieval → grounded generation → change impact → TokenOps and adapters → defense. That matches the spirit of the use-case guide and is better for learning than “build everything then evaluate.”

**Safety split.** Rules make the readiness decision. The LLM explains it. That matches the project rule that deterministic work must stay separate from LLM work.

**Teaching shape.** Each issue has Learn, Do, Done when, and Check yourself. Week 1 makes you the first baseline by solving golden scenarios by hand.

**Already fixed suggestions.** Extraction stretch (S5), conflict detection (S6), cut order and hours (S8), and provenance fields (S9) are already reflected in the roadmap and issues.

---

## Problems, in plain English

### 1. A required skill sits only on optional work

The brief requires extracting requirements from documents. In the plan, that work is only **W4-05**, and it is marked stretch. The roadmap also says to cut it as soon as Week 4 runs long.

If you cut it, you never build a required capability.

**Fix.** Keep a thin version as core work. Extract from one current PDF and compare with the CSV. Full reconciliation can stay stretch. Stop treating W4-05 as the first thing to delete.

### 2. The cut list can erase defense answers

Cutting Sets B and C (**W7-03**) removes the material for three final-defense questions about onboarding those sets.

**Fix.** If code for B and C slips, still write a paper mapping of each set into your Week 2 model. That keeps the defense answerable.

### 3. Some evaluation scenarios have no owner

The golden file has 30 scenarios in 14 categories. Several categories never appear in any issue’s “Done when.”

Examples.

- Defect impact (5 scenarios)
- NFR performance validation
- Security test drafting
- Multi-source evidence
- AI safety about archived vs current docs (this one is wrongly tied to the agentic test-runner stretch issue)

**Fix.** Assign every golden scenario to one issue’s exit criteria. Move the archived-doc safety scenario to version-aware retrieval or conflict detection, not the optional test runner.

### 4. The golden set cannot rank models

Measured facts.

- 30 scenarios total
- 9 of 14 categories have only one scenario
- Three categories (ambiguity, coverage gap, defect impact) make up 17 of 30 rows

Week 6’s “compare two models” can still teach cost and latency. Per-category quality rankings at one sample each are noise.

**Fix.** Treat the golden set as a smoke and regression suite. Build larger hand-labeled sets for tasks you care about (you already plan 30 ACs for the classifier). Freeze a hold-out set in Week 3 and score it only in Week 8. Decide S1.

### 5. Two Week 5 issues are in the wrong order

**W5-03** generates tests “from approved ACs.” Approval does not exist until **W5-04**.

**Fix.** Build the review gate before generation, or let generation use drafts you have hand-approved.

### 6. The dataset plants traps the plan under-describes

These are measured in the CSVs and PDFs.

- Acceptance criterion types are often wrong relative to the text. Do not use `criterion_type` as ground truth. Prefer `status`.
- There are only about 19 distinct AC texts across 421 rows. A random sample of 30 will mostly be duplicates. Only about 11 ACs are truly vague (“fast and user friendly”).
- Every requirement title uses a “scenario N” template. AI extraction and ambiguity work will look easier here than on real requirements. Say so in the defense.
- Integrity (foreign keys) is clean. The planted problems are semantic. Example. Tests marked NEEDS_REVIEW still have ACTIVE links, so they can inflate coverage. The plan talks about “deprecated” tests, but that status does not appear.
- Release fields disagree across requirements, defects, and executions. “Ready for R26.10” needs a written rule about which release column you trust.
- Week 2 readiness targets R26.10. One golden readiness scenario asks for R26.11. Build both. They exercise different rules.
- PDFs almost never contain requirement IDs. Many `source_section` values point at headings that do not exist. Full PDF-to-CSV reconciliation will mostly report mismatches. That is still a useful learning exercise if you set expectations.
- Sets A, B, and C each drop whole layers of the chain (requirements, ACs, tests, defects, or run history). Adapters alone may not be enough. Expect some core model changes and record them (strengthen S14).

### 7. Small gaps that still matter

- Missing acceptance criteria on a requirement is never reported as its own gap (you report ACs without tests, and requirements without tests).
- Document classification exists (DOC-03 is CONFIDENTIAL). Nothing in the plan routes that away from a public model yet (S12).
- Prompt-injection tests are left to a late stretch issue. Cheap to add early in the eval set (S13).
- No waiver or risk-acceptance table exists, though readiness text and some golden scenarios mention waivers.
- “Tracing” appears in the Week 7 theme line, but no issue builds it.

---

## What to decide now

Do these before the Week 2 model and loader harden.

1. **Keep a thin extraction issue as required work.** Do not make required document extraction the first cut.
2. **Give every golden scenario an owning issue.** Fix the archived-doc scenario’s home. Cover both R26.10 and R26.11 for readiness.
3. **Define a hold-out set and a scoring method in the Week 3 eval ADR.** Include how you score free-text expected answers.
4. **Force the Week 3 labeling sample.** Include the vague ACs on purpose. Deduplicate templates. Keep labels separate from golden ambiguity rows when you can.
5. **Reorder Week 5** so approval exists before “generate from approved ACs.”
6. **Adjust the cut order.** Protect the Week 8 readiness view if you care about the recommended dashboard. Prefer a paper mapping of Sets B and C over deleting those defense answers entirely.
7. **In the Week 2 model ADR, decide.** Which release field wins. Whether `status` or `approval_status` is trusted. What “active test” means (status only, or also executed and passing). Whether entity layers can be optional for Sets A/B/C.

Decide later at the issue that owns them. S10 (coverage gaming), S11 (review batch size), S12 (classification), S13 (injection), and a clearer generated-test quality bar (S7).

---

## Learning opportunities worth taking

These are lessons the dataset is designed to teach. Harvest them on purpose.

1. **Don’t trust labels.** Wrong `criterion_type` values are a ready example for the Week 1 data profile and the Week 2 data-quality report.
2. **Effective sample size.** Count distinct AC texts, not row counts. Write about inflated eval sets in the journal.
3. **Version-aware retrieval.** DOC-98 vs current docs is a concrete case. Similarity alone must not win.
4. **Adapters under stress.** Sets A/B/C will likely force a core change. A written ADR that admits that teaches more than a silent “no core changes” claim.
5. **Statistical humility.** When a category has one golden scenario, run the model a few times in Week 6 and show how scores move. Cost and latency stay trustworthy. Quality rankings do not.

---

## How this review was done

Read-only poteto-mode Investigation. Explorers covered requirements coverage, week sequencing, evaluation design, and dataset reality. Findings were checked against the CSVs and plan files. No roadmap or issue text was edited in that pass.

If you accept the “decide now” list, fold the outcomes into [SUGGESTIONS.md](SUGGESTIONS.md) checkboxes and then into [ROADMAP.md](ROADMAP.md) / [ISSUES.md](ISSUES.md).

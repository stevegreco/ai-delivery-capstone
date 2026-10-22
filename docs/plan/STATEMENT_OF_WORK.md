# Statement of Work: AI Delivery Assurance Copilot

This SOW commits to delivering a working, evaluated AI delivery-assurance copilot over 8 weeks (Oct 19 to Dec 13, 2026), built from the weekly plan in [ROADMAP.md](ROADMAP.md).

## How to read this SOW

A statement of work is the agreement on *what* will be delivered, *when*, and *how we will know it is done*. Each section answers one question:

| Section | The question it answers |
| --- | --- |
| Background | Why does this work exist? |
| Objectives | What outcomes count as success? |
| Scope | What is included, and just as important, what is not? |
| Deliverables | What concrete things will be handed over? |
| Schedule | When does each piece land? |
| Approach | How will the work be done, and under what rules? |
| Assumptions, constraints, risks | What must hold true, and what could go wrong? |
| Acceptance | Who signs off, and against what criteria? |

In a client engagement, Scope and Acceptance are where most disputes start, so they are the sections worth the most care.

## Background

Delivery teams lose business intent between requirements, implementation and testing, and often cannot answer: "Are we ready to release, and what evidence supports that?" Capstone 4 asks for a governed AI copilot that keeps the Requirement → Acceptance Criterion → Test → Result chain intact and explains release readiness with evidence.

This is a learning project for Steve's cohort. The goal is to understand every part well enough to explain and defend it, so understanding takes priority over speed. Sources: `PROJECT_BRIEF.md`, `Capstone4_usecase_definition.md` and the supplied dataset.

## Objectives and success criteria

The project succeeds when the copilot answers the golden scenarios with cited evidence, and Steve can explain every design decision behind it.

| Objective | Measured by |
| --- | --- |
| Answer coverage and readiness questions without AI | Deterministic gap report and readiness decision for release R26.10, every reason traceable to row IDs |
| Ground every AI output in sources | Each statement cites a document, section or row ID, or is blocked as unsupported |
| Measure quality from the first AI feature | Golden-scenario scorecard with a Week 3 baseline and a Week 8 rerun |
| Keep humans in control | No generated AC or test becomes `ACTIVE` without an approval record |
| Know the cost of every call | Model, tokens, latency and cost logged per call; at least two models compared |
| Generalize beyond the reference data | Set A (Jira) runs through adapters and config without editing core logic |
| Understand it all | ADRs for each major choice, a weekly journal, and a final walkthrough |

## Scope

**In scope**

- A normalized delivery model with provenance and origin (`HUMAN`, `AI_SUGGESTED`, `AI_APPROVED`) on every artifact and link
- Loading and validating the 11 reference CSVs
- Deterministic traceability queries, coverage gap reports and readiness rules
- An LLM client with TokenOps logging, and an acceptance-criteria quality classifier
- A golden-scenario evaluation harness with saved baselines
- Ingestion of the 8 PDFs, chunking with metadata, hybrid and version-aware retrieval
- Grounded generation of ACs and test cases with citations and unsupported-claim checks
- A human review gate and conflict detection across current documents
- Change impact and stale-test detection, plus an LLM explanation of the readiness decision
- Comparison of at least two models, caching and context minimization
- Onboarding Set A (Jira) through an adapter
- A minimal coverage and readiness view with drill-down to evidence

**Stretch (first to cut, in this order)**

1. Sets B (Kanban) and C (Mobile Banking)
2. Traceability graph view
3. Agentic test execution with approval gates
4. Reduce Set A to coverage only

Requirement extraction from PDFs (W4-05) is also stretch, cut as soon as Week 4 runs long.

**Out of scope**

- Production deployment, authentication or multi-user hosting
- Real Jira or Azure DevOps integration
- Editing or regenerating the source dataset, which stays read-only
- Any LLM making the readiness decision; rules decide and the LLM only explains

## Deliverables

Each deliverable maps to an issue in [ISSUES.md](ISSUES.md) and lands through its own branch and PR.

| Week | Deliverable | Issues |
| --- | --- | --- |
| 1 | Glossary and concept diagram, data profile, manual baseline for 5 golden scenarios, stack ADR | W1-01 to W1-04 |
| 2 | Delivery model ADR, one-command CSV loader with data-quality report, traceability and coverage gap report, readiness rules v0 | W2-01 to W2-04 |
| 3 | LLM wrapper with TokenOps log, 30 hand-labeled ACs, AC quality classifier, evaluation runner with baseline scorecard | W3-01 to W3-04 |
| 4 | Structured PDF extraction, chunking ADR, hybrid search with recall@k table, version-aware retrieval | W4-01 to W4-04 (W4-05 stretch) |
| 5 | Citation and unsupported-claim checks, generated ACs and test cases, review queue, conflict report | W5-01 to W5-05 |
| 6 | Change impact and stale-test lists, cited readiness summary, model comparison ADR | W6-01 to W6-03 |
| 7 | Before/after TokenOps table, adapter contract and Set A onboarding | W7-01, W7-02 (W7-03 stretch) |
| 8 | Coverage and readiness view, final evaluation vs baseline, retrospective and walkthrough | W8-01, W8-02 (W8-03, W8-04 stretch) |

Every week also produces a journal entry in `docs/journal/week-NN.md`.

## Schedule and milestones

Each week is one milestone. The checkpoints at the end of Weeks 2 and 4 are where stretch work gets cut, early rather than late, and Week 6 runs light because of Thanksgiving.

| Week | Dates | Theme | Milestone |
| --- | --- | --- | --- |
| 1 | Oct 19 – Oct 25 | Orientation and domain | |
| 2 | Oct 26 – Nov 1 | Delivery model and deterministic core | Checkpoint, Nov 1: cut stretch early? |
| 3 | Nov 2 – Nov 8 | First LLM calls and evaluation harness | |
| 4 | Nov 9 – Nov 15 | Document ingestion and retrieval | Checkpoint, Nov 15: cut stretch early? |
| 5 | Nov 16 – Nov 22 | Grounded generation and human review | |
| 6 | Nov 23 – Nov 29 | Change impact, readiness and model comparison | US Thanksgiving, Nov 26 |
| 7 | Nov 30 – Dec 6 | TokenOps and generalization | |
| 8 | Dec 7 – Dec 13 | Reviewer experience and defense | Final defense, Dec 13 |

## Approach and working agreements

The build order is deliberate: domain first, then the deterministic core, then AI with evaluation from day one, then generalization.

- **Rules before AI.** Anything a query can answer (traceability, coverage, readiness) stays deterministic. The LLM extracts, generates and explains, but never decides readiness.
- **Measure from the start.** The evaluation harness arrives with the first LLM feature, so every later change is compared to a baseline.
- **Cite or block.** Every AI output cites document, section or row IDs, or is marked unsupported.
- **Human gates.** Generated ACs and tests stay `DRAFT` until approved, with reviewer, time and diff recorded.
- **Decisions are written down.** Design choices go in ADRs (`docs/adr/NNNN-title.md`), written by Steve.
- **Weekly rhythm.** Start: read the week's issues and pick what to cut. During: one issue per branch and PR. End: journal entry and baseline update.
- **Teaching mode.** Steve writes the code by default; the assistant explains, hints and reviews.

## Assumptions, constraints and risks

**Assumptions**

- 8 to 10 focused hours a week are available.
- The supplied dataset and golden scenarios are the source of truth for evaluation.
- Access to at least two LLMs is available for the model comparison.

**Constraints**

- The dataset folder is read-only.
- API keys live in `.env`, never in the repo.
- No paid LLM call runs in a loop or at batch scale without a cost estimate first.
- No new dependency, framework or service without an explanation and a yes.

**Risks**

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| Eight weeks is tight; most weeks combine two themes | High | Cut stretch work in the stated order; check progress at the end of Weeks 2 and 4 |
| Week 6 includes US Thanksgiving (Nov 26) | High | Plan a lighter Week 6 or pull work forward |
| PDF parsing loses tables or the Doc 05 diagram | Medium | Note failures; transcribe the diagram manually if needed |
| The LLM softens or contradicts a BLOCKED decision | Medium | Rules own the decision; check the summary against it |
| LLM costs grow during evaluation runs | Medium | TokenOps logging from the first call; caching in Week 7 |
| The Week 2 model does not fit Set A | Medium | Record core changes in an ADR; treat it as a learning outcome |

## Acceptance and sign-off

Each issue is accepted when its "Done when" criteria in [ISSUES.md](ISSUES.md) are met and its PR is merged. The project as a whole is accepted when:

- [ ] The end-to-end scenario (§26 of the use-case definition) can be demoed
- [ ] The final evaluation is rerun and compared with the Week 3 baseline
- [ ] Every AI output in the demo cites its sources or is marked unsupported
- [ ] Every major design choice has an ADR Steve can explain and defend
- [ ] The §1P questions ("What the team should be able to explain") have prepared answers

**Checkpoints:** scope review at the end of Week 2 (Nov 1, 2026) and Week 4 (Nov 15, 2026); final defense by Dec 13, 2026.

**Sign-off:** Steve, as project owner.

Open question: does the cohort have a reviewer or instructor who should also sign off, and on what date is the defense?

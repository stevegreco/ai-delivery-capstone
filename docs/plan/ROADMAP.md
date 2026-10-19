# Roadmap: 12 weeks

Each week maps to a GitHub **milestone**, and each week's issues are in [ISSUES.md](ISSUES.md).

The order is deliberate:
1. Understand the domain before writing code.
2. Build the deterministic core (data, traceability, readiness rules) before adding AI.
3. Set up evaluation *before* the AI features get complex, so every later change can be measured.
4. Generalize to Sets A/B/C only after the reference project works.

| Week | Theme | You'll be able to explain… |
|---|---|---|
| 1 | Orientation & domain | What "delivery assurance" means, and how requirements, ACs, tests, runs and defects relate |
| 2 | Delivery model & structured ingestion | Why a normalized internal model matters, and how to load and validate relational data |
| 3 | Deterministic traceability & readiness | Coverage gaps, orphans and readiness rules, all with **no AI** |
| 4 | First LLM calls: structured outputs | Prompting for JSON against a schema, validation, and logging tokens, latency and cost |
| 5 | Evaluation harness | Golden sets, metrics, and why you measure before optimizing |
| 6 | Document ingestion | Parsing PDFs (text, tables, a diagram), chunking, and metadata |
| 7 | Retrieval (RAG) | Embeddings, hybrid search, version-aware filtering, and retrieval metrics |
| 8 | Grounded generation & human review | Generating ACs and tests with citations, blocking unsupported claims, and review gates |
| 9 | Change impact & release readiness | Stale tests, impact propagation, and evidence-based go/no-go explanations |
| 10 | Multi-model comparison & TokenOps | Quality/cost/latency trade-offs, caching, and context minimization |
| 11 | Generalization: Sets A, B, C | Adapters and mapping config rather than project-specific logic |
| 12 | Reviewer experience & defense | A dashboard, traceability views and an optional agent loop, plus your final story |

## Week by week

### Week 1: Orientation & domain
Read the spec closely, explore the data by hand, and work through a few golden scenarios **yourself**. Your manual answers are the first baseline every later version is compared to. Choose your stack and write your first ADR.

### Week 2: Delivery model & structured ingestion
Design the common internal model (Requirement, AC, Test, Execution, Defect, Change, Document, Release). Load the reference CSVs into it and write data-quality checks. Keep it boring and correct.

### Week 3: Deterministic traceability & readiness
Answer the hard questions with plain queries: which P0/P1 requirements have no active test, which tests are orphaned, which requirements have failing runs or open defects. Write v0 readiness rules. This is the part an LLM must *not* replace.

### Week 4: First LLM calls
Wrap an LLM client that logs model, tokens, latency and cost from the first call onward. Build an ambiguity/testability classifier for ACs that returns validated structured output, then compare it against labels you write by hand.

### Week 5: Evaluation harness
Turn the 30 golden scenarios into a repeatable evaluation run. Define metrics per category, score your Week 3 rules and Week 4 classifier, and record the baseline.

### Week 6: Document ingestion
Parse the 8 PDFs, including tables and the workflow diagram in Doc 05. Experiment with chunking. Attach document ID, section, version and status metadata to every chunk.

### Week 7: Retrieval (RAG)
Embed and index the chunks. Compare keyword, vector and hybrid search. Make retrieval version-aware so archived Doc 98 never wins over current guidance. Measure retrieval quality against the golden scenarios.

### Week 8: Grounded generation & human review
Generate candidate ACs and test cases (positive, negative, boundary, exception, API) grounded in retrieved context, with citations. Add an unsupported-claim check and a review queue where nothing is published until you approve it.

### Week 9: Change impact & release readiness
Use requirement changes to find impacted ACs, tests and evidence, and flag stale tests. Combine deterministic readiness rules with an LLM *explanation* layer, so the decision comes from rules and the LLM only explains it.

### Week 10: Multi-model comparison & TokenOps
Run the evaluation harness against two or more models. Compare quality, cost and latency. Add prompt/context caching and context minimization, and measure the savings.

### Week 11: Generalization
Onboard Sets A, B and C through adapters and mapping config only. Any change to core logic is a design smell, so record it in an ADR.

### Week 12: Reviewer experience & defense
Build a small coverage/readiness dashboard and a traceability view. Optionally, add an agent that runs approved tests through the mock test runner with approval gates. Prepare the final walkthrough.

## Each week
- Start: read that week's issues and decide the order.
- During: one issue per branch and PR, even working solo. The PR description is a learning artifact.
- End: write `docs/journal/week-NN.md` and update the evaluation baseline if something changed.

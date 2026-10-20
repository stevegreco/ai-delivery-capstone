# Roadmap: 8 weeks (Oct 19 – Dec 13, 2026)

Weeks run Monday to Sunday. Week 6 includes US Thanksgiving (Nov 26).

Each week maps to a GitHub **milestone**, and each week's issues are in [ISSUES.md](ISSUES.md).

The order is deliberate:
1. Understand the domain before writing code.
2. Build the deterministic core (data, traceability, readiness rules) before adding AI.
3. Set up evaluation *at the same time as* the first AI feature, so every later change can be measured.
4. Generalize to Sets A/B/C only after the reference project works.

Eight weeks is tight, so most weeks combine two themes. The plan assumes **8–10 focused hours a week**. Issues labeled `stretch` are the first to cut if you fall behind. Cut them without guilt: understanding the core matters more than finishing everything.

**Cut order**, if you fall behind:
1. W7-03 Sets B and C
2. W8-03 Traceability graph view
3. W8-04 Agentic test execution
4. Reduce W7-02 (Set A) to coverage only

W4-05 (requirement extraction) is stretch too, but cut it as soon as Week 4 runs long. Check progress at the end of Weeks 2 and 4, and cut early rather than late.

| Week | Dates | Theme | You'll be able to explain… |
|---|---|---|---|
| 1 | Oct 19 – Oct 25 | Orientation & domain | What "delivery assurance" means, and how requirements, ACs, tests, runs and defects relate |
| 2 | Oct 26 – Nov 1 | Delivery model & deterministic core | The normalized model, loading and validation, plus coverage gaps and readiness rules with **no AI** |
| 3 | Nov 2 – Nov 8 | First LLM calls & evaluation harness | Structured outputs, TokenOps logging, golden sets and metrics |
| 4 | Nov 9 – Nov 15 | Document ingestion & retrieval | PDF parsing, chunking, metadata, hybrid search and version-aware retrieval |
| 5 | Nov 16 – Nov 22 | Grounded generation & human review | Generating ACs and tests with citations, blocking unsupported claims, and review gates |
| 6 | Nov 23 – Nov 29 | Change impact, readiness & model comparison | Stale tests, impact propagation, evidence-based go/no-go, and quality/cost/latency trade-offs |
| 7 | Nov 30 – Dec 6 | TokenOps & generalization | Caching, context minimization, tracing, and onboarding Sets A/B/C through adapters |
| 8 | Dec 7 – Dec 13 | Reviewer experience & defense | A readiness view that shows its evidence, plus your final story |

## Week by week

### Week 1 (Oct 19 – Oct 25): Orientation & domain
Read the spec closely, explore the data by hand, and work through 5 golden scenarios **yourself**. Your manual answers are the first baseline every later version is compared to. Choose your stack and write your first ADR.

### Week 2 (Oct 26 – Nov 1): Delivery model & deterministic core
Design the common internal model. Load and validate the reference CSVs. Then answer the hard questions with plain queries: which P0/P1 requirements have no active test, which tests are orphaned, and whether the release is blocked. This is the part an LLM must *not* replace.

### Week 3 (Nov 2 – Nov 8): First LLM calls & evaluation harness
Wrap an LLM client that logs model, tokens, latency and cost from the first call onward. Build an AC ambiguity classifier with validated structured output, and compare it against labels you write by hand. Turn the golden scenarios into a repeatable evaluation run and record the baseline.

### Week 4 (Nov 9 – Nov 15): Document ingestion & retrieval
Parse the 8 PDFs, including tables and the Doc 05 diagram. Chunk them with full metadata. Compare keyword, vector and hybrid search, and make retrieval version-aware so archived Doc 98 never wins over current guidance. Stretch: extract requirements from the PDFs and reconcile them with the CSV.

### Week 5 (Nov 16 – Nov 22): Grounded generation & human review
Generate candidate ACs and test cases grounded in retrieved context, with citations. Add an unsupported-claim check and a review queue where nothing is published until you approve it. Detect conflicts between current documents.

### Week 6 (Nov 23 – Nov 29): Change impact, readiness & model comparison
Trace requirement changes to the ACs, tests and evidence they affect, and flag stale tests. The rules make the readiness decision and the LLM explains it. Run the evaluation against two or more models.

### Week 7 (Nov 30 – Dec 6): TokenOps & generalization
Add caching and context minimization, and measure the savings. Onboard Set A through adapters and mapping config only. Sets B and C are stretch goals.

### Week 8 (Dec 7 – Dec 13): Reviewer experience & defense
Build a minimal coverage/readiness view where a reviewer can drill down from any decision to the evidence behind it. Rerun the full evaluation, compare it with the Week 3 baseline, and prepare the final walkthrough.

## Each week
- Start: read that week's issues, decide the order, and pick what to cut if time runs short.
- During: one issue per branch and PR, even working solo. The PR description is a learning artifact.
- End: write `docs/journal/week-NN.md` and update the evaluation baseline if something changed.

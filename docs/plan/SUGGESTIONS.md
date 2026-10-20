# Suggestions

Concerns about the requirements, gaps in the plan, and design changes worth considering. **None of these are applied to [ROADMAP.md](ROADMAP.md) or [ISSUES.md](ISSUES.md) yet.** Tick a box once you've decided on it, and add the outcome.

Each item lists the issues it touches.

---

## Problems in the requirements and data

### S1 · The golden set is too small to rank models
- [ ] Decided
- **Problem:** There are 30 scenarios, and most categories have just 1–2. Per-category scores are noise, two models won't separate meaningfully on 30 items, and tuning prompts on the same 30 overfits to them.
- **Suggestion:** Treat the golden set as smoke tests. Build larger labeled sets for each task (like the 30 ACs in W3-02), hold some items back for the final evaluation, and run LLM evaluations several times to see how much results vary.
- **Affects:** W3-02, W3-04, W6-03

### S2 · The data is synthetic and possibly mislabeled
- [ ] Decided
- **Problem:** Requirements are templated ("…scenario 1", "…scenario 2"). The first two AC rows look mislabeled: AC-0001 is a happy path typed `ERROR_HANDLING`, and AC-0002 describes a transient error typed `PERFORMANCE`.
- **Suggestion:** Don't treat the given labels as ground truth. Measure the label noise in W1-02. Expect AI tasks to be easier here than on real requirements, and say so in the defense.
- **Affects:** W1-02, W3-02

### S3 · "Block unsupported claims" can't be fully met
- [ ] Decided
- **Problem:** Automated claim checking catches many problems but not all.
- **Suggestion:** Frame it as "flag, show the evidence and let a human decide." Measure how often it misses or wrongly flags a claim, rather than calling it a guarantee.
- **Affects:** W5-01

### S4 · There's no definition of a good generated test
- [ ] Decided
- **Problem:** Coverage only shows a test exists. The spec gives no quality bar for generated tests, and there's just one TEST_GENERATION golden scenario.
- **Suggestion:** See S7.
- **Affects:** W5-03

---

## Gaps in the plan

### S5 · Add requirement extraction from documents
- [x] Decided: added as **W4-05** (stretch).
- **Problem:** Requirements Intelligence #1–2 asks you to extract requirements, actors, rules and dependencies from the documents. The plan currently relies on `requirements.csv`.
- **Suggestion:** Add an issue (Week 4, after PDF extraction) that extracts requirements from the PDFs and checks them against the CSV: what's in the documents but missing from the CSV, and where they disagree.
- **Affects:** new issue, Week 4

### S6 · Add conflict detection between documents
- [x] Decided: added as **W5-05** (required).
- **Problem:** W4-04 handles current vs archived only. Current documents can also contradict each other, for example an NFR limit in Doc 06 vs a functional spec.
- **Suggestion:** Add an explicit conflict-detection issue that outputs the conflicting statements with citations to both.
- **Affects:** new issue, Week 4–5

### S7 · Strengthen the W5-03 exit test
- [ ] Decided
- **Problem:** "Scenario passes" doesn't measure whether the generated tests are any good.
- **Suggestion:** Score tests against a rubric (traceable to an AC, has an exact expected result, boundary values come from the spec), or seed a spec violation and check whether the generated tests catch it.
- **Affects:** W5-03

### S8 · Protect the 8-week schedule
- [x] Decided: 8–10 hours a week. Cut order is W7-03 → W8-03 → W8-04 → Set A coverage only, now in ROADMAP.md.
- **Problem:** Eight weeks leaves no buffer. Weeks 2, 3 and 4 each pack two themes, and a slip in Week 4 (PDF parsing and retrieval) pushes everything after it.
- **Suggestion:** Decide your cut line now: W7-03, W8-03 and W8-04 go first, then reduce Set A to coverage only. Check progress at the end of Weeks 2 and 4 and cut early rather than late. Size this against the hours you actually have each week.
- **Affects:** ROADMAP.md

---

## System design changes

### S9 · Record where every link and artifact came from
- [x] Decided: folded into **W2-01** (origin fields on every artifact and link).
- **Suggestion:** Every link and artifact gets an `origin` (written by a human / suggested by AI / AI-generated and approved) plus who, when, the model and the prompt version. Without it, AI output gets mixed into the traceability graph and you can't audit it later.
- **Affects:** W2-01, W5-01, W5-04

### S10 · Don't let coverage be gamed
- [ ] Decided
- **Problem:** An AI that generates tests pushes coverage up whether or not the tests are good.
- **Suggestion:** Count only tests that are approved, active and executed. Report "has a test" separately from "has passing evidence."
- **Affects:** W2-03, W5-03, W8-01

### S11 · Design against rubber-stamping
- [ ] Decided
- **Problem:** A reviewer facing 200 generated tests stops reading them.
- **Suggestion:** Cap batch sizes, show the evidence next to each item, and track approval and edit rates. A 100% approval rate is a warning sign.
- **Affects:** W5-04

### S12 · Respect data classification
- [ ] Decided
- **Suggestion:** `document_registry.csv` has a `classification` column. Decide which classifications can go to which model provider, and enforce that in the LLM wrapper.
- **Affects:** W3-01, W6-03

### S13 · Treat source text as untrusted
- [ ] Decided
- **Problem:** Requirements, tickets and PDFs can contain text that tells the LLM what to do (prompt injection).
- **Suggestion:** Keep source data separate from instructions in prompts from W3 onward. Add one or two injection test cases to the evaluation instead of leaving AI safety to Week 8.
- **Affects:** W3-03, W3-04, W5-01, W8-04

### S14 · Expect generalization to force some core changes
- [ ] Decided
- **Problem:** Some sets may have no explicit traceability links, so links would have to be inferred, which is AI work with confidence scores.
- **Suggestion:** Check each set's linking fields early in Week 7. Record every core change in a decision record instead of avoiding it.
- **Affects:** W7-02, W7-03

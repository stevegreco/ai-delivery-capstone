---
name: plan-learning-project
description: Turn a project brief or use-case document into a learning plan — a statement of work, a week-by-week roadmap and an issue backlog — for a project whose goal is to understand the work well enough to explain and defend it, not just to ship it. Use when the user starts a new learning project, capstone, course project or self-study build and asks for a plan, roadmap, backlog, SOW or "how should I approach this over N weeks".
---

# Plan a learning project

A learning plan differs from a delivery plan in one way: every week ends with something the learner can *explain*, not only something that runs. Optimize for understanding. When speed and understanding conflict, choose understanding.

## 1. Gather inputs before writing anything

Ask for whatever is missing. Do not guess these:

- **The brief:** the problem statement, requirements and any supplied data or documents. Read all of it.
- **Time box:** start and end dates, and focused hours per week. Size the plan against the hours, not the calendar.
- **Starting point:** what the learner already knows, and what they most want to learn.
- **Fixed constraints:** read-only data, required stack, reviewers, a defense or demo date.

Also flag holidays or known busy weeks inside the date range.

## 2. Order the work deliberately

Use this order unless the brief forces another, and say why in the roadmap:

1. **Domain first.** Vocabulary, a hand exploration of the data, and solving a few target tasks *manually*. The manual answers become the first baseline.
2. **Deterministic core next.** Anything a query or rule can answer gets built without AI. That code is the reference the AI is later checked against.
3. **Evaluation with the first AI feature.** Build the measurement harness in the same week as the first model call, so every later change has a baseline.
4. **Generalize last.** Extend to new data sets or sources only after the reference case works.

## 3. Write the outputs

Produce these in order. Each has a template in `references/`. Read the template when you reach that step.

| Output | Default path | Template |
|---|---|---|
| Roadmap | `docs/plan/ROADMAP.md` | [roadmap-template.md](references/roadmap-template.md) |
| Issue backlog | `docs/plan/ISSUES.md` | [issue-template.md](references/issue-template.md) |
| Statement of work | `docs/sow.md` | [sow-template.md](references/sow-template.md) |

Write the roadmap and backlog first, and the SOW last, because the SOW summarizes and commits to them. Show the roadmap to the user and get agreement before writing the backlog.

## 4. Protect the schedule

- Most short plans pack two themes into a week. Say so plainly.
- Label optional work `stretch`, and write an explicit **cut order** (what goes first, second and so on).
- Put **checkpoints** at roughly one third and halfway through, where stretch work gets cut early rather than late.
- Every issue fits inside one week at the stated hours. Split it if it doesn't.

## 5. Stay in scope

- Write plans, not code. Do not scaffold folders, add dependencies or create files that belong to an issue.
- Do not create GitHub issues, milestones or labels without explicit approval. The backlog is a draft in Markdown first.
- Design choices (stack, data model, metrics, thresholds) belong to the learner. Turn each one into a `decide` issue that produces an ADR, rather than deciding it in the plan.

## 6. Hand off

When the plan is agreed, suggest the next steps:

- Run a critique pass over the requirements and plan (problems in the brief, gaps in the plan, design changes), with each item marked undecided until the learner decides it.
- Set up the learning journal (`docs/journal/week-NN.md`: what I learned, what confused me, open questions).

# Statement of work template

Write the SOW last. It commits to what the roadmap and backlog already say, so every row should point back to them.

```markdown
# Statement of Work: <project name>

<date> · <owner>

This SOW commits to delivering <one-line outcome> over <N> weeks (<start> to <end>), built from the weekly plan in `docs/plan/ROADMAP.md`.

## How to read this SOW

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

## Background
<The problem, and that this is a learning project where understanding comes before speed. Name the source documents.>

## Objectives and success criteria
<One sentence on what success means.>

| Objective | Measured by |
| --- | --- |
| <outcome> | <evidence someone else could check> |

## Scope
**In scope**
- <capability>

**Cut order, if behind**
1. <same order as the roadmap>

**Out of scope**
- <explicit exclusions, including anything the AI must never decide>

## Deliverables
| Week | Deliverable | Issues |
| --- | --- | --- |
| 1 | <artifacts> | W1-01 to W1-0N |

Every week also produces a journal entry in `docs/journal/week-NN.md`.

## Schedule and milestones
<Each week is one milestone. Name the checkpoint weeks and what happens at them.>

## Approach and working agreements
- <the build order and why>
- <rules such as "rules before AI", "cite or block", "human gates", "decisions in ADRs", "teaching mode">

## Assumptions, constraints and risks
**Assumptions**
- <hours per week, data, access to models>

**Constraints**
- <read-only data, secrets handling, cost limits, dependency approvals>

**Risks**
| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| <risk> | <High/Medium/Low> | <action> |

## Acceptance and sign-off
Each issue is accepted when its "Done when" criteria are met and its PR is merged. The project as a whole is accepted when:
- [ ] <demo, evaluation rerun, explanation criteria>

**Checkpoints:** <dates>. **Sign-off:** <who>.
```

## Guidance

- Scope and Acceptance are where disputes start. Spend the most care there.
- The "How to read this SOW" table is there for learners who haven't written one before. Drop it for experienced readers.
- End with any open questions (other reviewers, defense date) rather than guessing.

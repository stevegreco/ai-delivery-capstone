# Roadmap template

Fill in every `<…>`. Keep the week table to one line per week.

```markdown
# Roadmap: <N> weeks (<start> – <end>)

Weeks run <Monday to Sunday>. <Note holidays or busy weeks.>

Each week maps to a milestone, and each week's issues are in [ISSUES.md](ISSUES.md).

The order is deliberate:
1. <Domain first, and why>
2. <Deterministic core before AI, and why>
3. <Evaluation alongside the first AI feature, and why>
4. <Generalization last, and why>

The plan assumes **<H> focused hours a week**. Issues labeled `stretch` are the first to cut.

**Cut order**, if you fall behind:
1. <issue ID and name>
2. <…>

Check progress at the end of Weeks <X> and <Y>, and cut early rather than late.

| Week | Dates | Theme | You'll be able to explain… |
|---|---|---|---|
| 1 | <dates> | <theme> | <the concepts the learner can explain by the end of the week> |

## Week by week

### Week 1 (<dates>): <theme>
<2–4 sentences: what happens this week and why it comes at this point.>

## Each week
- Start: read that week's issues, decide the order, and pick what to cut if time runs short.
- During: one issue per branch and PR. The PR description is a learning artifact.
- End: write `docs/journal/week-NN.md` and update the evaluation baseline if something changed.
```

## Guidance

- The **"You'll be able to explain…"** column is the most important one. Write it as concepts, not tasks ("why retrieval must be version-aware", not "build retrieval").
- A theme with two parts ("Ingestion & retrieval") is a signal the week is full. Don't add a third.
- If the time box is short, write a separate suggestions or critique file instead of adding caveats to the roadmap.

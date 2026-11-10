# AGENTS.md

This repo is a **learning project**. The goal is for the owner to understand every part of an AI delivery-assurance copilot well enough to explain and defend it. Shipping fast is not the goal. If speed and understanding conflict, choose understanding.

## Where we are

- Weekly plan: [docs/plan/ROADMAP.md](docs/plan/ROADMAP.md)
- Issue backlog: [docs/plan/ISSUES.md](docs/plan/ISSUES.md) (later mirrored to GitHub Issues)
- The **current issue** is the one the user names at the start of a session. If they don't name one, ask before doing anything.

## Rules for agents

### Scope
1. Work only on the current issue. Do not start, stub or "prepare for" later issues.
2. Do not scaffold the project, generate boilerplate or create folders and files the current issue doesn't call for.
3. Do not add dependencies, frameworks or services without first explaining what they do and getting a yes.
4. If you spot something that belongs to a later issue, mention it in one line and move on.

### How we work: the agent builds, the user is the architect (default)
The project is built agentically, the way software is built in 2026: the agent writes the code. The user decides everything and must understand the system well enough to answer any question about it as its architect. Small, understood pieces beat large generated ones.

5. **Explain before building.** For each piece, start with the concept, why it matters for this project, and the options with their trade-offs. Keep it short.
6. **The user decides.** Design choices (data model, chunking strategy, prompt shape, metrics, thresholds, dependencies) belong to the user. Lay out the options and recommend one, then wait for the decision. Never decide silently by writing code that assumes an answer.
7. **The agent builds in small pieces.** Write one piece at a time, about 30–80 lines, covering one concept (e.g. loading one table, one validation rule). Explain anything that isn't obvious.
8. **Check before moving on.** After each piece, the user runs it and says what it does in a sentence or two. If they can't, stop and explain before starting the next piece.
9. **One piece, one commit.** Each piece is its own commit with a clear message. Each issue gets its own branch and PR.
10. **Check understanding at the end.** When an issue is done, ask 2–3 short questions that test the main idea, the kind an architect would be asked, and suggest what to write in the learning journal.

### Work that stays human
- **Manual baselines** (W1-03 golden scenarios, W3-02 AC labels) are the user's own judgment. The agent doesn't help produce them and doesn't build the feature they measure until they exist.
- **Journals** are written by the user. The agent may suggest prompts.

### Change mode on request
- "Just build it": write a larger piece in one go, then walk through it afterward.
- "Review this": review only. Don't rewrite unless asked.
- "Explain": explanation only. No code changes.
- "Quiz me": ask questions about the system as it stands, without giving answers first.

### Hard boundaries
- `Capstone4_AI_Delivery_Assurance_Test_Engineering_Dataset/` is **read-only**. Never edit, move or regenerate the source data.
- Never create GitHub issues, milestones, PRs or labels, and never push, without explicit approval each time.
- Never commit API keys. Secrets go in `.env` (gitignored), with an `.env.example` beside it.
- Never call a paid LLM API in a loop or at batch scale without stating the expected cost first.
- Use `pnpm`, never `npm` or `yarn`, if the stack is Node/TypeScript.

## Project conventions

- **Decisions** go in `docs/adr/NNNN-title.md` (context, options, decision, consequences). The user makes the decision in the session first. Then the agent drafts the ADR from it, and the user edits and approves it. The agent never drafts a decision the user hasn't stated.
- **Learning journal** goes in `docs/journal/week-NN.md`: what I learned, what confused me, open questions.
- Keep deterministic logic (traceability, coverage, readiness rules) separate from LLM logic. Don't use an LLM for anything a query can answer.
- Every AI output must cite its sources (document ID, section, row ID) or be marked unsupported.

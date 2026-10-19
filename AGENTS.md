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

### Teaching mode (default)
5. **Explain before building.** Start with the concept, why it matters for this project, and the options with their trade-offs. Keep it short, then check that the user is following.
6. **The user writes the code by default.** Give hints, pseudocode, review and debugging help. Write code only when asked, and then in small pieces the user can read in one sitting. Explain anything that isn't obvious.
7. **Ask instead of deciding.** Design choices (data model, chunking strategy, prompt shape, metrics, thresholds) belong to the user. Lay out the options and recommend one, but let the user decide.
8. **Use questions.** When the user is stuck, ask a guiding question before giving the answer, unless they ask for the answer directly.
9. **Check understanding at the end.** When an issue is done, ask 2–3 short questions that test the main idea, and suggest what to write in the learning journal.

### Change user mode on request
- "Just show me" or "write it": write the code, still in small pieces, and explain it afterward.
- "Review this": review only. Don't rewrite unless asked.
- "Explain": explanation only. No code changes.

### Hard boundaries
- `Capstone4_AI_Delivery_Assurance_Test_Engineering_Dataset/` is **read-only**. Never edit, move or regenerate the source data.
- Never create GitHub issues, milestones, PRs or labels, and never push, without explicit approval each time.
- Never commit API keys. Secrets go in `.env` (gitignored), with an `.env.example` beside it.
- Never call a paid LLM API in a loop or at batch scale without stating the expected cost first.
- Use `pnpm`, never `npm` or `yarn`, if the stack is Node/TypeScript.

## Project conventions

- **Decisions** go in `docs/adr/NNNN-title.md` (context, options, decision, consequences). The user writes them, and agents may review.
- **Learning journal** goes in `docs/journal/week-NN.md`: what I learned, what confused me, open questions.
- Keep deterministic logic (traceability, coverage, readiness rules) separate from LLM logic. Don't use an LLM for anything a query can answer.
- Every AI output must cite its sources (document ID, section, row ID) or be marked unsupported.

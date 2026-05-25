# PROBSOLVE — A working-state template for problem solving

A markdown layout for capturing the *current* state of solving a non-trivial problem: what you're trying to achieve, what you've learned, what you don't yet know, what you'd test next, and what you've rejected. Distinct from a project plan or a writeup — this is **working notes**, refactored as understanding deepens.

## When to use

- The problem spans multiple sessions and you need durable state to pick it up cold.
- You'll run experiments and accumulate knowledge over time.
- You'll consider alternatives and need to remember why you rejected the ones you didn't pick.
- You've ever lost track of "what was that thing I tried two weeks ago and what did it tell us?"

**When not to use**: one-shot tasks with a clear answer (just do them); pure documentation (use a README); ticket/sprint tracking (use a tracker); incident response (use a runbook).

## The sections, in order

Each section header is followed by a one-line blockquote (`> ...`) restating the section's purpose. This is template scaffolding that stays in the filled-in doc — it tells the reader what belongs there, and tells future-you what to write when adding new entries.

1. **Goals** — 2–5 bullets describing what success looks like. Each one written so "done or not done" is unambiguous.
2. **Constraints** — non-negotiable limits on the solution space. Things you've decided you won't compromise on. (Examples: platform, latency budget, no external services, reproducibility requirements.)
3. **Established Findings** (`EF`) — durable findings; claims you'd carry to a similar problem. Two categories live here: (a) **lessons** earned from experiments — each cites the experiment(s) that established it; (b) **characterizations** of what you built — verifiable from the artifacts themselves, not from a hypothesis test. No floating claims of either kind.
4. **Working Hypotheses** (`H`) — claims you believe based on the work but haven't formally tested. Each one: states the belief, names the evidence base (what you observed), and notes how it would be **falsified** by a specific outcome. Hypotheses are promoted to Established Findings when confirmed, demoted to nothing when refuted. Use this section for generalizations and meta-claims that emerge from your experiments but go beyond any single one.
5. **Decisions Made** — consequential choices, both rejections and acceptances. Each entry: **what** was decided, **why** (referencing Established Findings or Experiment log rather than re-paraphrasing them), and a **"revisit if"** trigger when one exists. The expected overlap with Established Findings — beliefs shape decisions — is handled by *referencing* the belief (`per EF §3`), not restating its content.
6. **Open Questions** (`Q`) — unverified predictions and unknowns. Each one **names the experiment that would resolve it**, or is explicitly marked "not actionable" with the reason.
7. **Next Experiments** (`NX`) — concrete actions, ordered by expected impact. Each one **either resolves an open question (cross-referenced) or is tool/coverage work** with no associated hypothesis.
8. **Experiment Log** — historical record, append-only. Only entries that **asked a question and produced new knowledge**. Construction milestones and shipping decisions live elsewhere (READMEs, git log, tickets).

Optional sections, only if the problem demands them:

- **Stakeholders** — who the goals serve and whose input shapes the constraints. Useful when the problem is partly social.
- **Budget / timeline** — when cost or deadlines are first-class constraints, not just preferences.

### Cross-reference conventions

Short ID prefixes keep references compact: `EF §3` = third Established Finding; `H2` = second hypothesis; `Q1` = first open question; `NX1` = first next experiment. When the experiment log uses any of the same letters (e.g. our example uses `NQ#` for "noob questions" in a separate file), call out the convention in the section preface to avoid collisions.

## Rules of the format

These are the disciplines that keep the doc honest:

- **An experiment asks a question and produces new knowledge.** Building, shipping, documenting, refactoring are not experiments.
- **Every belief is traceable.** A bullet in Established Findings is either a lesson citing the experiment(s) that established it, or a characterization of the artifact you can verify by inspecting the code/data. If it's neither — it's a Working Hypothesis (untested belief), an Open Question (genuine uncertainty), or noise. Move it or delete it.
- **Working Hypotheses are claim-shaped and falsifiable.** Each one states the belief, the evidence base, and what specific outcome would refute it. A hypothesis you can't imagine falsifying is dogma — delete it.
- **Decisions reference, don't restate.** A decision is shaped by a belief in Established Findings (or sometimes a Working Hypothesis) plus a tradeoff judgment. Reference the belief (`per EF §3`) rather than re-paraphrasing it; otherwise the doc grows duplicate facts that can drift.
- **Every open question has a planned test.** If you can't write the experiment that would resolve it, mark it "not actionable" with the blocker (e.g., needs labeled data, needs a customer interview).
- **Decisions Made captures consequential choices, not implementation trivia.** A decision belongs here if future-you might be tempted to revisit it or quietly drift away from it. "Kept both engines side by side" qualifies; "chose pool size = 30" does not (that's a constant in code). Rule of thumb: if the reasoning would surprise someone reading the code, write the decision down.
- **Sections are mutually exclusive.** If two sections overlap, you have a stale section. Merge or delete.
- **The whole doc is refactorable.** As understanding deepens, items move between sections. Working Hypotheses become Established Findings (or are refuted). Open Questions become resolved. Next Experiments become Experiment Log rows. Edit aggressively.

## Common failure modes

The patterns that show the discipline has slipped:

- **A "Known problems" or "Issues" section that paraphrases other sections.** Most items in such a section are either already a verified lesson (→ Established Findings), an untested belief (→ Working Hypotheses), a genuine question (→ Open Questions), or being worked on (→ Next Experiments). Delete the section.
- **Working Hypotheses and Open Questions duplicate each other.** If `H1` and `Q1` are the same uncertainty in two phrasings, keep only one. Use Working Hypotheses when you have a strong prior and a falsification criterion; use Open Questions when you genuinely don't know and want to be reminded to find out.
- **Experiment log bloat.** Rows for "built the thing", "wrote the README", "fixed a typo" puff the log without capturing new knowledge. Those belong in the README or `git log`.
- **Naming collisions.** `Q1` in one section meaning something different from `Q1` in another section. Disambiguate by prefix (e.g. `NQ#` for one kind, `Q#` for another) and call out the convention in the section preface.
- **Vague Next Experiments without an ordering.** Without expected-impact ordering, the list is a wishlist. Order by "what I'd run first if I only had time for one."
- **Citations point at the wrong rows after editing.** If you renumber the experiment log or move items between sections, grep for old references and update them. A stale citation is worse than no citation.

## How to apply

1. Start by writing **Goals** and **Constraints**. These rarely change once set.
2. Leave **Experiment Log** empty. Don't pre-fill it with planned work — that's what Next Experiments is for.
3. Each time you run an experiment, append a row to the log. Then ask:
   - Did this generate a durable lesson or characterization? → add a bullet to **Established Findings** with a citation.
   - Did it produce a generalization beyond the specific test, that you believe but haven't formally verified? → add a **Working Hypothesis** with a falsification criterion.
   - Did it create new uncertainty? → add an entry to **Open Questions** with a planned test.
   - Did it close out an existing open question? → cross out / remove the question.
4. When you make a consequential choice — whether rejecting an alternative, picking a default, or deliberately accepting a tradeoff — write it into **Decisions Made** immediately, with the reasoning (referencing Established Findings rather than restating them) and a "revisit if" trigger when one exists. Don't trust future-you to remember why.
5. Re-read the whole doc at the start of each new session. If a section feels stale or duplicative, prune it before doing anything else. If a Working Hypothesis has been confirmed by recent experiments, promote it to Established Findings; if refuted, delete it.

## A worked example

See [`PS-LEDGER.md`](PS-LEDGER.md) in this repo for a non-trivial application: a comparison of two RAG engine implementations across 8 experiments, with the resulting findings, hypotheses, decisions, open questions, and ordered next steps. The doc was refactored at least seven times as understanding deepened — sections renamed, items moved between sections, a "Known problems" section was deleted once every item lived more accurately elsewhere, a narrower "Considered and deferred" was generalized to "Decisions Made", the section was repositioned to sit alongside "Established Findings" rather than near the forward-looking sections, Decisions entries were tightened to reference (not restate) the beliefs that shaped them, blockquote scaffolding was added under each section header to keep the template self-documenting, and a separate "Working Hypotheses" section was carved out to hold claim-shaped beliefs that emerged from the work but go beyond any single experiment. That refactoring is the format working as intended.

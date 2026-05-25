# PROBSOLVE — A working-state template for problem solving

A markdown layout for capturing the *current* state of solving a non-trivial problem: what you're trying to achieve, what you've learned, what you don't yet know, what you'd test next, and what you've rejected. Distinct from a project plan or a writeup — this is **working notes**, refactored as understanding deepens.

## When to use

- The problem spans multiple sessions and you need durable state to pick it up cold.
- You'll run experiments and accumulate knowledge over time.
- You'll consider alternatives and need to remember why you rejected the ones you didn't pick.
- You've ever lost track of "what was that thing I tried two weeks ago and what did it tell us?"

**When not to use**: one-shot tasks with a clear answer (just do them); pure documentation (use a README); ticket/sprint tracking (use a tracker); incident response (use a runbook).

## The sections, in order

1. **Goals** — 2–5 bullets describing what success looks like. Each one written so "done or not done" is unambiguous.
2. **Constraints** — non-negotiable limits on the solution space. Things you've decided you won't compromise on. (Examples: platform, latency budget, no external services, reproducibility requirements.)
3. **What we know** — durable findings; claims you'd carry to a similar problem. Two categories live here: (a) **lessons** earned from experiments — each cites the experiment(s) that established it; (b) **characterizations** of what you built — verifiable from the artifacts themselves, not from a hypothesis test. No floating claims of either kind.
4. **Decisions Made** — consequential choices, both rejections and acceptances. Each entry: **what** was decided, **why** (referencing What we know or Experiment log rather than re-paraphrasing them), and a **"revisit if"** trigger when one exists. The expected overlap with What we know — beliefs shape decisions — is handled by *referencing* the belief, not restating its content. Covers everything from "rejected alternative Y" to "chose default Z" to "accepted duplication W until trigger fires".
5. **Open questions** — unverified predictions and unknowns. Each one **names the experiment that would resolve it**, or is explicitly marked "not actionable" with the reason.
6. **Next experiments** — concrete actions, ordered by expected impact. Each one **either resolves an open question (cross-referenced) or is tool/coverage work** with no associated hypothesis.
7. **Experiment log** — historical record, append-only. Only entries that **asked a question and produced new knowledge**. Construction milestones and shipping decisions live elsewhere (READMEs, git log, tickets).

Optional sections, only if the problem demands them:

- **Stakeholders** — who the goals serve and whose input shapes the constraints. Useful when the problem is partly social.
- **Budget / timeline** — when cost or deadlines are first-class constraints, not just preferences.

## Rules of the format

These are the disciplines that keep the doc honest:

- **An experiment asks a question and produces new knowledge.** Building, shipping, documenting, refactoring are not experiments.
- **Every belief is traceable.** A bullet in "What we know" is either a lesson citing the experiment(s) that established it, or a characterization of the artifact you can verify by inspecting the code/data. If it's neither — it's a hunch. Move to "Open questions" or delete.
- **Decisions reference, don't restate.** A decision is shaped by a belief in "What we know" plus a tradeoff judgment. Reference the belief (`per WK §3`) rather than re-paraphrasing it; otherwise the doc grows duplicate facts that can drift.
- **Every open question has a planned test.** If you can't write the experiment that would resolve it, mark it "not actionable" with the blocker (e.g., needs labeled data, needs a customer interview).
- **Decisions Made captures consequential choices, not implementation trivia.** A decision belongs here if future-you might be tempted to revisit it or quietly drift away from it. "Kept both engines side by side" qualifies; "chose pool size = 30" does not (that's a constant in code). Rule of thumb: if the reasoning would surprise someone reading the code, write the decision down.
- **Sections are mutually exclusive.** If two sections overlap, you have a stale section. Merge or delete.
- **The whole doc is refactorable.** As understanding deepens, items move between sections. Open questions become known. Next experiments become experiment log rows. Edit aggressively.

## Common failure modes

The patterns that show the discipline has slipped:

- **A "Known problems" or "Issues" section that paraphrases other sections.** Most items in such a section are either already a verified lesson (→ What we know), an unverified prediction (→ Open question), or being worked on (→ Next experiments). Delete the section.
- **Hypotheses + Follow-ups as separate sections.** Each untested hypothesis is by definition a planned experiment. Merge them: Open questions point at Next experiments.
- **Experiment log bloat.** Rows for "built the thing", "wrote the README", "fixed a typo" puff the log without capturing new knowledge. Those belong in the README or `git log`.
- **Naming collisions.** "Q1" in one section meaning something different from "Q1" in another section. Disambiguate by prefix (e.g. `NQ#` for one kind, `Q#` for another) and call out the convention in the section preface.
- **Vague "Next experiments" without an ordering.** Without expected-impact ordering, the list is a wishlist. Order by "what I'd run first if I only had time for one."
- **Citations point at the wrong rows after editing.** If you renumber the experiment log, grep for old references and update them. A stale citation is worse than no citation.

## How to apply

1. Start by writing **Goals** and **Constraints**. These rarely change once set.
2. Leave **Experiment log** empty. Don't pre-fill it with planned work — that's what Next experiments is for.
3. Each time you run an experiment, append a row to the log. Then ask:
   - Did this generate a durable lesson? → add a bullet to **What we know** with a citation.
   - Did it create new uncertainty? → add an entry to **Open questions** with a planned test.
   - Did it close out an existing open question? → cross out / remove the question.
4. When you make a consequential choice — whether rejecting an alternative, picking a default, or deliberately accepting a tradeoff — write it into **Decisions Made** immediately, with the reasoning (referencing What we know rather than restating it) and a "revisit if" trigger when one exists. Don't trust future-you to remember why.
5. Re-read the whole doc at the start of each new session. If a section feels stale or duplicative, prune it before doing anything else.

## A worked example

See [`PS-LEDGER.md`](PS-LEDGER.md) in this repo for a non-trivial application: a comparison of two RAG engine implementations across 8 experiments, with the resulting beliefs, decisions, open questions, and ordered next steps. The doc was refactored at least six times as understanding deepened — sections were renamed, items moved between sections, a "Known problems" section was deleted once every item lived more accurately elsewhere, a narrower "Considered and deferred" was generalized to "Decisions Made" to cover both rejections and deliberate acceptances, the section was repositioned to sit alongside "What we know" rather than near the forward-looking sections, and Decisions entries were tightened to reference (not restate) the beliefs that shaped them. That refactoring is the format working as intended.

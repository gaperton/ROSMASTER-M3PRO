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
3. **What we know** — durable lessons earned through experiments. Each bullet **cites the experiment(s) that established it**. No floating claims.
4. **Open questions** — unverified predictions and unknowns. Each one **names the experiment that would resolve it**, or is explicitly marked "not actionable" with the reason.
5. **Next experiments** — concrete actions, ordered by expected impact. Each one **either resolves an open question (cross-referenced) or is tool/coverage work** with no associated hypothesis.
6. **Considered and deferred** — options evaluated and rejected, with the reasoning captured *now* so future-you doesn't re-derive the same conclusion.
7. **Experiment log** — historical record, append-only. Only entries that **asked a question and produced new knowledge**. Construction milestones and shipping decisions live elsewhere (READMEs, git log, tickets).

Optional sections, only if the problem demands them:

- **Stakeholders** — who the goals serve and whose input shapes the constraints. Useful when the problem is partly social.
- **Budget / timeline** — when cost or deadlines are first-class constraints, not just preferences.
- **Decision log** — separate from Experiment log when you make consequential non-experimental decisions (vendor picks, architecture choices) that you'll want to look back on.

## Rules of the format

These are the disciplines that keep the doc honest:

- **An experiment asks a question and produces new knowledge.** Building, shipping, documenting, refactoring are not experiments.
- **Every belief cites its evidence.** If a bullet in "What we know" doesn't trace back to an experiment row, it's a hunch — move it to "Open questions" or delete it.
- **Every open question has a planned test.** If you can't write the experiment that would resolve it, mark it "not actionable" with the blocker (e.g., needs labeled data, needs a customer interview).
- **Considered and deferred is not a parking lot.** It's for explicit rejections with reasoning. Things you might do go in Next experiments. Things you've decided not to do go in Considered and deferred.
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
4. When you decide *not* to pursue an option, write it into **Considered and deferred** immediately, with the reasoning. Don't trust future-you to remember.
5. Re-read the whole doc at the start of each new session. If a section feels stale or duplicative, prune it before doing anything else.

## A worked example

See [`TODO.md`](TODO.md) in this repo for a non-trivial application: a comparison of two RAG engine implementations across 8 experiments, with the resulting beliefs, open questions, considered-and-rejected alternatives, and ordered next steps. The doc was refactored at least four times as understanding deepened — sections were renamed, items moved between sections, and a "Known problems" section was deleted entirely once it became clear every item lived more accurately elsewhere. That refactoring is the format working as intended.

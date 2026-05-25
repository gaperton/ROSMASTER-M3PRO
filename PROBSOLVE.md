# Problem-Solving Ledger Skill

## Purpose

Use this skill when a project needs a durable record of the problem-solving process: goals, constraints, findings, hypotheses, decisions, open questions, next experiments, and experiment history.

This skill is for engineering investigations where future work depends on knowing not only the current answer, but how that answer was reached.

Typical use cases:

- comparing tools, models, engines, libraries, or architectures;
- debugging a recurring failure;
- evaluating a retrieval, robotics, ML, or software system;
- preserving experimental knowledge across sessions;
- preventing future re-discovery of already tested dead ends.

Do not use this skill for ordinary task lists, meeting notes, or one-off summaries.

---

## Core Ontology

Maintain the distinction between these categories.

### Goal

A desired end state. It should be testable as done / not done.

Example:

> Build local RAG over the robot documentation so a beginner can ask natural-language questions and receive relevant chunks with paths and heading breadcrumbs.

### Constraint

A non-negotiable limit on the solution space.

Example:

> Retrieval must run locally with no network calls after model download.

### Established Finding

A claim supported by experiments, logs, measurements, or direct observation. It may include empirical findings, causal diagnoses, and methodological lessons, but it must state or imply its scope.

Example:

> After matching stop-word filtering and fusion-pool size, sqlite-vec and LanceDB tie on observed retrieval quality for this corpus.

### Working Hypothesis

A plausible explanation or prediction not yet established by experiment.

Example:

> Corpus coverage is probably the next major quality lever because retrieval cannot recover answers absent from the source docs.

### Decision

A consequential choice made because of findings, hypotheses, constraints, or tradeoffs. Decisions should include revisit conditions.

Example:

> Keep both engines side by side until maintenance cost outweighs the value of the comparison harness.

### Open Question

A known unknown. It should point to an experiment or condition that would resolve it.

Example:

> Does `bge-large-en-v1.5` meaningfully outperform `bge-small-en-v1.5` on this corpus?

### Next Experiment

A planned action intended to resolve an open question, refine a hypothesis, or improve the evaluation toolchain.

Example:

> Rebuild both indexes with `bge-large-en-v1.5` and rerun labeled plus subjective evaluations.

### Experiment Log Entry

A chronological record of an experiment that produced new knowledge. Exclude construction milestones unless they changed what is known.

---

## Anti-Slop Rules

Apply these rules strictly.

1. Do not call empirical findings “truths.” Use “findings,” “diagnoses,” or “supported claims.”
2. Do not mix decisions into Established Findings. If a claim says what should be done, it belongs under Decisions Made.
3. Do not leave Working Hypotheses empty. Either populate it or remove the section.
4. Do not use fragile references like “section 3” when order may change. Prefer IDs: F1, H1, D1, Q1, NX1, E1.
5. Do not claim general benchmark results from one corpus. State scope.
6. Do not rescue a weak conclusion by making it tautological. If a claim only survives by becoming trivial, say so.
7. Do not record every implementation step in the Experiment Log. Only record experiments that changed knowledge.
8. Do not hide failed experiments. Failed experiments are often the most important evidence.
9. Do not confuse “not tested” with “false.” Put untested claims under Working Hypotheses or Open Questions.
10. Do not remove revisit conditions from decisions. They are what make decisions reversible rather than dogma.

---

## Update Procedure

When updating a ledger, follow this sequence.

1. Read the current ledger fully.
2. Identify whether the new information is:
   - an established finding;
   - a working hypothesis;
   - a decision;
   - an open question;
   - a next experiment;
   - an experiment-log entry.
3. Check whether the new information changes an existing section rather than adding a new section.
4. Preserve scope. Every finding should imply the conditions under which it is valid.
5. Add or update IDs if the ledger uses them.
6. Add revisit conditions for new decisions.
7. Remove obsolete next experiments once completed, but preserve their results in the Experiment Log.
8. If an experiment resolves an open question, update both the Open Questions and Established Findings sections.
9. If an experiment falsifies a hypothesis, mark it explicitly instead of silently deleting it.

---

## Recommended Ledger Template

```markdown
# Problem-Solving Ledger

## Goals

> 2–5 bullets describing what success looks like. Each should be testable as done / not done.

- ...

## Constraints

> Non-negotiable limits on the solution space.

- ...

## Established Findings

> Empirical findings, causal diagnoses, and methodological lessons supported by the experiment log. Each claim should state or imply its scope.

- **F1. [Finding title].** [Claim, scope, and evidence reference.]
- **F2. [Finding title].** [Claim, scope, and evidence reference.]

## Working Hypotheses

> Plausible explanations or predictions not yet established by experiment.

- **H1. [Hypothesis title].** [Claim.]  
  *Falsified by:* [What evidence would make this false.]  
  *Test:* [Experiment or condition that would test it.]

## Decisions Made

> Consequential choices to preserve or reconsider deliberately.

- **D1. [Decision title].**  
  *Decision:* [What was decided.]  
  *Why:* [Findings, hypotheses, constraints, or tradeoffs.]  
  *Revisit if:* [Condition that should reopen the decision.]

## Open Questions

> Important things we know we do not know. Each should point to an experiment that can resolve it.

- **Q1. [Question].** [Why it matters.]  
  *Test:* NX1.

## Next Experiments

> Planned actions expected to resolve open questions, refine hypotheses, or improve the toolchain. Ordered by expected impact.

1. **NX1 — [Experiment name].**  
   [Action and method.]  
   *Resolves:* Q1.

## Experiment Log

> Chronological record of experiments that produced new knowledge.

Excludes construction milestones and shipping decisions; those belong in READMEs, commits, or implementation notes.

| # | Question tested | Method | Result / new knowledge | Produces |
|---|---|---|---|---|
| E1 | ... | ... | ... | F1 / H1 / D1 / Q1 |
```

---

## Quality Checklist

Before considering the ledger clean, verify:

- Goals are testable.
- Constraints are actually non-negotiable.
- Findings are supported by experiments or direct evidence.
- Findings do not contain hidden decisions.
- Hypotheses are testable or falsifiable.
- Decisions include reasons and revisit conditions.
- Open questions point to resolving experiments.
- Next experiments are ordered by expected impact.
- Experiment log entries changed knowledge.
- Scope is stated for any claim that could otherwise look universal.
- Failed or negative results are preserved.

---

## Response Style for Hermes

When using this skill, respond as an engineering reviewer, not as a motivational coach.

Preferred style:

- direct;
- structured;
- sparse but complete;
- explicit about category errors;
- explicit about unsupported claims;
- willing to say “this belongs in another section.”

Avoid:

- generic praise;
- vague “looks good” comments;
- over-broad conclusions;
- philosophical decoration unless it clarifies the ontology;
- changing the substance of findings while merely editing prose.

---

## Minimal Final Skeleton

```markdown
# Problem-Solving Ledger

## Goals
## Constraints
## Established Findings
## Working Hypotheses
## Decisions Made
## Open Questions
## Next Experiments
## Experiment Log
```

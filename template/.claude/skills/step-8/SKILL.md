---
name: step-8
description: Step 8 — fold what a finished unit taught into the plan that is left. Use when a journey is complete and deployed, or a release's clean-up or layer pass is. Runs the handoff to zero as its last step. Triggers: "run step 8", "the journey is done", "the clean-up is done", "the layer pass is done".
---

# Step 8 — fold what the journey taught into the plan that is left

The journey is finished. What it changed about the **unbuilt** work is written
down nowhere yet.

This is the load-bearing step and the easiest to skip, because it happens after
the work feels finished and produces nothing demonstrable. Everything short in
this document set is short because it ran.

**The question is not "what did we learn". It is "what does this make false
elsewhere".**

The same step closes the two units at the end of a release, the clean-up and the
layer pass. Read "journey" below as whichever unit just finished. For the layer
pass, the first question carries most of the weight: a reshaped surface between
layers changes what every later journey will build against.

## 1. Ask the four questions

Work through all four before writing anything — the answers overlap and routing
them one at a time produces duplicates.

**What does this make false elsewhere?** Contradictions with unbuilt work are the
highest-value output. A rule built in this journey may silently conflict with a
decision already recorded for a later one; that is invisible from inside the
finished journey and appears only when looking forward. Read the remaining
journey documents and the open items with this journey's result in hand.

**What did this journey change that it did not add?** Split the diff. What it
added is the work. What it **changed** in code earlier journeys wrote is a lesson
arriving late — that code was wrong or insufficient and nothing knew until this
journey asked it a question it had to refuse. These are the highest-yield design
notes available, because they are proven rather than anticipated.

**What did this journey decide not to do?** The simplification pass produced
fixes applied and findings skipped; only the first landed in a commit. Every
skipped finding goes to the roadmap's open items with what was skipped, why, and
**the event that would change the answer**.

**Did anything fit no routing category?** Answer explicitly, yes or no, and
record it in `docs/experiments.md` under E3. Silence there is ambiguous —
complete categories and an unread instruction look identical.

## 2. Route each answer

Use the ordered question in `CLAUDE.md`. Briefly:

architecturally significant → **ADR** · a rule for writing similar code →
**design notes** · a word → **glossary** · changes what is left to build →
**roadmap** · work too small for a journey → the release's **clean-up list** in
the roadmap · changes how the next change is made → **CLAUDE.md** · belongs to
the business → **stakeholder questions**

## 3. Rewrite, do not annotate

**The test of a finished step 8: a reader who has never seen the previous version
cannot tell which parts changed.**

A correction written as "this used to say X" is history, and history is
`git log`. Rewrite the affected sections of the roadmap, the remaining journey
documents and the architecture document so they say what is now known rather than
what was assumed.

This is the discipline that keeps the plan a plan. Appending is easier than
revising, and a roadmap that accumulates a findings section per journey becomes a
document somebody reads a thousand lines of completed work in, looking for the
next step.

## 4. Close out

- Update `docs/architecture.md` if the shape changed, or if it currently asserts
  something the code does not do.
- **Run the handoff to zero.** Take one signal, handle it, delete the item that
  raised it, take the next — until nothing remains. Then delete the file, because
  it has reached nothing rather than in order to declare the journey over. The
  `handoff` skill is this loop.
- Run the gate, then commit.
- If the journey's `Lesson:` trailers did not parse, do **not** rewrite history to
  fix them — the trailer is a capture aid and the record is what you just routed.

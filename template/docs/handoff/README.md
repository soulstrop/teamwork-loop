# Handoff

**The job:** the current unit of work's micro-state — what is done, what remains,
in what order — so that a session starting from zero can resume it. One file per
journey in flight, named for the journey. Usually there is one; sometimes none.

**Not the job:** anything durable. A rule, a decision, a lesson, a deferral —
each has a home, and the handoff is not it. See the routing question in
[`../../CLAUDE.md`](../../CLAUDE.md#6-where-a-thing-goes--ask-in-this-order).

A document with no stated job collects everything unfiled; the handoff was that
document once, and [`../dev-process.md`](../dev-process.md#the-three-failure-modes-all-of-which-happened)
has what it cost.

## Lifecycle — it burns down to nothing

1. **Created** when a journey starts, or when work is interrupted mid-journey.
2. **Revised in place, and shrinking.** It is state, not a log: rewrite it. A
   handoff that is growing is a unit of work that is growing.
3. **Deleted when it reaches nothing**, at step 8. If deleting it would lose
   something, it had not reached nothing.

What empties it is the residue loop in
[`../../CLAUDE.md`](../../CLAUDE.md#7-the-handoff-and-the-residue-loop); why it
is a loop is in
[`../dev-process.md`](../dev-process.md#the-handoff-burns-down-and-the-residue-loop-runs-to-zero).

## Committed, not ignored

These files are **committed**, and deleted when the journey ships.

That is a deliberate departure from the obvious arrangement. The argument for
ignoring them is that they are disposable working state and the set holds no
record of what used to be true. The argument that wins is the method's own axiom:
**context that is not in the repository does not exist.** A collaborator resuming
on another machine, in a fresh session, or in a cloud environment cannot read an
ignored file — which makes an ignored handoff a resume aid that fails in exactly
the case it was written for.

The concern it raises is answered by the lifecycle rather than by ignoring it:
the file is deleted at step 8, so nothing accumulates, and `git log` holds the
deleted versions for anybody who needs to know what a journey looked like
half-built.

**If this project ignores them instead**, say so here and accept that resuming is
a single-machine operation.

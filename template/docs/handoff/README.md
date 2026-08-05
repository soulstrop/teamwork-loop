# Handoff

**The job:** the current unit of work's micro-state — what is done, what remains,
in what order — so that a session starting from zero can resume it. One file per
journey in flight, named for the journey. Usually there is one; sometimes none.

**Not the job:** anything durable. A rule, a decision, a lesson, a deferral —
each has a home, and the handoff is not it. See the routing question in
[`../../CLAUDE.md`](../../CLAUDE.md#6-where-a-thing-goes--ask-in-this-order).

This file exists because that second paragraph was learned the hard way.

## Why it has a stated job

**A document with no stated job collects everything unfiled.** In the project
this method was generalised from, the handoff was the only document without a
defined job, so anything that fitted nowhere landed there — and the handoff is
deliberately disposable. Two consciously-deferred findings, with the reasoning
behind them, existed nowhere else and were one `rm` from being lost.

The failure was not carelessness. It is what happens structurally when one
document in a set will accept anything: it becomes the lowest-energy destination
for exactly the material that most needs a considered home.

## Shrinking it to nothing is the objective

**The handoff is a register of what is not yet done or not yet routed, and its
target state is empty.** That is not a test applied at the end — it is what the
unit of work is driving at. A journey is finished when its handoff is nothing,
and the file is deleted because there is nothing left in it rather than deleted
in order to declare it finished.

That distinction changes how the document is used. A handoff treated as a report
gets written once and read at resume. A handoff treated as a burn-down gets
**shorter every session**, and its length is the honest measure of how much of
the unit is left.

1. **Created** when a journey starts, or when work is interrupted mid-journey.
2. **Revised in place, and shrinking.** It is state, not a log — rewrite rather
   than append. A handoff that reads as a diary has become a record of what used
   to be true, which no committed document here is. A handoff that is growing is
   a unit of work that is growing.
3. **Deleted when it reaches nothing**, at step 8. If deleting it would lose
   something, it had not reached nothing.

## The residue test, run to fixpoint

**Whatever is in the handoff that is not already somewhere is, by definition,
something with no home.** Work it as a loop, not a pass:

> **Take one signal → handle it → remove the item that raised it → take the
> next.** Repeat until there are no signals left.

**Removing the item is what proves it was handled.** An entry routed but left in
place is indistinguishable from one nobody has looked at, and on the next read it
costs the same attention again. The deletion is the receipt.

Handling depends on which kind it is:

- **Knowledge** → route it (a rule, a decision, a word, a plan change), then
  delete the line. The handoff caught a miss, which is it working.
- **Checkable state** → a document is the wrong fix. Make a task refuse, then
  delete the line. The task is now the thing that remembers.
- **Neither** → **stop, and treat it as a process finding.** A document is
  missing a job, or a category is wrong. Log it in
  [`../experiments.md`](../experiments.md), raise it, and only then delete the
  line.

**Expect the loop to lengthen before it shortens.** Handling one signal routinely
surfaces another — routing a rule reveals that two documents disagree, making a
task refuse reveals a second caller. That is the loop working, and it is why the
exit condition is *no signals remain* rather than a number of passes.

**The third branch is the one worth protecting.** It is the only signal about the
process that arrives without anybody going looking for it, and it is the easiest
to lose: filing it into the nearest approximate bucket empties the line, feels
like progress, and means the categories are never questioned. Emptying the
handoff is the objective — but emptying it by filing things where they do not
belong is how the register gets to zero while the project learns nothing.

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

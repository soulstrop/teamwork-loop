---
name: handoff
description: Write or update the handoff for the journey in flight, and run the residue test against it. Use when pausing work mid-journey, when resuming and the handoff is stale, or at step 8 before deleting it. Triggers: "write the handoff", "update the handoff", "pausing here", "wrap up for now", "close out J<N>".
---

# Handoff

The handoff is the current unit of work's **micro-state** — what is done, what
remains, in order — so a session starting from zero can resume it. Its job and
its lifecycle are in `docs/handoff/README.md`; the shape is
`docs/handoff/TEMPLATE.md`.

## Writing or updating one

1. **Find the journey in flight.** `docs/handoff/` holds one file per journey,
   named for it. If none exists and work is underway, create it from the
   template.
2. **Rewrite in place. Do not append.** It is state, not a log. A handoff that
   reads as a diary has become a record of what used to be true, which no
   committed document here is.
3. **Fill the definition-of-done table from the actual test run**, not from
   memory. It is the first thing a resuming session reads to find out how far
   along the work is, and a table that is optimistic is worse than none.
4. **Order what remains, next action first.** "What is left" without an order is
   a list somebody has to re-derive priorities from.
5. **End with one sentence under *Next*** — the single next action, so a session
   with no context can start without reading the rest.

## The residue test — a loop, run every time

**Shrinking the handoff to nothing is the objective of the unit of work**, so
this is not a check performed once at the end. Run it whenever you touch the
file, and the file gets shorter each time.

**Whatever is in it that is not already somewhere is, by definition, something
with no home.** Work it one item at a time:

> **Take one signal → handle it → remove the item that raised it → take the
> next.** Repeat until no signals remain.

**Delete the line as part of handling it, in the same pass.** An entry routed but
left in place is indistinguishable from one nobody has looked at, and it costs
the same attention again on the next read. The deletion is the receipt.

- **Knowledge** — a rule, a decision, a word, a plan change. Route it using the
  question in `CLAUDE.md`, then delete the line. The handoff caught a miss, which
  is it working.
- **Work too small for a journey**, and belonging to no other one — add a line
  to the current release's clean-up list in `docs/roadmap.md`, naming this
  journey, then delete the line here.
- **Checkable state** — something a task could assert rather than a document.
  Make the task refuse, then delete the line. The task is now what remembers.
- **Neither** — **stop and say so.** A document is missing a job or a routing
  category is wrong. Log it in `docs/experiments.md` under E3 and raise it with
  the user *before* deleting the line. Do not file it into the nearest
  approximate bucket: that empties the line, feels like progress, and means the
  categories are never questioned.

**Expect the list to lengthen before it shortens.** Handling one signal routinely
surfaces another — routing a rule reveals two documents disagreeing, making a
task refuse reveals a second caller. That is the loop working, and it is why the
exit condition is *no signals remain* rather than a number of passes.

## At step 8

The handoff is deleted **because it has reached nothing**, not in order to
declare the journey over. If deleting it would lose something, it has not reached
nothing — run the loop again on what is left.

Then delete the file and commit the deletion with the rest of step 8.

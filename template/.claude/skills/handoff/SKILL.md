---
name: handoff
description: Handoff for the journey in flight — rewrite it as current state and run its residue loop to zero. Use when pausing mid-journey, or resuming with a stale handoff. Triggers: "pausing here", "resuming J<N>", "update the handoff".
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

## The residue loop — every time you touch the file

Run the loop in `CLAUDE.md` §7 until no signals remain. What it adds here:

- **Delete each line in the same pass that handles it.**
- **A clean-up line names this journey**, so the clean-up knows where it came
  from.
- **A line that fits no kind is the finding.** Log it in `docs/experiments.md`
  under E3 and raise it with the user, then delete the line. Its value is that it
  questions the categories, so it stays unfiled.

## At step 8

The handoff is deleted **because it has reached nothing**, not in order to
declare the journey over. If deleting it would lose something, it has not reached
nothing — run the loop again on what is left.

Then delete the file and commit the deletion with the rest of step 8.

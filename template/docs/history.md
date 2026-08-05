# History

**Generated. Do not edit.** Rebuilt from `git log` by the `history` task.

Anything typed into this file is overwritten on the next run, which is the
correct direction: the log is authoritative and this is a render of it.

## Why a generated document is allowed here

The set's rule is that **history is `git log`** — no committed document records
what used to be true, because a maintained history is one that drifts from the
thing it describes and nothing reports the divergence.

A *generated* narrative is exempt for exactly that reason. It cannot drift,
because it is not maintained. It is a rendering of the source of truth in a form
somebody can read end to end, which the log is not.

The same exemption covers any other generated output the project adds — a
document bundle, an export, an extracted list of lessons.

## What the task should produce

*Adjust to what the project actually wants. The shape that has proved useful:*

- **Releases and journeys, in order**, each with what it made possible rather
  than a list of commits. A reader wants the narrative, not the log they already
  have.
- **The `Lesson:` trailers**, extracted. Captured at the moment of insight by
  whoever hit the thing, and worth reading together — a lesson that appears twice
  in different words is a rule that was never written, and that is the signal the
  [process loop](dev-process.md#8-the-process-loop) runs on.
- **Dates and shas**, so any entry can be taken back to the diff.

Two things to get right in the task itself:

**A trailer only parses in the last paragraph of the message**, and only on lines
that are `Key: value` or a whitespace-indented continuation of one. A `Lesson:`
after a blank line is not a trailer, and one whose wrapped second line starts at
column 0 stops being one there — both silently, with the extraction simply not
listing them. Whatever writes commits should be checked against this once.

**Never rewrite history to add a trailer.** The trailer is a capture aid; the
record is the ADR, the design note or the plan. A missed one is a lesson to route
by hand, not a reason to rewrite a commit somebody may have deployed.

---

*(Generated content begins below. Nothing above this line survives a rebuild —
move it into the task's own header if it should.)*

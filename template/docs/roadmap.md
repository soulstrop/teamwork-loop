# Implementation plan

## Where we are

*Two or three sentences, rewritten every time a journey lands. Which release,
how far into it, what is next, and what the last journey found that changes the
rest. A reader arriving cold should be able to start from this paragraph.*

*If there is a deployed environment, name the release it is running and anything
about its state that would mislead somebody who assumed it was current.*

What the system is and who uses it is [`../README.md`](../README.md); why it is
shaped as it is, is an [ADR](adr/README.md); what each unit of work must do is a
[journey](journeys/README.md). **This document is what is left to build.**

## Journey inventory

**Journeys exist in two forms**, and the distinction matters more than it looks:

- **A document** — a full journey specification in
  [`journeys/`](journeys/README.md), linked from the table. Every journey in the
  current release is one of these; so is anything deferred out of a previous
  release, which carries its document forward unchanged rather than reverting to
  a line.
- **A sketch** — a row and a sentence, held in this table and nowhere else. It
  names a journey identified as necessary, without claiming to know what it says.

**Two reasons a journey is still a sketch**, and they are worth telling apart in
the row:

*Not thought about deeply yet.* Real but not yet examined. Writing it is cheap
whenever somebody wants to.

*Deliberately unwritten, because the release before it will decide what it
says.* Writing it now produces fiction that later reads as a decision. This is
the more common case for anything two releases out, and it is the reason journey
documents are drafted a release at a time rather than all at once.

**Promoting a sketch is part of the release boundary.** When a release becomes
current, its sketches are written into documents *before* the first of them is
built — drafting them together is what surfaces the ordering, the shared rules
and the questions belonging to somebody else.

**Numbers are permanent through all of this.** A journey deferred to a later
release keeps its number and its document; the suffix rule
([`journeys/README.md`](journeys/README.md#numbering)) exists so that no
rearrangement ever renumbers anything.

### Release 1 — *(what it makes possible)*

*All documents. State is `done` · `next` · blank.*

| # | Journey | Actor | State |
|---|---|---|---|
| J1 | | | |
| J2 | | | |

*Link each row to its document as it is written. Left unlinked until then, so the
link checker passes on an empty project.*

### Release 2 — *(what it makes possible)*

*A mix. Linked rows have documents; the rest are sketches with a reason.*

| # | Journey | Actor | Form |
|---|---|---|---|
| | | | sketch — *waiting on Release 1's decision about …* |
| | | | sketch — *identified, not yet examined* |

*Notes on ordering go here as prose, not as a column: why a journey sits where it
does when the number suggests otherwise, and what it is waiting on.*

## Definition of done

The `ship` task green, plus whatever the project's dials add — see
[`../CLAUDE.md`](../CLAUDE.md) for the settings and
[ADR 0002](adr/0002-tooling-roles.md) for what the gate covers.

The eight-step loop is in
[`../CLAUDE.md`](../CLAUDE.md#4-the-journey-loop--eight-steps-every-journey) and
the reasoning is [`dev-process.md`](dev-process.md). Neither is repeated here.

## Open items, not blocking

*The most valuable section in this document, and the one that decays fastest
without discipline.*

**Every entry carries three things:** what it is, when and where it was found,
and **the event that would change the answer**. An item without the third is a
note nobody re-reads — and worse, it is one the next simplification pass raises
again from scratch, having lost the reason it was declined.

**Deferrals belong here as much as findings.** Step 6 produces fixes applied and
findings skipped, and only the first lands in a commit. A skipped finding
recorded nowhere committed is one that gets re-argued.

*Format:*

> - **A one-line statement of the thing** — *found in J*N*, date; skipped with a
>   reason.* What it is, in a paragraph. Why it was not done. **What would change
>   the answer:** the concrete event.

## Verification

*What gets tested, at which layer, and why that layer is the one that can answer
it. Grows as the project finds out what its own correctness risks are.*

*The general rule: a test earns its place by naming a failure it would catch that
nothing else would. A layer earns its place by answering a question the layers
either side of it cannot.*

## Structural changes

*Additive, each introduced by the journey that needs it. Delete this section if
nothing here migrates or has a schema.*

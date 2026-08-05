# Journeys

One file per journey. Each describes what somebody is trying to accomplish, what
has to be true before they start, the steps they take, what they end up with, and
the edge cases that make it harder than it looks.

**A journey is the unit of implementation.** Development proceeds one journey at
a time, not one layer at a time. Each begins with a failing end-to-end test that
defines done, then red-green-refactor inward. The loop is in
[`../../CLAUDE.md`](../../CLAUDE.md#4-the-journey-loop--eight-steps-every-journey);
the reasoning is [`../dev-process.md`](../dev-process.md).

## Scope of these documents

| Contains | Does not contain |
|---|---|
| Actor, precondition, steps, outcome, edge cases | Component structure — see [`../architecture.md`](../architecture.md) |
| What the E2E must prove | Decision rationale — see [`../adr/`](../adr/README.md) |
| Domain rules the journey exercises, **cited** | Those rules restated — see [`../design-notes.md`](../design-notes.md) |

That last row is the one that decays first. A journey document is read at the
start of an implementation session, so every rule it restates is a rule with two
spellings and one reader. Cite instead.

## Numbering

Sequential and permanent: `J1`, `J2`, `J3`. The number is not a priority and not
a dependency order — it is an identity, used in cross-references, test markers
and commit messages.

**A journey that turns out to need a sibling gets a suffix**, never a renumber:
`J4b` is a second door to the same rows, `J4c` a second way of filling the same
column. Neither is a later stage. Renumbering to open a slot rewrites every
cross-reference in the set in exchange for a tidier sequence nobody reads as a
sequence.

**Build order is allowed to differ from numbering**, and where it does, the
document says why. Dependency beats sequence.

## Releases

Group journeys into releases by what the release makes possible, not by size. The
inventory lives in [`../roadmap.md`](../roadmap.md) — this file indexes the
documents; the roadmap holds their state and what is left.

Write a release's journey documents before building any of it. Drafting them all
is what surfaces the ordering, the shared rules and the questions that belong to
somebody else — and it is cheap, because a journey document is a page.

**Journeys for later releases are sketched rather than written**, and a sketch
lives in [`../roadmap.md`](../roadmap.md#journey-inventory) rather than here — a
row and a sentence, with the reason it is still a sketch. There are two reasons
and they are worth telling apart: *not examined yet*, which is cheap to fix
whenever somebody wants to; and *deliberately unwritten because the release
before it will decide what it says*, which is the more common case and where
writing early produces fiction that later reads as a decision.

**A journey deferred out of a release keeps its document**, and its number. It
does not revert to a sketch — what was learned writing it is still true.

This directory therefore holds every journey that has a document: the current
release's, and anything carried forward. The roadmap holds their state and the
sketches.

## These documents are revised as journeys land

Step 8 carries what a journey taught into the documents for work that has not
been built yet, so the next journey starts from what the last one found rather
than rediscovering it.

**A journey document untouched since it was first written is a document step 8
has not been run against.** That is worth checking directly, because nothing else
will report it.

## Index

*One table per release. Delete this note and fill in as journeys are drafted.*

### Release 1 — *(what it makes possible)*

| # | Journey | Actor |
|---|---|---|
| J1 | | |
| J2 | | |

### Release 2 — *(what it makes possible)*

*Sketches only until Release 1 lands.*

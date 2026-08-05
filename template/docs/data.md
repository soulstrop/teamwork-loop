# The data store

*Conditional — delete this file unless somebody who did not write the code has to
look after the data.*

For whoever is responsible for the store and has not worked on this application.
It assumes they know the technology and know nothing about the domain: how to
reach it, what it holds, which rules are load-bearing, and what a well-meaning
hand at a prompt can break that nothing will report until much later.

**It is not the deploy procedure** — that is [`deployment.md`](deployment.md).
**It is not the rationale** either; each decision below links to the ADR that
argued it. What belongs here is the store as an object somebody looks after.

**Open with the one-sentence version.** The single most important true thing: the
schema is generated only by migrations, the application connects as something
that cannot alter it, and *(the one rule the system exists to guarantee)*.

## What you are looking after

*The technology and version, anything non-optional about the installation, and
the databases or namespaces that exist — including the ones that are safe to
browse and the ones that are not.*

## Connecting

*Which identity for which purpose, and how a person connects, which is usually
none of the application's identities.*

*Where privileges are split — one identity that can change the shape, one that
can only read and write rows — say why: the process most exposed to the outside
should not be able to remove the constraint that protects it.*

## What is in it

*The spine first, as a chain, in the domain's words: what produces what. Then a
table by area. This is the map, not the dictionary — the
[glossary](glossary.md) defines the words.*

*Single out the two or three tables somebody answering a question will actually
need, and say what each is for. The ones that earn it are usually the frozen
record, the audit trail, and anything that cannot be recomputed after the fact.*

## The constraints that are the product

*Which rules are enforced by the store rather than by code, and why each one is
there. This is the section that stops somebody dropping a constraint to make an
insert work.*

*Where a check enumerates a closed set, say what happens to a value outside it —
if a code becomes a sentence somebody reads, an invented one is displayed to a
person as itself.*

*Say what cascades. If nothing does, say that too: a delete that takes more than
you meant is not recoverable at a prompt.*

## Things that will surprise you

*The behaviours that are correct and counter-intuitive. Every one of these is
something somebody has already got wrong, or will.*

*The recurring shapes worth checking for:*

- **A read that bypasses an audit trail.** If reading through the application
  logs the read, reading at a prompt does not — and the absence of a log entry is
  not the absence of a read.
- **Versioned rows that must not be updated in place.** Editing one silently
  rewrites history; work already derived under the old version will re-derive
  differently, with nothing to compare against.
- **A date that is not the date it looks like.** Any domain with a working day
  that does not align to the calendar day has one of these, and grouping by the
  obvious field quietly gives a different answer than the system does.
- **Time zones and offsets**, wherever a stored instant is rendered somewhere
  with an opinion about locality.
- **A rule enforced only in application code**, which is exactly what
  hand-editing walks straight through.

## Changing data by hand

*When it is legitimate — there is usually one case, such as the first account on
a fresh environment — and the rules for everything else.*

*The ones that generalise: never change the shape outside a migration; never
disable a constraint to make a write succeed; never hand-write a row that
something else produces as part of a transaction, because the row without its
siblings is a fact with no explanation attached.*

## Routine care

*Backups, growth, and anything periodic. **Backups are verified by restoring
them**, not by a job that reports success — and if that has not been rehearsed,
this section should say so rather than imply otherwise.*

## When something looks wrong

*Read-only queries that answer the questions people actually ask. Each one worth
a line saying what a non-empty result means.*

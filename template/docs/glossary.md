# Glossary

The domain language, and what each word means **in which context**. A word often
means one thing in the schema and a narrower thing in the domain; that is usually
deliberate, and where it is not, this says so.

**Why this document exists.** More than one defect is a naming problem wearing a
bug's clothes — a key colliding with a method name, a code unique at the wrong
scope, a word that quietly acquired a third meaning. The rule is
[one word must not acquire a third meaning](design-notes.md#modelling); this is
where you check before spending the second.

**Rejected names are part of the record.** A name considered and turned down is
the cheapest way to stop somebody re-proposing it, and the reason is usually a
constraint that still holds.

| Section | |
|---|---|
| [Words that mean different things in different places](#words-that-mean-different-things-in-different-places) | Check here first |
| [The domain](#the-domain) | This project's own words |
| [Words about the work](#words-about-the-work-not-the-system) | Seeded with the method's |
| [Names considered and rejected](#names-considered-and-rejected) | And why |
| [Deliberately unnamed](#deliberately-unnamed) | Gaps not being filled yet |

---

## Words that mean different things in different places

*The most valuable section and the one that stays empty longest, because a
collision has to be noticed before it can be written down. When one is found
while it is still free to avoid, that is the win — the entry costs a line and the
unpicking costs a journey.*

## The domain

*This project's words, grouped as the domain groups them rather than as the code
does. Each entry is one sentence saying what the thing is, and — where it
matters — what it is **not**.*

## Words about the work, not the system

These name how the work is done rather than what it does. They are here for the
same reason as everything above: they are precise, they could drift, and some of
them collide with words a codebase has already taken.

**Journey.** One actor completing one goal end to end. The unit of
implementation, and the thing a numbered document and a numbered E2E both refer
to.

**Journey loop.** The eight steps, once per journey. Step 8 is what feeds back
into the plan.

**Inner loop.** The tight build cycle inside one journey — the `check` task and
the journey's own E2E, run continuously.

**Process loop.** The feedback loop that changes how the work is done. Its output
is [`dev-process.md`](dev-process.md), `CLAUDE.md` and the tasks, rather than the
application. Distinct from **residue** in that it is *reflective*: somebody
notices friction and goes looking, where residue arrives unbidden.

*Rejected:* **method loop**, because `dev-process.md` already names the subject
and a second word for it is the divergence this document exists to prevent.
**Outer loop**, because it implies a middle that does not exist.

**Residue.** What is in the handoff that is not already somewhere else — by
definition, something with no home. Handled as a **loop**: take one signal, deal
with it, remove the item that raised it, take the next, until none remain.
Removing the item is what proves it was handled. Residue fitting *no* routing
category is a process finding, not a filing problem.

**Handoff.** The current unit's register of what is not yet done or not yet
routed. **Shrinking it to nothing is the objective of the unit of work**, so it
gets shorter every session; the file is deleted because there is nothing left in
it, rather than deleted to declare the journey over. Revised in place, never
appended to. See [`handoff/README.md`](handoff/README.md).

**Step 0.** Project initialisation. Not a journey: no actor, and nothing an E2E
could assert. Produces the first ADRs and the filled-in `CLAUDE.md`.

**Dial.** A part of the method that varies with the kind of project rather than
being a rule. The dials, and what each kind sets them to, are in
[`dev-process.md`](dev-process.md#the-dials-and-what-sets-them).

**The gate.** The `ship` task. The definition of done, and the thing nothing is
allowed past.

**Witness.** A value that explains a verdict rather than asserting it — the date
two windows both claim, rather than "they overlap". Prefer returning one; derive
the boolean from it.

## Names considered and rejected

| Wanted | Rejected | Why |
|---|---|---|
| | | |

## Deliberately unnamed

*Concepts that do not have a word yet, and should not get one until something
needs it. Naming early means guessing at what a reader wants. Record the gap so
the guess is not made accidentally.*

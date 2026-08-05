# J*N* — *what the actor accomplishes, in their words*

*One or two sentences: who wants what, and why it matters. If this needs a
paragraph, the journey is probably two journeys.*

- **Actor:** *who is doing this, and what they are entitled to*
- **Precondition:** *what must already exist. Usually the output of an earlier
  journey — name it*
- **Outcome:** *what is true afterwards that was not true before*

## Steps

*What the actor does, in order. Written from their side of the screen, not the
system's. Each step is something they would describe doing.*

1.
2.
3.

## States

*The steps above are transitions, so this journey has a state machine whether or
not anybody draws it. Name the states here, in the actor's words.*

*They are worth naming because the same names are then used in four places: the
E2E assertions, the transition trail recorded at runtime, what a person says when
they report a problem, and any sequence diagram drawn to settle an argument. A
trail reading `chose a date → saw three options → was refused` needs no
translation; one reading in module names has to be translated by whoever is least
able to. See [`../diagnostics.md`](../diagnostics.md).*

*Include the states that are not on the happy path — refused, expired, empty,
already-done. Those are the ones a report arrives about.*

| State | Reached by | Leaves by |
|---|---|---|
| | | |

## What the end-to-end test must prove

*This is the contract. Each line becomes an assertion, and the test is written
and committed red before any implementation. Its URLs, labels and accessible
names are what the implementation must satisfy — not suggestions to improve on
while building.*

| # | Assertion |
|---|---|
| 1 | |
| 2 | |

**Accessibility is asserted inside these tests, not beside them.** Select by
accessible role and name. A control nobody can ask for by name is a defect the
same suite should find.

## Edge cases

*The cases that make this harder than it looks. Each one either becomes an
assertion above, or is explicitly out of scope with a reason.*

- **
- **

## Rules this journey inherits

*Cite, do not restate. Links into [`../design-notes.md`](../design-notes.md),
[`../adr/`](../adr/README.md) and [`../glossary.md`](../glossary.md) for the
rules that already apply here — this section is what makes the journey document
sufficient as an implementation session's starting point.*

-
-

## Decisions this journey owns

*Questions deliberately deferred to this journey by earlier work, and questions
this journey will have to settle. Pre-registering them is what turns "the agent
asked something" into "the process worked".*

*A question here that rises to a design decision is not for guessing — present
the alternatives and their implications, and the answer becomes an ADR.*

-

## Not in this journey

*What a reader might reasonably expect here and will not find, with where it
lives instead. This is the section that stops the next journey rebuilding
something.*

-

# Design notes

Rules learned by getting them wrong, and settled decisions too small for an
[ADR](adr/README.md). One place to look before writing code with a shape somebody
has already paid for.

**This is not the plan and not the rationale.** What is being built next is
[`roadmap.md`](roadmap.md); why the architecture is shaped as it is, is an ADR;
what a screen must do is a [journey](journeys/README.md). A rule earns a place
here when it is **actionable in advance** and would otherwise be re-learned.

**Provenance is marked.** `[inherited]` came with the method — paid for
elsewhere, kept because it kept recurring. Everything else carries the journey
that produced it, which is the pointer into `git log` where the narrative lives.
A rule that survives contact with this project can drop its `[inherited]` mark
and take a journey citation instead; one that turns out not to apply here should
be deleted rather than carried.

| Group | For when you are |
|---|---|
| [Make the door refuse](#make-the-door-refuse) | About to write down a convention |
| [A guard is only as good as its reach](#a-guard-is-only-as-good-as-its-reach) | Adding a check, a flag or a static test |
| [Silent fallbacks](#silent-fallbacks) | Handing a value to something you do not control |
| [Decide what a layer receives](#decide-what-a-layer-receives) | Designing a query, a model or a template context |
| [Placement and layering](#placement-and-layering) | Resolving an import cycle, or extracting a helper |
| [One spelling of a fact](#one-spelling-of-a-fact) | Writing a comment, a count, or a second list |
| [Boundaries](#boundaries) | Reading or writing somebody else's format |
| [Tests and fixtures](#tests-and-fixtures) | Writing a fixture, or explaining a flake |
| [Changing code that works](#changing-code-that-works) | Refactoring, renaming or deleting a rule |
| [Deploying](#deploying) | Anything that has to exist in the artifact |
| [Modelling](#modelling) | Deciding what a thing *is* |

---

## Make the door refuse

The most-repeated finding there is. When a rule is about to be written down as a
convention, **find the door the value comes through and make that door refuse.**

**A rule that has to be remembered at the moment it matters is not a rule.**
[inherited]

**If a rule is enforced by every caller remembering, count the callers who did —
the number is never all of them.** [inherited] Measured once at two routes out of
eight, one journey after the rule was written down. The journey that *recorded*
the rule had already broken it in its own code.

**A helper is not a door.** [inherited] A helper every caller is supposed to call
is the same thing as a convention. Ask inside the function each path already
funnels through, not at the top of three callers.

**Instrumentation should be structural, not remembered.** [inherited] Make the
only way to do the thing be the way that records it — then "definition of done
includes emitting metrics" stops depending on discipline.

**Each of these deserves a static half.** A runtime guard only fires on a path
some test exercises, and the failure being guarded against is a path nobody took.

## A guard is only as good as its reach

**A constraint the application is expected to be refused by needs a test that the
application is actually refused by it.** [inherited] "The database refused" and
"the ORM tidied up first" render identically.

**A green check over an empty set is worse than no check, because it is
believed.** [inherited] Every static check should walk its subject **and** assert
it found something.

**A predicate nobody satisfies is a predicate nobody has tested.** [inherited] A
guard written before anybody fails it is a guard whose call sites nothing checks.
The journey that first makes it return false has to go back over the call sites
rather than trust that they ask.

**A gate that reports nothing is worse than a gate that reports a failure.**
[inherited] `1 error, 0 tests` looks like nothing to see.

**Verify a guard by mutation.** A test that would pass either way is worse than
no test, because it is counted.

## Silent fallbacks

**Where a value crosses into a namespace you do not control, hand over data with
no surface of its own.** [inherited] A dictionary whose key collides with a method
name renders the bound method — no exception, no log line, no lint warning.

**A lookup that silently falls back to a different namespace is not a lookup you
can trust — and the fallback is what stops you noticing.** [inherited]

**A configuration default that chooses between credentials is a security decision
in disguise.** [inherited] **A setting that selects an identity or a credential
gets no default.**

**A tool that tolerates a bad input gracefully is not a check on that input, and
the graceful handling is what hides the need for one.** [inherited]

**Catching a builtin exception around a call catches everything inside that
call.** [inherited] One exception type per meaning.

## Decide what a layer receives

Not what it displays. The rule generalises downward — to the query, and to the
model.

**A screen cannot leak what it was never handed.** [inherited] Withhold the text,
the count, and the flag saying one exists. "There is no branch that could reveal
it" is a stronger statement than any branch could be.

**Decide what a model can express, and the contradiction becomes unrepresentable
rather than merely untrue.** [inherited]

**Two numbers that can disagree eventually do.** [inherited] Derive the second
from the first.

**Prefer a witness to a boolean.** [inherited] A function returning *the first
date two windows both claim* gives the layer above something to say; one
returning `true` forces it to invent the explanation. Derive the boolean from the
witness, never the reverse, or the caller that needs the value re-derives it.

## Placement and layering

**An import cycle is a placement being wrong, not an obstacle to route around.**
[inherited] Not a local import, not a deferred-typing guard.

**When the misplaced function has to do I/O, split the question from the answer.**
[inherited] Resolve once at the door, read the result everywhere else.

**Logic parked in a route is logic the next journey has to reimplement**, with
nothing structural forcing the two to agree. [inherited]

**A rule reachable only through a route is a rule tested only through a route,
and usually not at all.** [inherited] When a refusal has no test, look at what you
would have to build to reach it — the answer names the layer it is trapped in.

## One spelling of a fact

**A hand-kept list of names is a second spelling of a rule, and the copy is what
goes stale.** [inherited] The fix is a test that the two files which are exactly
connected agree.

**A number in prose about the shape of the code is a claim with no test behind
it.** [inherited] Say what the rule is rather than how many things obey it.

**A comment is not a flag**, and **a comment claiming a route is terminal is not
evidence that it is — the template is.** [inherited]

**A docstring that cites a document is a claim about that document, and nothing
checks it.** [inherited] A link checker that reads only markdown does not read
the links in the code.

**A second query answering a question the first one already answered can disagree
with it.** [inherited]

## Boundaries

**An exogenous file is somebody else's document; what you build from it is
yours.** [inherited] Parse at the edge into your own types. Letting the incoming
shape *be* the model means every upstream change is a change to your domain.

**Give the incoming row and the thing it becomes different names**, or the
collision arrives later as a bug in something unrelated. [inherited]

**Deciding and doing belong in separate functions in separate layers.**
[inherited] It is what makes a preview possible at all — and the unplanned
benefit is that the write can *re-decide* against the world rather than replay a
stale judgement, turning a race into a state that cannot be reached.

**A vendored boundary holds only if something fails the build when it is
breached.** [inherited] The design system is the recurring case: the application
may reference tokens and may not define them, so no literal colour, type, spacing
or radius appears outside the vendored directory — and a static check asserts
both that, and that nothing inside the directory reaches out. A boundary
maintained by everybody remembering is one that two commits eventually breach,
and the breach is invisible because each one looks reasonable on its own.

## Tests and fixtures

**A shortcut past a constructor has to be re-checked whenever the thing it
shortcuts grows an obligation.** [inherited] A fixture that inserts rows by hand
misses what the real path writes precisely because something needed it.

**A failure that only appears when something else is also running looks exactly
like flakiness.** [inherited] "Did not reproduce in three clean runs" is evidence
pointing *at* concurrency, not away from it.

**A cost measured on a fixture is not a cost measured on the thing the fixture
stands in for.** [inherited] Numbers that justify a design decision have to come
from the real scale.

**Real input data earns its place immediately.** [inherited] Invented data is
uniform in the ways real data is not, and the irregularities are the test.

**An assertion written before the code can require schema, and that is the right
direction.** [inherited]

## Changing code that works

**When logic becomes shared, ask what the first caller was handling that the new
ones now are not.** [inherited] Error handling left at the original call site is
invisible in review, because each caller reads correctly on its own.

**A decision that is correct by accident survives until the second case, and then
it is wrong rather than incomplete.** [inherited] Derive rather than add a branch.

**When a rule's subject disappears, the question is not whether to delete the
rule but what the rule was protecting against.** [inherited]

**Renaming a constant to another constant is not parameterising it.** [inherited]
One variable every name derives from is the same work once and none afterwards.

**A blanket text replacement hits homonyms.** [inherited]

## Deploying

**Deploying is where you find out what was never packaged.** [inherited]
Everything else runs from the source tree, where the assets are present whether
or not the build was told to include them.

**Import time is not startup time.** [inherited] A service is a factory, and
nothing at import time touches the outside world.

**Run the simplification pass after the deploy, not before.** [inherited]

**A check that validates a map is not a check that validates the store.**
[inherited] The step that fetches is the step that fails.

## Modelling

**The commit boundary has to be the same size as the side effect.** [inherited] A
loop doing something irreversible — sending mail, calling out — commits per item,
not per pass. What cannot be rolled back must not be inside a transaction that
can be.

**An audit record is not part of the transaction it describes.** [inherited] The
test is whether a rollback leaves the record true. A log written inside the
request that refuses is a log of every permitted access and no refused one —
exactly backwards, and it looks healthy.

**A number somebody typed does not belong in a proof.** [inherited] A policy
limit wired into a feasibility argument stops being a limit and becomes a proof
that the work is impossible. **The tell is that the refusal has no lever in it** —
nobody can act their way out of it, and the person who could fix it is told about
the wrong thing.

**One word must not acquire a third meaning.** [inherited] Recognise the
collision while it is still free to avoid; see [`glossary.md`](glossary.md).

**Provenance does not earn a noun.** [inherited] A thing that arrived by import
and a thing that was typed are the same thing meaning the same thing, so how it
arrived is a field and not vocabulary.

---

## Settled decisions without an ADR

Decided, in force, and too small or too self-evident to have earned their own
record. Anything here that later grows a rejected option worth arguing becomes an
ADR.

| Area | Decision |
|---|---|
| Test order | Outside-in — journey E2E first, red-green-refactor inward |
| | |

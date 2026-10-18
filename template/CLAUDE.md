# CLAUDE.md

Conventions for this repository, loaded every session. **Rules only** — the
reasoning is [`docs/dev-process.md`](docs/dev-process.md), the decisions are
[`docs/adr/`](docs/adr/README.md), what is left to build is
[`docs/roadmap.md`](docs/roadmap.md).

## This project

*Filled in at step 0. It modulates every rule below, which is why it is above
them.*

**Kind:** *(unset — spike · learning · on spec · production)*. The reasoning is
[ADR 0001](docs/adr/0001-what-kind-of-project-this-is.md).

**The bar:** *(one sentence: what this project owes whoever uses it, and what it
does not.)*

**Dials that differ from this kind's defaults**, each with its reason. The dials
and what each kind sets them to are in
[`docs/dev-process.md`](docs/dev-process.md#the-dials-and-what-sets-them). *An
absent row means the default applies — do not infer a dial is off because nothing
mentions it.*

| Dial | Setting here | Why |
|---|---|---|
| | | |

Two things are on at every kind and are not dials: **the named gate**, and
**step 8 in some form**.

## Commands

Four roles, filled by whatever this project chose. The reasoning is
[ADR 0002](docs/adr/0002-tooling-roles.md). *Everything below refers to task
names rather than commands.*

| Role | Tool here |
|---|---|
| Task runner | *(unset)* |
| Toolchain manager | *(unset)* |
| Environment manager | *(unset)* |
| Dependency manager | *(unset)* |

| Task | Runs | Invoke as |
|---|---|---|
| `check` | The fast lane: lint, types, fast tests — while working | *(unset)* |
| `ship` | **The gate**: `check` + the journey E2E + every cross-reference | *(unset)* |
| `fmt` | Format and autofix | *(unset)* |
| `tasks` | Everything available, with descriptions | *(unset)* |

`tasks` is the list. Do not keep a second copy of it here — a hand-kept list of
names is a second spelling of a rule, and the copy is what goes stale.

## 1. You start cold

You have the repository and nothing else. No memory of yesterday's reasoning, no
record of what was tried and abandoned.

- **Context that is not written down does not exist.** A decision made in
  conversation and not committed is gone. Route it (§6) before the session ends.
- Do not relitigate a settled decision. If an ADR covers it, follow it; reopen it
  only when its stated *"reconsider this if"* condition has been met.
- **Load for the session you are in.** Implementing a journey and planning the
  work are different jobs with different context budgets —
  [`docs/README.md`](docs/README.md#two-ways-in) says what each one reads. Do not
  preload the other half.

Orienting for **implementation**: `docs/roadmap.md` for which journey is next →
`docs/handoff/` for a unit already in flight → the journey document → **the
previous journey's end-to-end test** → the source, in dependency order.

That fourth step is not obvious and is worth keeping. To find out what an area
actually settled, its E2E is a better source than its code: it states the
contract in the actor's vocabulary, it is short, and it cannot have drifted from
behaviour without failing.

**The source tree is the only artifact guaranteed current** — it is the
accumulated result of every journey so far. What it does not carry is *why*,
which is the whole argument for docstrings that reason rather than describe.

## 2. Build one journey at a time

A **journey** is one actor completing one goal end to end. Building it means
touching domain, storage, service and interface in one pass.

- Never build a layer across all journeys. Layers that have never met produce all
  their integration problems at once, at the end.
- **Shared modules are libraries, not layers.** Build a cross-cutting rule
  minimally inside the journey that first needs it and let it grow. Pre-build
  nothing.
- A journey that turns out to need a sibling gets a **suffix** (`J4b`, `J4c`),
  never a renumber. Later numbers are already spoken for in the plan and in
  cross-references.

## 3. The failing end-to-end test is the definition of done

- Write it **before** the implementation, from the journey document.
- **Commit it red, in its own commit, and say so in the body.** A discipline that
  is not in the history is one nobody can check afterwards.
- **The E2E is the contract, not a starting point.** Its URLs, labels, button
  text and accessible names are what the implementation must satisfy — not
  suggestions to improve on while building.
- **Select by accessible role and name, never by CSS or internal structure.**
  Tests then survive a restyle, and every control's accessible name becomes
  interface asserted by the suite rather than decoration.
- If the suite reports `N errors, 0 tests`, treat it as a failure. A gate that
  reports nothing is worse than one that reports a failure.

## 4. The journey loop — eight steps, every journey

1. Write the journey document — actor, precondition, steps, outcome, edge cases
2. Write the failing E2E and commit it red. **This is the definition of done**
3. Red-green-refactor inward: domain → storage → service → interface
4. Accessibility assertions inside the same E2E
5. **Commit, then deploy the running system**
6. Simplification pass, then redeploy
7. Update the architecture document; write ADRs for anything significant
8. **Fold what the journey taught into the plan that is left**

Four things here are load-bearing rather than tidy:

- **Commit before deploying.** A release built from a dirty tree names a tree
  that no longer exists, and "what is deployed" becomes unanswerable.
- **Simplify after deploying, not before.** Deploying asks questions the source
  tree cannot: which credential this process actually uses, what is in the
  artifact, what happens on a restart. Those faults are invisible from the code.
- **Deploy every journey, not every release.** The packaging cost of a journey is
  paid by the journey that introduced it.
- **Step 8 asks "what does this make false elsewhere", not "what did we learn".**
  Contradictions with unbuilt work are its most valuable output. **Rewrite** the
  affected parts of the plan; never append a note about what changed. The test of
  a finished step 8: a reader who never saw the previous version cannot tell
  which parts changed.

**Step 5 is about the running system**, and only that. An artifact that is not
the deployed system — a rendered documentation bundle, a paper, a report — is
produced out of band, and its toolchain is deliberately not a release dependency:
a full TeX installation has no business being reachable from the path that ships
code. What that exception must never become is a category the running system can
be put into. If it serves a request, it deploys in the loop.

Two prompts at step 8 that are easy to skip:

**What did this journey change that it did not add?** A journey's diff splits in
two. What it added is the work; what it *changed* in code earlier journeys wrote
is a lesson arriving late — that code was wrong or insufficient and nothing knew
until this journey asked it a question it had to refuse. Those are the
highest-yield design notes available, because they are proven rather than
anticipated. Prefer correcting an earlier journey to building around it.

**What did this journey decide not to do?** Step 6 produces fixes applied and
findings skipped, and only the first lands in a commit. A skipped finding goes to
the roadmap's open items with what was skipped, why, and **the event that would
change the answer** — without that last part it becomes a list nobody re-reads.

Step 8 is the easiest step to skip and the one everything else depends on. Run it.

**A release ends with two units that are not journeys**, once its last journey
has landed:

1. **The clean-up** — the release's clean-up list in
   [`docs/roadmap.md`](docs/roadmap.md), worked as one journey-sized unit. The
   list holds work too small to deserve a journey and belonging to no other one,
   routed there from handoff residue (§7) as the release goes.
2. **The layer pass** — simplification read by layer rather than by journey:
   the surfaces between domain, storage, service and interface, which no single
   journey sees whole. Building a layer across journeys is still wrong (§2);
   *reviewing* one, after the journeys exist, is how the seams get simplified.

Neither writes a new E2E. Every journey's E2E is the contract both must keep
green, unchanged. Each ends the way a journey does — the gate, commit, deploy,
then **step 8**, folding what it found into the plan that is left. The release is
done when the layer pass's step 8 is.

## 5. One named gate, and tasks rather than tools

- **Every repeated command has a name; run the task, not the tool it wraps.**
  Tasks carry the flags, environment and connection strings that make a command
  correct. A hand-built invocation drops them silently — pointing at the wrong
  database, or acting as the wrong role.
- **If a task's flags are wrong, fix the task.** Do not work around it.
- **Nothing passes the gate by weakening it.** Report failures rather than
  routing around them; never relax an assertion, skip a test or widen a tolerance
  to get green.
- **A gate says nothing about what it does not look at.** When you find a gap,
  the fix is usually a task that refuses, not a line in a document.
- **Builds happen in an isolated, locked environment.** A build that depends on
  what is installed on the machine is reproducible by accident.

## 6. Where a thing goes — ask in this order

1. Architecturally significant — expensive to reverse, or constrains later
   choices? → an **ADR**, including its *"reconsider this if"*
2. A rule worth having in hand before writing similar code? →
   [`docs/design-notes.md`](docs/design-notes.md)
3. A word, or a word you nearly used? → [`docs/glossary.md`](docs/glossary.md).
   Record rejected names with their reason, or they get re-proposed within a week
4. Changes what is left to build? → [`docs/roadmap.md`](docs/roadmap.md), by
   rewriting it. Work too small for a journey and belonging to none goes on the
   current release's clean-up list there
5. Must change how the next change is made? → **this file**
6. Belongs to somebody who knows the business rather than the code? →
   [`docs/stakeholder-questions.md`](docs/stakeholder-questions.md)
7. Fits none of the above, and you are not ready to throw it away? →
   [`docs/inbox/`](docs/inbox/README.md), which is a holding area and not a home

**History is `git log`.** No committed document is a record of what used to be
true. A *generated* narrative of the history is fine, because it is rebuilt
rather than maintained — see the `history` task.

Capture insight where it happens with a `Lesson:` commit trailer. The trailer is
a capture aid, **not** the record — the record is the ADR, the design note or the
plan. A lesson that appears twice in different words is a rule that was never
written.

## 7. The handoff, and the residue test

The handoff is the register of what is not yet done or not yet routed.
**Shrinking it to nothing is the objective of the unit of work**, not a check
applied at the end. A journey is finished when its handoff is empty, and the file
is then deleted because there is nothing in it — rather than deleted in order to
declare it finished.

**Whatever is in it that is not already somewhere is, by definition, something
with no home.** Work it as a loop:

> **Take one signal → handle it → remove the item that raised it → take the
> next.** Repeat until no signals remain.

**Removing the item is what proves it was handled.** An entry routed but left in
place is indistinguishable from one nobody has looked at, and it costs the same
attention again on the next read. Handling depends on the kind:

- **Knowledge** → route it (§6), then delete the line. The handoff caught a miss.
- **Work too small for a journey**, and belonging to no other one → the
  release's clean-up list (§4), then delete the line.
- **Checkable state** → a document is the wrong fix. Make a task refuse, then
  delete the line.
- **Neither** → **stop, and treat it as a process finding.** A document is
  missing a job or a category is wrong. Log it in
  [`docs/experiments.md`](docs/experiments.md) and raise it *before* deleting the
  line — this is the one signal about the process that arrives without anybody
  going looking for it.

**Expect the loop to lengthen before it shortens.** Handling one signal routinely
surfaces another, which is why the exit condition is *no signals remain* rather
than a number of passes — and why emptying the register by filing things where
they do not belong defeats the exercise while looking like progress.

## 8. Engineering rules

The full set, with the evidence, is
[`docs/design-notes.md`](docs/design-notes.md). These are the ones that change
what you write today:

- **Make the door refuse.** Where a rule must hold at every call site, find the
  one door the value comes through and enforce it there. A rule maintained by
  every caller remembering is one that two callers eventually forget.
- **Give every structural rule a static half and a runtime half.** A runtime
  guard only fires on a path some test takes; a static check reads every call
  site. Neither is redundant. Verify both by mutation.
- **A threshold nothing measures only gets crossed.** A number in prose — module
  size, coverage, latency — is not a check. Make it one.
- **Use the real dependency when its constraints are the point.** A faster
  in-memory substitute is not testing the constraint you chose the real one for.
- **Capture real input data early.** Invented data is uniform in the ways real
  data is not, and the irregularities are the test.
- **Write the reasoning where the thing is.** Docstrings carry *why*, not *what*.
- **Scope shared local resources by one explicit instance name**, so parallel
  checkouts cannot destroy each other's state.

## 9. Working style

- Report what actually happened: failing tests with their output, steps skipped,
  scope left undone and why.
- **A genuinely undecided question that rises to a design decision is not for
  guessing.** Stop and present the alternatives with their trade-offs and
  implications, and start a conversation. Those alternatives are already an ADR's
  *Options considered*, so the conversation produces the record rather than
  preceding it — and a decision taken in conversation and not written down is
  gone by the next session.
- Below that line, decide. State the assumption, continue, and flag it.
- Ask before anything outward-facing — deploying, publishing, anything hard to
  reverse.
- Extend the conventions when they run out. Add the task rather than running the
  command twice by hand; write the comment explaining the flag that caught you
  out.

## 10. This codebase

*Everything above is the method. What follows is this repository, and it is empty
until there is something true to put in it. Keep it to what has to be in hand
before touching code — the shape, the directions, the refusals.*

**Layout and import direction.** *(which directory holds pure logic, which way
imports flow, what may not import what.)*

**Configuration and secrets.** *(where values come from, what has no default,
what must never be committed.)*

**Ask before.** *(structural moves, file renames, schema changes.)*

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
[`docs/dev-process.md`](docs/dev-process.md#the-dials-and-what-sets-them). An
absent row means the default applies.

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

`tasks` is the list; ask it rather than keeping a copy here.

## 1. You start cold

You have the repository and nothing else.

- **Context that is not written down does not exist.** Route every decision
  (§6) before the session ends.
- **A settled decision stays settled.** Follow the ADR that covers it; reopen it
  only when its *"reconsider this if"* condition has been met.
- **Load for the session you are in** — implementing or planning.
  [`docs/README.md`](docs/README.md#two-ways-in) says what each one reads.

Orienting for **implementation**: `docs/roadmap.md` for which journey is next →
`docs/handoff/` for a unit already in flight → the journey document → **the
previous journey's end-to-end test**, the shortest true statement of what an area
settled → the source, in dependency order.

## 2. Build one journey at a time

A **journey** is one actor completing one goal end to end. Build it through
domain, storage, service and interface in one pass.

- **Each journey crosses every layer.** Layers built across all journeys meet for
  the first time at the end.
- **Shared modules are libraries, not layers.** Build a cross-cutting rule
  minimally inside the journey that first needs it, and let it grow.
- A journey that turns out to need a sibling gets a **suffix** (`J4b`, `J4c`).
  Numbers are permanent.

## 3. The failing end-to-end test is the definition of done

- Write it **before** the implementation, from the journey document.
- **Commit it red, in its own commit, and say so in the body.**
- **The E2E is the contract.** Its URLs, labels, button text and accessible
  names are what the implementation must satisfy, as written.
- **Select by accessible role and name.** CSS and internal structure are not
  selectors.
- `N errors, 0 tests` is a failure.

## 4. The journey loop — eight steps, every journey

1. Write the journey document — actor, precondition, steps, outcome, edge cases
2. Write the failing E2E and commit it red. **This is the definition of done**
3. Red-green-refactor inward: domain → storage → service → interface
4. Accessibility assertions inside the same E2E
5. **Commit, then deploy the running system**
6. Simplification pass, then redeploy
7. Update the architecture document; write ADRs for anything significant
8. **Fold what the journey taught into the plan that is left** — the `step-8`
   skill. Run it every journey.

The order is deliberate: commit before deploying, simplify after deploying, and
deploy every journey rather than every release. Step 5 covers the running
system; a documentation bundle, paper or report is built out of band. Why, with
the evidence: [`docs/dev-process.md`](docs/dev-process.md#4-the-journey-loop).

**A release ends with two units that are not journeys**, once its last journey
has landed:

1. **The clean-up** — the release's clean-up list in
   [`docs/roadmap.md`](docs/roadmap.md), worked as one journey-sized unit.
2. **The layer pass** — simplification read by layer: the surfaces between
   domain, storage, service and interface. *Reviewing* a layer once the journeys
   exist is how the seams get simplified; building one stays wrong (§2).

Neither writes a new E2E; every existing E2E stays green, unchanged. Each ends
the way a journey does — the gate, commit, deploy, then **step 8**. The release
is done when the layer pass's step 8 is.

## 5. One named gate, and tasks rather than tools

- **Every repeated command has a name; run the task, not the tool it wraps.**
  Tasks carry the flags, environment and connection strings that make a command
  correct.
- **If a task's flags are wrong, fix the task.**
- **The gate only gets stronger.** Report a failure as a failure; assertions,
  tests and tolerances stay as they are to reach green.
- **A gate says nothing about what it does not look at.** Close a gap with a task
  that refuses, not a line in a document.
- **Builds happen in an isolated, locked environment.**

## 6. Where a thing goes — ask in this order

1. Architecturally significant — expensive to reverse, or constrains later
   choices? → an **ADR**, including its *"reconsider this if"*
2. A rule worth having in hand before writing similar code? →
   [`docs/design-notes.md`](docs/design-notes.md)
3. A word, or a word you nearly used? → [`docs/glossary.md`](docs/glossary.md),
   rejected names included, with their reason
4. Changes what is left to build? → [`docs/roadmap.md`](docs/roadmap.md), by
   rewriting it. Work too small for a journey and belonging to none goes on the
   current release's clean-up list there
5. Must change how the next change is made? → **this file**
6. Belongs to somebody who knows the business rather than the code? →
   [`docs/stakeholder-questions.md`](docs/stakeholder-questions.md)
7. Fits none of the above, and you are not ready to throw it away? →
   [`docs/inbox/`](docs/inbox/README.md), a holding area rather than a home

**History is `git log`.** Committed documents say what is true now. A
*generated* narrative of the history is fine — see the `history` task.

Capture insight where it happens with a `Lesson:` commit trailer; the record is
the ADR, the design note or the plan it gets routed to. A lesson that appears
twice in different words is a rule that was never written.

## 7. The handoff, and the residue loop

The handoff is the register of what is not yet done or not yet routed.
**Shrinking it to nothing is the objective of the unit of work.** The file is
deleted once it is empty, and only then.

Whatever is in it that is not already somewhere is **residue**. Work it as a
loop:

> **Take one signal → handle it → remove the item that raised it → take the
> next.** Repeat until no signals remain.

**The deletion is the receipt.** Handling depends on the kind:

- **Knowledge** → route it (§6), then delete the line.
- **Work too small for a journey**, and belonging to no other one → the
  release's clean-up list (§4), then delete the line.
- **Checkable state** → make a task refuse, then delete the line.
- **Neither** → **stop: it is a process finding.** Log it in
  [`docs/experiments.md`](docs/experiments.md) and raise it with the user
  *before* deleting the line.

Expect the loop to lengthen before it shortens; the exit is *no signals remain*.

## 8. Engineering rules

The full set, with the evidence, is
[`docs/design-notes.md`](docs/design-notes.md). These change what you write
today:

- **Make the door refuse.** Where a rule must hold at every call site, enforce it
  at the one door the value comes through.
- **Give every structural rule a static half and a runtime half**, and verify
  both by mutation.
- **A threshold nothing measures only gets crossed.** Make a number in prose —
  module size, coverage, latency — a check.
- **Use the real dependency when its constraints are the point.**
- **Capture real input data early.** Its irregularities are the test.
- **Write the reasoning where the thing is.** Docstrings carry *why*, not *what*.
- **Scope shared local resources by one explicit instance name**, so parallel
  checkouts keep their own state.

## 9. Working style

- Report what actually happened: failing tests with their output, steps skipped,
  scope left undone and why.
- **A genuinely undecided question that rises to a design decision goes to the
  user.** Present the alternatives with their trade-offs — they are the ADR's
  *Options considered* — and write the ADR from the conversation.
- Below that line, decide: state the assumption, continue, and flag it.
- Ask before anything outward-facing — deploying, publishing, anything hard to
  reverse.
- **Extend the conventions when they run out.** Add the task rather than running
  the command twice by hand; comment the flag that caught you out.

## 10. This codebase

*Everything above is the method. What follows is this repository, and it is empty
until there is something true to put in it. Keep it to what has to be in hand
before touching code — the shape, the directions, the refusals.*

**Layout and import direction.** *(which directory holds pure logic, which way
imports flow, what may not import what.)*

**Configuration and secrets.** *(where values come from, what has no default,
what must never be committed.)*

**Ask before.** *(structural moves, file renames, schema changes.)*

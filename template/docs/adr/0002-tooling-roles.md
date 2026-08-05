# ADR 0002: What fills the four tool roles, and what the gate covers

- **Status:** proposed
- **Date:** YYYY-MM-DD
- **Supersedes:** —
- **Superseded by:** —

*Written at step 0, after [ADR 0001](0001-what-kind-of-project-this-is.md) — the
kind of project sets how much rigour these roles need. The Problem and the
requirements are the method's; the Options and Decision are this project's.*

## Problem

The method depends on four jobs being done and does not care what does them. What
it does care about is that each is done by *something named*, because the
alternative in every case is a hand-built command that is correct on one machine.

| Role | Has to provide |
|---|---|
| **Task runner** | A name for every repeated command, carrying the flags, variables and connection strings that make it correct |
| **Toolchain manager** | Pinned versions of the tools themselves, so two checkouts build the same way |
| **Environment manager** | Per-environment configuration supplied to a command — connection strings, profiles, secret paths |
| **Dependency manager** | Resolved, locked dependencies in an isolated environment, so a build does not depend on what is installed on the machine |

One tool may fill several. What matters is that none of them is *nobody*.

Three requirements come with the roles and do not vary by project:

**Run the task, not the tool it wraps.** A test runner invoked by hand points at
whatever database the shell was holding; a migration tool invoked by hand runs as
whatever role the shell was holding. The task carries what makes the command
correct and a hand-built invocation drops it silently. It also costs fewer
retries, which matters when an agent is running the commands.

**If a task's flags are wrong, fix the task.** Working around it puts a second
spelling of the command in somebody's shell history, where nothing reviews it.

**Builds resolve against a lockfile in an isolated environment.** A build that
works because of what is installed globally is reproducible by accident, and it
stops being reproducible on the day the machine changes rather than the code.

## Options considered

### A. *(what this project chose)*

**For:**

**Against:**

### B. *(the serious alternative)*

**For:**

**Against:**

## Decision

*(What fills each role, and why. Where a house default was taken unchanged, say
so in one line and cite it rather than restating the reasoning. Record the actual
invocations in the table at the top of
[`../../CLAUDE.md`](../../CLAUDE.md#commands) — this document is the reasoning,
that table is the reference.)*

### What the gate covers

`ship` is the definition of done and means nothing if anything is allowed past
it. At minimum:

| Covers | Because |
|---|---|
| Lint and type checks | The cheap half, and the half skipped by hand |
| The fast test lane | The logic, without the slow dependencies |
| **The journey end-to-end tests** | The definition of done for the unit of work |
| Documentation cross-references | A renamed file breaks links silently; a link checker is the only reader that notices |
| Schema or contract drift | Wherever the code's model of a thing and the thing itself can disagree |

`check` is the subset that runs while working: the above minus anything needing a
browser or a built artifact.

**A gate says nothing about what it does not look at.** Anything outside its
reach is a gap to close with a task that refuses, not a line in a document — and
the gaps are found by asking, of each failure that gets through, which task
should have caught it.

## Reconsider this if

- A role is being filled by two tools that disagree, which is the state this
  record exists to prevent
- The gate is slow enough that people run the subset and ship on that
- A second environment appears that the environment manager cannot express
  without duplicating configuration
- The build stops working on a machine that has never built it before
- [ADR 0001](0001-what-kind-of-project-this-is.md) changes — a promotion from
  spike to production is exactly when the missing roles start costing

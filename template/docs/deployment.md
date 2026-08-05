# Deployment

*Conditional — delete this file unless there is somewhere to deploy.*

The procedure, the environments, and the runbook. **The shape and the reasoning
behind it belong in an ADR**; this document is what somebody does.

**Say what is real.** An environment the scripts support but nobody has deployed
to is not a working deploy — a deploy task nobody has run is a deploy task that
does not work. Name which environments are real and which are aspirational, at
the top, where somebody about to rely on one will read it.

## Environments

| Environment | Data | Configuration | Purpose |
|---|---|---|---|
| | | | |

*Configuration should be driven by one variable per concern, so that one task
definition serves a local socket, a CI container and a remote host without
branching. Nothing in the application should know which environment it got.*

*Where deployed values come from is one seam and the application should not be
able to see it — see the secrets prior in the toolchain default. A committed map
holding paths and no values is what makes moving to a different store a change to
one block rather than to every script.*

## Local setup

*The shortest path from a clone to a running system, and — importantly — how many
privileged steps it takes. If the answer is more than zero, say which and why,
because that is the number somebody will be surprised by.*

## Setting up a new environment

*Once per environment, and deliberately **not** something the deploy does:
provisioning and releasing are different activities with different blast radii. A
deploy script that provisions is a deploy script that will provision production
one day.*

## Releasing

*The steps, in order, and why the order is the design. The ones that recur:*

- **Preflight first.** Everything knowable before anything changes. A deploy that
  fails halfway is the expensive kind.
- **Build the artifact**, which is also what proves that everything needed is
  *in* it — assets and migration scripts are present in a source tree whether or
  not the build was told to include them.
- **Migrate as a separate step, with different credentials**, where there is
  anything to migrate.
- **Activate atomically**, and record what was there before.
- **Health check, and roll back on failure.** The health check has to compare
  something the artifact knows against something the deployed state reports —
  otherwise it confirms only that a process started, and a migration pointed at
  the wrong target exits zero.

*Prune old releases **after** the health check. A release directory deleted while
it is still the rollback target is a rollback that cannot happen.*

## Rolling back

*What it does, what it deliberately does not do, and what is not reversible.*

*A rollback should need nothing it does not already have on disk — no build, no
network — because those are the two things least likely to work at the moment a
rollback is happening. **A failed rollback should change nothing.***

*State plainly whether data or schema is rolled back. Usually it is not, and the
discipline that makes that safe is forward-compatible migrations: add before
writing, drop a release after the code stopped reading.*

---

# Runbook

*One section per thing that goes wrong, written to be read at 3am by somebody
who did not build it. Start with the signal, not the cause.*

**Leave a section empty until it has been rehearsed, and say so.** A procedure
nobody has run is fiction, and fiction in a runbook is worse than a gap because
somebody will follow it. Backups in particular are verified by restoring them,
not by a job that reports success.

## *(A failed deploy)*

## *(It is slow)*

*Name which measurements trend with load and which have a hard budget — for the
first, only the trend means anything; for the second, a single value does.*

## *(Still to be written at first production deploy)*

-

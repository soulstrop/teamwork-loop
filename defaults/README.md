# Defaults

Standing priors, brought to a project rather than decided by it. These are an
**input to step 0** and are deliberately not copied into
[`../template/`](../template/): a default copied into every repository becomes a
second spelling of a decision the ADRs already hold, and it goes stale per
project while looking authoritative.

## How they are used

At step 0, each default is either taken or departed from, and the project's ADR
records which in one line:

> **Decision.** House default unchanged: mise for tasks, toolchain and
> environment; uv for dependencies. See [`defaults/toolchain.md`].

> **Decision.** Departed from the storage default. The ladder puts this at
> SQLite; it is Postgres here because two processes write concurrently and the
> non-overlap constraint is the product.

**A default is a prior, not a policy.** Departing from one is ordinary and costs
a sentence. What is not ordinary is departing silently — the next reader cannot
tell a considered departure from an accident, and neither can you in four months.

## What is here

| Default | Covers | State |
|---|---|---|
| [`toolchain.md`](toolchain.md) | The four tool roles, secrets, and what the priors are | written |
| [`storage.md`](storage.md) | Exogenous formats, TOML, and a ladder to a specialised store | written |
| [`language.md`](language.md) | What picks a language, and what overrides the prior | **to be filled in** |
| [`design-system.md`](design-system.md) | The house style, the token boundary, and contributing back | written |

## Adding one

A prior earns a place here when it has been the answer on more than one project
*and* would otherwise be re-derived from scratch. Everything else is a project
decision that happens to have been made the same way twice.

Each entry states the prior, the reason behind it, and — the part that matters —
**what would make it wrong**. A default with no stated failure condition is
indistinguishable from a habit, and habits are what a cold reader has no way to
question.

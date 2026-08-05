# *(Project name)*

*One or two sentences: what this is and what it does. Written for somebody who
arrived from a link and knows nothing — this is the landing page.*

*This is an **output**. It stands alone and may restate what the rest of the set
holds elsewhere, because its reader will not follow a link to find out what the
system is for.*

## What it does

*The domain, in the domain's language. What problem this solves, and the shape of
the solution — enough that a reader can tell whether it is the kind of thing they
were looking for.*

*If the interesting part is an algorithm, a policy or a rule that makes the
system non-obvious, this is where to describe it. Not how it is implemented —
what it decides, and why that is the hard part.*

## Who uses it

| Role | What they do |
|---|---|
| | |

## Getting started

*Prerequisites, then the shortest path from a fresh clone to something running.
Every command a named task — see [ADR 0002](docs/adr/0002-tooling-roles.md).*

```
```

### Common tasks

*The few worth knowing by name, and no more. A hand-kept copy of the full task
list is the copy that goes stale — point at the task runner's own listing
instead.*

```
check    the fast lane, while working
ship     the gate: what has to be green
fmt      format and autofix
```

## Layout

*A short tree with a line per top-level directory. The detailed version is
[`docs/architecture.md`](docs/architecture.md); this is orientation.*

```
```

## Documentation

Everything is under [`docs/`](docs/README.md), which indexes the set and says
what each document is **for** — the roadmap is what is left to build, the ADRs
are why things are the way they are, the journeys are what each unit of work must
do.

Development proceeds one journey at a time rather than one layer at a time. Each
journey starts with a failing end-to-end test that defines done, and ends by
folding what it taught back into the plan — the loop is in
[`CLAUDE.md`](CLAUDE.md) and the reasoning behind the method is
[`docs/dev-process.md`](docs/dev-process.md).

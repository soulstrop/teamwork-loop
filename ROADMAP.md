# Roadmap

## Where we are

`main` is the roadmap-and-handoff method. Recording the process version in
generated projects and tagging it are what stand between `main` and **1.0**.
**2.0** turns the issue tracker into a fifth tool role — bring your own, with
beads as the default — and is not started.

This document is what is left to build *for the framework itself*. The roadmap a
project gets is [`template/docs/roadmap.md`](template/docs/roadmap.md), and this
one borrows its shape.

## Release 1.0 — the roadmap-and-handoff method, released

Work is tracked in markdown: `roadmap.md` holds the journey inventory and open
items, and a per-journey handoff holds the burn-down. No tracker is required.

| # | Item | State |
|---|---|---|
| 1.1 | **Move `routing-and-sweep-spec.md` out of the template** to `design/2.0/`, and drop its references in `template/docs/README.md`, `template/docs/dev-process.md` and `USING-THIS-FRAMEWORK.md` | done |
| 1.2 | **Record the process version in generated projects** — a `Process: 1.0` line in the template's `CLAUDE.md`, written by `teamwork-init` and covered by `verify` | next |
| 1.3 | **Tag `v1.0`** once the tool's tests and `verify` are green | |
| 1.4 | **End each release with a clean-up and a layer pass** — a clean-up list in the roadmap for residue too small for a journey, worked as one unit after the last journey; then simplification by layer; each closed by step 8 | done |

1.4 came in after 1.3 was numbered, from a process finding; numbers do not move,
so it is listed last but lands before the tag.

## Release 2.0 — bring your own issue tracker, beads by default

Work-item state moves out of markdown and into a tracker; specifications and
reasoning stay in markdown. Documents name tracker operations as task names, the
way they already name commands, so the tracker can change without a rewrite.

| # | Item | Depends on |
|---|---|---|
| 2.1 | **The tracker contract** — the issue tracker as a fifth role in ADR 0002, with the capabilities any tracker must provide: stable citable IDs, parent and child, dependencies with a ready query, deferral carrying *what would change the answer*, notes, cheap cold-session access, and optionally export | — |
| 2.2 | **Reword the axiom** to *context not reachable from the repository does not exist*, wherever it is stated or argued from, and say in the release notes that this loosens it | 2.1 |
| 2.3 | **Tracker task names** — the vocabulary documents use (`ready`, `file`, `defer`, `note`, `close`, …) and where it is defined | 2.1 |
| 2.4 | **The beads adapter** — task names mapped to `bd`, how it meets the contract, and the JSONL export committed with a gate check that it is current | 2.3, decision A |
| 2.5 | **Journeys as epics; the handoff retired** — the burn-down becomes child items, residue goes in notes on the journey epic, and step 8 runs the residue test over those notes. The release's clean-up list becomes child items of a clean-up epic, and the layer pass an epic of its own | 2.3 |
| 2.6 | **Open items become tracker deferrals** — a dependency where the trigger is another item, a condition plus a sweep step where it is a metric or an outside event | 2.3 |
| 2.7 | **The roadmap shrinks** to *where we are* and each release's goal, with the journey tables generated from the tracker | 2.4, decision B |
| 2.8 | **`teamwork-init` asks for the tracker** and renders its adapter into the project | 2.4 |
| 2.9 | **A second adapter**, rough is enough — the test of whether the contract is right | 2.4, decision C |
| 2.10 | **Five roles, not four**, in `USING-THIS-FRAMEWORK.md` and `README.md` | 2.1 |
| 2.11 | **Migration guide, 1.0 to 2.0** | 2.5, 2.6, 2.7 |

**Ordering.** 2.1 comes first because every other item is written against the
contract. 2.9 comes before release, not after: a role with one implementation is
a guess, and the contract should be corrected while nothing depends on it.

**Sources.** [`design/2.0/routing-and-sweep-spec.md`](design/2.0/routing-and-sweep-spec.md)
is an earlier draft of a beads integration. Its commands and schema predate the
real `bd`, so it is a source of ideas, not a specification. What to draw from it:

- for 2.1, the split of specifications in markdown and state in the tracker, and
  its matrix of which granularity lives where;
- for 2.3, its taxonomy of scale and context, as a starting point for the task
  vocabulary;
- for 2.6, its explicit trigger types and the intake sweep, which answer the
  missing condition triggers noted under open items.

## Decisions open

Each carries the event that would settle it.

- **A. How beads state reaches the repository.** Commit the JSONL export as the
  record, with Dolt as the working copy and the gate refusing when they disagree;
  or treat a Dolt remote as the source of truth. *Leaning: commit the export*,
  because it keeps the strict 1.0 axiom true for beads projects. **What would
  change the answer:** the export proving unreliable as a restore path, or
  `bd init --from-jsonl` losing anything the method relies on.
- **B. How much of the roadmap is generated.** Prose with generated tables, or
  wholly generated, or dropped in favour of the tracker's own views. *Leaning:
  prose plus generated tables*, since *where we are* is writing, not data.
  **What would change the answer:** drafting 2.7 and finding the prose has
  nothing left to say.
- **C. Which tracker is the second adapter.** Jira matches the stated motive,
  people already invested in a tracker; GitHub Issues is free to test and close
  to hand. **What would change the answer:** someone with a Jira project willing
  to try it.

## Open items, not blocking

- **The CLA check is not yet required on `main`** — *found 2026-10-17, after the
  CLA landed.* GitHub only offers it as a required check after the workflow has
  run once. **What would change the answer:** the first pull request from another
  account.
- **The README's "Who it is for" paragraph is inferred** — *written 2026-10-17
  from the existing docs, not from the author.* **What would change the answer:**
  the author rewriting it, or confirming it.
- **GitHub will not detect the licence** — *2026-10-17.* Three licences by path
  read as "Other". `LICENSE.md` is authoritative and this is cosmetic. **What
  would change the answer:** a contributor or user being put off by it.
- **beads has no native condition triggers** — *found 2026-10-17 while mapping
  open items to beads.* `bd defer` takes only a date, so a trigger such as *table
  exceeds 50,000 rows* needs a convention. Folded into 2.6. **What would change
  the answer:** a `bd` release that adds them.

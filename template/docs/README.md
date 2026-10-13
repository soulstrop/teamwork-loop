# Documentation

Each document has one job, and they cross-reference rather than repeat. A link
checker should resolve every relative link and heading anchor across the set, so
a renamed file cannot break them silently — that check belongs in the `ship`
task, because a cross-reference nothing verifies is a cross-reference that is
already wrong somewhere.

## Two ways in

The set serves two kinds of session, and reading the wrong half fills a context
window with material that will not be used.

| | **Planning** | **Implementation** |
|---|---|---|
| Answers | What to build, in what order, and what is undecided | Build this one journey |
| Scale | Meso and macro | Micro |
| Reads | [`roadmap.md`](roadmap.md), [`journeys/README.md`](journeys/README.md), [`architecture.md`](architecture.md), the [ADR index](adr/README.md), the inboxes | [`../CLAUDE.md`](../CLAUDE.md), one journey document, the previous journey's E2E, [`design-notes.md`](design-notes.md), [`glossary.md`](glossary.md), [`handoff/`](handoff/README.md) |
| Omits | Handoffs, journey detail, the rules for writing code | The rest of the roadmap, other journeys, the inboxes, the experiment menu |
| Produces | A rewritten plan, ADRs, journey documents | A journey, through the eight-step loop |

**Pointers rather than content is what makes this work.** An implementation
session starts from one journey document and must be able to reach anything else
it turns out to need — which is why journey documents *cite* rules rather than
restating them, and why the roadmap names a journey rather than describing it.
The measure of this set is not how much it holds. It is how little has to be
loaded before work can start, and how reliably the rest can be found from there.

## The set

| Document | Contains | Explicitly does not contain | Mode |
|---|---|---|---|
| [`../README.md`](../README.md) | What the system is, who uses it, how to get running | Design rationale, journey detail | output |
| [`../CLAUDE.md`](../CLAUDE.md) | The conventions and the loop, as rules | Reasoning, and anything a person would not also want | both |
| [`roadmap.md`](roadmap.md) | **What is left to build.** Inventory, releases, open items | History, rationale, anything already done | planning |
| [`journeys/`](journeys/README.md) | One file per journey: actor, precondition, steps, outcome, edge cases | Architecture, interface specifics, rationale | both |
| [`architecture.md`](architecture.md) | Components, responsibilities, layout, how they relate | Decision rationale — that lives in ADRs | planning |
| [`adr/`](adr/README.md) | One architecturally significant decision each | Anything not architecturally significant | planning |
| [`design-notes.md`](design-notes.md) | Rules learned by getting them wrong, and settled decisions too small for an ADR | Narrative, and anything that is already an ADR | implementation |
| [`glossary.md`](glossary.md) | What each word means in which context, and the names rejected | Anything that is not a word used here | implementation |
| [`handoff/`](handoff/README.md) | The current unit's micro-state, for a resume that starts from zero | Anything durable — that gets routed instead | implementation |
| [`dev-process.md`](dev-process.md) | **How the work is done**, and the evidence for each claim | Anything specific to this system | process |
| [`routing-and-sweep-spec.md`](routing-and-sweep-spec.md) | **Routing pipeline, TODO taxonomy, sweep procedure, dependencies & triggers** | Issue tracker implementation details | process |
| [`experiments.md`](experiments.md) | Investigations into the process. **A menu, not a backlog** | Conclusions, which route into `dev-process.md` | process |
| [`stakeholder-questions.md`](stakeholder-questions.md) | Decisions taken provisionally that belong to somebody who knows the business | Anything an engineer can settle alone | output |
| [`inbox/`](inbox/README.md) | Unrouted ideas, held rather than filed | Anything that has a home | planning |
| [`references/`](references/README.md) | External material, and which decision each informs | Our own reasoning | planning |
| [`history.md`](history.md) | A narrative rollup of the log. **Generated, never edited** | Anything not derivable from `git log` | generated |

**Conditional — delete unless the project has the thing.** Each earns its place
by a condition rather than by seeming prudent, and several of those conditions
are also escalation triggers in
[ADR 0001](adr/0001-what-kind-of-project-this-is.md).

| Document | Earns its place when |
|---|---|
| [`deployment.md`](deployment.md) | There is somewhere to deploy, and a runbook somebody will need at 3am |
| [`data.md`](data.md) | Somebody who did not write the code has to look after the store |
| [`security.md`](security.md) | There is a credential worth stealing, personal data, money, or untrusted input |
| [`observability.md`](observability.md) | Something runs somewhere nobody is watching it |
| [`auditability.md`](auditability.md) | Somebody will ask *who did this*, or an obligation says a record must exist |
| [`diagnostics.md`](diagnostics.md) | Somebody who is not a developer will report a problem |
| [`backups.md`](backups.md) | There is data that cannot be regenerated |
| [`ui-brief.md`](ui-brief.md) | Design is done by somebody who is not implementing it |
| [`demo.md`](demo.md) | The work has to be shown to a room |

**Five of those sit close together and are deliberately separate**, because they
answer different questions and have different readers:

| | Asks | Reader |
|---|---|---|
| `security.md` | What are we protecting, from whom, and what have we chosen not to defend? | Whoever is about to widen a boundary |
| `observability.md` | Is it healthy, and would this signal change a decision? | Whoever is adding a measurement |
| `auditability.md` | Who did what, and what obligation says we must know? | Whoever is asked to account for something |
| `diagnostics.md` | What led to this moment, and can it be reproduced? | Whoever is handed a user's complaint |
| `backups.md` | What happens when we lose it, and has the restore been rehearsed? | Whoever is having the worst day |

**Three of them capture data at runtime and the mechanisms overlap.** What keeps
them apart is retention: telemetry expires on a clock, audit on a policy, and a
diagnostic capture **when the problem it explains is closed** — the only one tied
to a work item rather than to time. `diagnostics.md` holds that comparison.

## Where a thing goes

The routing question is in [`../CLAUDE.md`](../CLAUDE.md#6-where-a-thing-goes--ask-in-this-order),
because it has to be in hand at the moment something is learned rather than
looked up afterwards. This file is the map; that is the rule.

**History is `git log`.** No committed document records what used to be true. A
lesson worth carrying forward is captured with a `Lesson:` trailer at the moment
of insight and then *routed* — the trailer is the capture aid and the ADR, design
note or plan is the record.

**Generated documents are the exception**, and they are exempt because they
cannot drift: [`history.md`](history.md) is rebuilt from the log by the `history`
task and edited by nobody. That is what makes a narrative history compatible with
the rule above rather than a violation of it.

## Not in the set

`handoff/` is working state. It is deleted when the journey ships, and an empty
one is the test that the journey finished — so it is the one place a durable
finding must never be left. See [`handoff/README.md`](handoff/README.md).

`inbox/` is a holding area with an expiry: an entry either gets routed or gets
deleted. It exists so that "not yet filed" is a visible state rather than a file
somebody dropped in `docs/`.

## Keeping this map honest

Add a row when a document is added, and delete the row and the file together. A
document whose row says one job while the file does another is the failure this
table exists to prevent — and the version that is wrong is always the one nobody
re-reads.

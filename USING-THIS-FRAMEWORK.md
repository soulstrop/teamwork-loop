# Using this framework

A document set for building software one journey at a time, with a collaborator
that starts every session cold. Copy [`template/`](template/) into a new
repository and it is the initial version: enough context for an agent or a new
human to know where the project is, what is next, and how the work is done here —
before a line of the project's own code exists.

**On where this comes from.** The method is not one project's invention. It
evolved across several, and this set of documents is the generalisation of it.
What *is* one project is the evidence: the failures cited in
[`dev-process.md`](template/docs/dev-process.md) and
[`design-notes.md`](template/docs/design-notes.md) come mostly from the latest
and fullest expression of the method, because that is the project that recorded
them. So a rule stated plainly has usually been paid for more than once; a rule
stated *with a citation* has been paid for at least once in a way somebody wrote
down. Neither is validated across projects in a way that would survive a sceptic,
which is what the next project is for.

## Three layers

| Layer | What it is | Copied into the project? |
|---|---|---|
| [`defaults/`](defaults/README.md) | Standing priors brought to a project rather than decided by it | **No** — read at step 0, cited by the ADRs |
| [`template/`](template/) | The document set at its initial version | Yes, wholesale |
| The project | What the set grows into as journeys land | — |

**Defaults are not copied**, and that is deliberate. A default copied into every
repository becomes a second spelling of a decision the ADRs already hold, and it
goes stale per project while continuing to look authoritative. The project's ADR
cites it in one line instead: *house default unchanged*, or *departed, because —*.

## The two rules the set obeys

**Information is not repeated; documents cross-reference instead.** One fact has
one home. A second spelling is the copy that goes stale, and nothing tells you
which one is wrong.

**Except in outputs.** [`README.md`](template/README.md),
[`demo.md`](template/docs/demo.md), [`data.md`](template/docs/data.md),
[`ui-brief.md`](template/docs/ui-brief.md) and
[`stakeholder-questions.md`](template/docs/stakeholder-questions.md) are written
for an audience that will not follow a link — a reader on GitHub, a room being
demonstrated to, whoever looks after the database, a designer, a stakeholder.
They stand alone and may restate. Everything else links.

**A third kind is generated**, and it is exempt from both rules because it cannot
drift: [`history.md`](template/docs/history.md), a rendered bundle, an extracted
list of lessons. A generated document is rebuilt from its source of truth and
**never edited**. That is what makes a narrative history compatible with *history
is `git log`* — the log stays authoritative and the narrative is a render of it.

## Two ways in, and two context budgets

The set serves two kinds of session, and loading the wrong half fills a context
window with material that will not be used.

| | **Planning** | **Implementation** |
|---|---|---|
| Answers | What to build, in what order, and what is undecided | Build this one journey |
| Scale | Meso and macro | Micro |
| Reads | `roadmap.md`, `journeys/README.md`, `architecture.md`, the ADR index, the inboxes | `CLAUDE.md`, one journey document, the previous journey's E2E, `design-notes.md`, `glossary.md`, the handoff |
| Omits | Handoffs, journey detail, the rules for writing code | The rest of the roadmap, other journeys, the inboxes, the experiment menu |
| Produces | A rewritten plan, ADRs, journey documents | A journey, through the eight-step loop |

**Pointers rather than content is what makes this work.** An implementation
session starts from one journey document and must be able to reach anything else
it turns out to need — which is why journey documents *cite* rules rather than
restating them, and why the roadmap names a journey rather than describing it.
The measure of the set is not how much it holds. It is how little must be loaded
before work can start, and how reliably the rest can be found from there.

## Step 0, and what it produces

Project initialisation is **not a journey** — there is no actor and nothing an
end-to-end test could assert, and numbering it J1 would offset every project's
journeys by an artifact of the method.

It consumes the defaults and produces records:

1. **[ADR 0001](template/docs/adr/0001-what-kind-of-project-this-is.md)** — what
   kind of project this is. First, because it sets the bar every later rule is
   calibrated against, and because its escalation triggers are what stop a spike
   quietly becoming a product.
2. **[ADR 0002](template/docs/adr/0002-tooling-roles.md)** — the four tool roles
   and what the gate covers.
3. **[`README.md`](template/README.md)** — what the system is and who uses it.
4. **[`docs/journeys/`](template/docs/journeys/README.md)** — a document per
   journey of the first release, from
   [`TEMPLATE.md`](template/docs/journeys/TEMPLATE.md). Draft them all before
   building any.
5. **[`docs/roadmap.md`](template/docs/roadmap.md)** — that inventory, grouped
   into releases, with later releases held as sketches.
6. **[`CLAUDE.md`](template/CLAUDE.md)** — the project profile, the dials, the
   commands.

```bash
cp -r framework/template/. /path/to/new-project/
cd /path/to/new-project
git init && git add -A && git commit -m "Document set at its initial version"
```

**Or run [`tool/`](tool/README.md)**, which is the same copy with the answers
already rendered into it: the kind and its ADR, the four roles and theirs, the
task names spelled for the runner that was chosen, and the conditional documents
this project has not earned deleted along with every link to them. It asks the
questions above and writes records 1, 2, 3 and 6; journeys and the roadmap are
still yours, for the reason step 0 gives. `template/` stays directly copyable, so
the two paths lead to the same place.

```bash
cd framework/tool && uv run teamwork-init
```

Everything else grows as the project produces something to put in it. A document
still at its seed content after three journeys is telling you it has not earned
its place — delete it, or find out why nothing has been routed to it.

## The four tool roles

The method needs four jobs done and does not care what does them. Name the tools
once, in [`CLAUDE.md`](template/CLAUDE.md); record why in ADR 0002.

| Role | Has to provide |
|---|---|
| **Task runner** | A name for every repeated command, carrying the flags and variables that make it correct. The gate lives here |
| **Toolchain manager** | Pinned versions of the tools themselves |
| **Environment manager** | Per-environment configuration supplied to a command |
| **Dependency manager** | Locked dependencies in an isolated environment, so a build is reproducible |

One tool often fills several. Nothing assumes the mapping is one-to-one, and
nothing assumes a language. **Every document writes task names rather than
commands** — "the `ship` task" — so the runner can change without a rewrite.

## What each file arrives carrying

**Seeded** — real content on day one, because it is universal.

| File | Carries |
|---|---|
| [`CLAUDE.md`](template/CLAUDE.md) | The profile, the conventions, the eight-step loop |
| [`docs/README.md`](template/docs/README.md) | The index, the routing map, the two session modes |
| [`docs/dev-process.md`](template/docs/dev-process.md) | The method, the dials, and the evidence behind each claim |
| [`docs/design-notes.md`](template/docs/design-notes.md) | Engineering rules that generalise, marked `[inherited]` |
| [`docs/glossary.md`](template/docs/glossary.md) | The vocabulary of the work itself |
| [`docs/adr/`](template/docs/adr/) | Lifecycle, sections, the template, and ADRs 0001–0002 |
| [`docs/journeys/`](template/docs/journeys/) | Scope, numbering, the suffix rule, and a journey template |
| [`docs/handoff/`](template/docs/handoff/) | The handoff's stated job, its shape, and the residue test |
| [`docs/experiments.md`](template/docs/experiments.md) | Experiments on the process, as a menu |
| [`docs/inbox/`](template/docs/inbox/README.md), [`docs/references/`](template/docs/references/README.md) | The two categories for material that is not yet, or never, a document |
| [`.claude/skills/`](template/.claude/skills/) | `handoff` and `step-8` — the two procedures with the highest skip risk |

**Skeleton** — a stated job, a structure, nothing to say yet. `README.md`,
`roadmap.md`, `architecture.md`, `stakeholder-questions.md`.

**Conditional** — delete unless the project has the thing. Each earns its place
by a stated condition rather than by seeming prudent, and several of those
conditions are escalation triggers in ADR 0001.

| File | Earns its place when |
|---|---|
| [`deployment.md`](template/docs/deployment.md) | There is somewhere to deploy |
| [`data.md`](template/docs/data.md) | Somebody else looks after the store |
| [`security.md`](template/docs/security.md) | There is a credential worth stealing, personal data, money, or untrusted input |
| [`observability.md`](template/docs/observability.md) | Something runs where nobody is watching it |
| [`auditability.md`](template/docs/auditability.md) | Somebody will ask *who did this* |
| [`diagnostics.md`](template/docs/diagnostics.md) | Somebody who is not a developer will report a problem |
| [`backups.md`](template/docs/backups.md) | There is data that cannot be regenerated |
| [`ui-brief.md`](template/docs/ui-brief.md) | Design is done by somebody else |
| [`demo.md`](template/docs/demo.md) | The work has to be shown to a room |

**Generated** — produced by a task, never edited.
[`history.md`](template/docs/history.md).

## What this fixes from the project it was generalised from

**The handoff had no stated job**, so everything unfiled landed in a document
deleted on purpose — twice, findings survived only because somebody looked before
running `rm`. It has one now, and residue fitting no category routes to the
process loop rather than merely being noted. It is also **committed rather than
ignored**, since the method's own axiom is that context outside the repository
does not exist.

**There was no journey template**, so every journey document reinvented its shape.

**Loose files accumulated with no category** — a performance note, a schema
proposal, a PDF. `inbox/` and `references/` name those two kinds, and the inbox
carries an expiry.

**The eight-step loop was written out in three places** and had begun to differ.
It is stated once, in `CLAUDE.md`, because that is the file loaded every session.

**Nothing named the two session modes**, so every session loaded the same
material regardless of what it was for.

**Nothing declared the quality bar.** Production assumptions were load-bearing
everywhere and stated nowhere, so absence of a rule and deliberate omission of a
rule were indistinguishable. ADR 0001 and the dial table fix that.

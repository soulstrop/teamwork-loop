# How this project is built

Everything else in [`README.md`](README.md) is about the system. This is about
the *process* — what is done, why, and what it cost.

**How to read a claim here.** The method evolved across several projects; the
evidence written down comes mostly from one, because that is the project that
recorded it. So a rule stated plainly has usually been paid for more than once. A
rule stated *with a citation* has been paid for at least once in a way somebody
wrote down, and the citation is there so you can judge whether it travels. Where
a rule has no evidence behind it and is here on argument alone, it says so.

**This document is also the container for what this project learns about the
process** — the process loop in §8. Add to it; it is not read-only.

---

## 1. Step 0 — initialisation

Before the first journey, and it is not a journey: there is no actor, and nothing
an end-to-end test could assert. Calling it J1 would offset every project's
numbering by an artifact of the method.

What it consumes is **defaults** — standing priors brought to the project rather
than decided by it. What it produces is a record of decisions:

1. **[ADR 0001](adr/0001-what-kind-of-project-this-is.md) — what kind of project
   this is.** First, because it sets the bar every later rule is calibrated
   against.
2. **[ADR 0002](adr/0002-tooling-roles.md) — the four tool roles and what the
   gate covers.** The kind determines how much rigour the roles need, which is
   why it is second.
3. **[`../README.md`](../README.md)** — what the system is and who uses it.
   Everything else assumes it.
4. **[`journeys/`](journeys/README.md)** — a document per journey of the first
   release. Draft them all before building any: drafting is what surfaces the
   ordering, the shared rules, and the questions that belong to somebody else,
   and a journey document is a page.
5. **[`roadmap.md`](roadmap.md)** — that inventory, grouped into releases.
6. **[`../CLAUDE.md`](../CLAUDE.md)** — the profile, the dials, the commands.

A default taken unchanged is recorded in one line and cited, not restated. A
default departed from gets a sentence saying why. **What is not acceptable is
departing silently** — a later reader cannot distinguish a considered departure
from an accident, and neither can you in four months.

## 2. The journey is the unit of implementation

**Build one journey at a time, not one layer at a time.** A journey is one actor
completing one goal end to end. Building it means touching the domain, the
storage, the service and the interface in one pass.

The alternative — all the models, then all the repositories, then all the routes
— produces layers that have never met. Nothing is demonstrable until the last
layer lands, and every integration problem arrives at once, at the end.

*Evidence:* a rule reached from three unrelated call sites could not have been
designed layer-first. Its hard cases only appeared when the rule and its three
callers were built together.

**Horizontal modules are libraries, not layers.** A shared rule is built
minimally inside the journey that first needs it and allowed to grow. Nothing is
pre-built.

**The suffix, not the renumber.** A journey that turns out to need a sibling gets
`J4b`, `J4c`. Later numbers are already spoken for in the plan and in
cross-references, and renumbering rewrites the whole set for a sequence nobody
reads as a sequence.

## 3. The failing end-to-end test is the definition of done

**Write it before the implementation, and commit it red.** It is the journey
document turned into assertions.

**The E2E is the contract, not a starting point.** Its URLs, labels, button text
and accessible names are what the implementation must satisfy. When routes are
written days after the test, the test is the specification and the ambiguity
budget is zero.

**Selecting by accessible role and name makes accessibility load-bearing.** The
reason is mundane — designs arrive after implementation, so tests must survive a
restyle — but the effect is that every control's accessible name is *interface*,
asserted by the suite, rather than decoration somebody might get to.

**It is also how the next journey learns what this one established.** To find out
what an area actually settled, its E2E is a better source than its code: it
states the contract in the actor's vocabulary, it is short, and it cannot have
drifted from behaviour without failing. *Evidence:* a cold session building the
next journey read the previous journey's E2E fourth — before any source file, and
long before the architecture document. Nobody designed that use.

**Commit it red, in its own commit, and say so in the body.** *Evidence:* while
this was optional, two journeys did different things and both were compliant;
only one left proof. **A discipline that is not in the history is a discipline
nobody can check afterwards**, including the person who followed it.

It also exposes a hazard early: a missing module made the test runner report
`1 error, 0 tests` and silently skip 45 other tests. **A gate that reports
nothing is worse than one that reports a failure**, and step 2 is a better place
to meet that than step 5.

## 4. The journey loop

The eight steps are in
[`../CLAUDE.md`](../CLAUDE.md#4-the-journey-loop--eight-steps-every-journey),
because that is the file loaded every session. Stated once; what follows is why.

**Steps 5 and 6 are in that order deliberately.** They were the other way round
until the first journey ran both. *Evidence:* the simplification pass before the
deploy found the route surface; the same pass after it found a configuration
fallback that let the application connect as the schema owner, and a module-level
instance doing I/O at import time in every test process. Neither was visible from
the code, because neither is wrong until something outside the repository has an
opinion.

**Commit before deploying.** A release built from a dirty tree names a tree that
no longer exists, so "what is deployed" becomes unanswerable the moment a file is
edited. The deploy is a step in the loop, not a rescue.

**Deploy every journey, not every release.** The packaging cost of a journey is
paid by the journey that introduced it. *Evidence:* the first deploy found the
migrations were not in the package at all — a release could not have migrated
itself.

**Step 5 is about the running system**, and the exception is worth stating
because it will be reached for otherwise. An artifact that is not the deployed
system — a rendered documentation bundle, a paper, a report — is produced out of
band, and its toolchain is deliberately not a release dependency: a full TeX
installation has no business being reachable from the path that ships code. What
that exception must never become is a category the running system can be put
into. If it serves a request, it deploys in the loop.

### Step 8 is what keeps the plan a plan

The journey is finished; what it changed about the *unbuilt* work is written down
nowhere. Step 8 routes each durable thing to where it will be read, then
**rewrites** the affected plan rather than appending notes about what changed.
The test of a finished step 8: a reader who never saw the previous version cannot
tell which parts changed.

*Evidence:* run for the first time, retroactively, it produced six changes across
three documents — and **the most valuable was not a lesson but a contradiction**:
a rule built in one journey silently conflicted with a decision recorded for a
later one. That was invisible from inside the finished journey and appeared only
when looking forward. So the question step 8 asks is not *what did we learn* but
**what does this make false elsewhere**.

**Two prompts that are easy to skip.**

*What did this journey change that it did not add?* A journey's diff splits in
two. What it added is the work; what it **changed** in code earlier journeys
wrote is a lesson arriving late — that code was wrong or insufficient, and
nothing knew until this journey asked it a question it had to refuse. Those are
the highest-yield design notes available, because they are proven rather than
anticipated. *Evidence:* a cold session corrected two earlier journeys rather
than building around them — a table keyed in a way that forbade what a later
decision required, and a function that reported one state forever because nothing
had yet asked it something it had to refuse. Both are the kind of thing a cold
reader is *better* placed to see than the person who wrote them.

*What did this journey decide not to do?* Step 6 produces fixes applied and
findings skipped; only the first lands in a commit. A skipped finding goes to the
roadmap's open items with what was skipped, why, and **the event that would
change the answer**. Without that last part it becomes a list nobody re-reads —
and a deferral recorded nowhere is one the next simplification pass raises again,
having lost the reason it was declined.

### A release ends with a clean-up and a layer pass

The rule is in
[`../CLAUDE.md`](../CLAUDE.md#4-the-journey-loop--eight-steps-every-journey).
*It is here on practice across projects rather than on written evidence.*

**Small work needs a home that is not a journey.** Residue is not only
knowledge. Some of it is work — a rename, a missing guard, a test that should
exist — too small to deserve eight steps, and belonging to no journey still to
come. Folded into the next journey, it pads a diff that should be about one
actor's goal. Left in the handoff, it stops the handoff reaching zero. Dropped,
it is lost. So it goes on the release's clean-up list in
[`roadmap.md`](roadmap.md), and the clean-up works the list down as one unit
once the journeys are built.

**Journeys see their own path through the layers, never a whole layer.** Each
step 6 simplifies what one journey touched. After several journeys, every
interface between layers has been extended by each of them in turn and looked at
as one surface by none: conversions done twice, a parameter threaded through for
a single caller, a service function per journey where one would do. The layer
pass reads by layer to find those. It comes after the clean-up, so it reads the
code the release will actually ship.

**The journey E2Es are what make it safe.** They select by role and name rather
than by structure, so the layer pass can reshape the internals freely, and an E2E
going red means the pass changed behaviour rather than shape.

**Both end in step 8.** What they find is step 8's question asked at release
scale, and it arrives at the cheapest moment to act on it: the next release's
journeys are mostly still sketches, so changing them costs a rewrite of a row.

### The dials, and what sets them

Not every rule above applies at every quality bar. The kind of project — recorded
in [ADR 0001](adr/0001-what-kind-of-project-this-is.md) — sets these; the project
records only its **deviations** from the column it picked.

| Dial | Spike / POC | Learning | On spec | Production |
|---|---|---|---|---|
| Deploy inside the loop | no | no | per release | every journey |
| E2E first, committed red | one, maybe | yes — it is the point | yes | yes |
| Real dependencies in tests | no | yes | where constraints matter | yes |
| Accessibility asserted in the E2E | no | no | yes | yes |
| ADRs written | only what you would re-argue | yes | yes | yes |
| Simplification pass | skip | yes | yes | yes |
| Step 8 | light | yes | yes | yes |
| Clean-up and layer pass at release end | skip | yes | yes | yes |
| Config and secrets | committed defaults fine | fine | must not leak | no defaults; refuses at startup |
| Documents beyond roadmap + journeys | none | glossary, design notes | the full set | the full set |

**Two are not dials.** A **named gate**, even if it runs one command — added
later, it says nothing about anything built before it. And **step 8 in some
form** — a unit of work with no record of what it found is a unit somebody runs
twice.

**A dial turned down needs a reason recorded**, because absence of a rule and
deliberate omission of a rule are indistinguishable from inside the repository.

## 5. One named gate that means done

`ship` — lint, type-check, fast tests, drift, cross-references, journey E2E.
What it must cover is in [ADR 0002](adr/0002-tooling-roles.md).

**Every repeated command has a name, and you run the task rather than the tool it
wraps.** Not style: tasks carry the flags, environment and connection strings
that make a command correct. A hand-built invocation drops them silently — the
test runner pointing at a development database instead of a test template, the
migration tool running as the wrong role. It also costs fewer retries, which
matters when an agent is running the commands.

**If a task's flags are wrong, fix the task.** Do not work around it.

**The gate only means something if nothing is allowed past it.** Report failures
rather than working around them, and never weaken a test to get a green gate.

**A gate says nothing about what it does not look at.** *Evidence:* the gate here
never touched the development database, so that database drifted four migrations
behind while every run stayed green. The fix for that class of gap is a task that
refuses, not a line in a document.

## 6. Why it is shaped for a collaborator with no memory

**The agent starts every session cold.** It has the repository and nothing else —
no recollection of yesterday's reasoning, no sense of which decisions are
settled, no memory of the thing that was tried and abandoned. Everything it needs
has to be *in the repository, in the place it will look*.

That single constraint produces most of this process:

| Practice | What it is really for |
|---|---|
| `CLAUDE.md` | Conventions loaded every session, so they are not re-derived or re-argued |
| ADRs with *"reconsider this if"* | Stops settled decisions being relitigated by somebody with no memory of settling them |
| The glossary, with rejected names | A name turned down without its reason gets re-proposed within a week |
| Journey documents | The specification survives the session that wrote it |
| The handoff | The current unit's state, for a resume that starts from zero |
| `Lesson:` trailers | Capture at the moment of insight, because the insight will not survive the session |
| Docstrings carrying *why* | The reasoning is where the code is, which is the only place it is certain to be read |

**A human developer holds most of this in their head and pays no filing cost. An
agent cannot, so the filing cost is the price of the collaboration** — and the
side effect is a project a new human contributor can also enter cold.

**The corollary is that context which is not written down does not exist.** A
decision made in conversation and not committed is gone. This is why step 8
routes rather than remembers, and why the handoff is a document rather than a
habit.

**The source tree is the only artifact guaranteed current.** It is the
accumulated result of every journey. What it cannot carry is *why*, which is the
whole argument for docstrings that reason rather than describe.

### Two sessions, two context budgets

Planning and implementation are different jobs and should not load the same
material — the split is in [`README.md`](README.md#two-ways-in). Planning wants
the meso and macro view and almost none of the micro; implementation wants one
journey's worth of micro plus pointers to everything else.

**What makes that work is pointers rather than content**, which is why journey
documents cite rules rather than restating them. The measure of this set is not
how much it holds; it is how little must be loaded before work can start, and how
reliably the rest can be found from there.

*Evidence, one data point:* a cold session given only "start J8" produced the
journey complete through all eight steps, including the two steps nothing
enforces. Its navigation was roadmap → look for a handoff, find none → the
journey document → the previous journey's E2E → source in dependency order. The
architecture document, the largest in the set, was first read substantively at
minute 47, *to update it*. The documentation index did no orientation work at
all. **Honest limits:** one journey, one repository, one model, and an author who
had written the documents under test.

## 7. The document set as a system

**Each document has one job, they cross-reference rather than repeat, and the
cross-references are checked mechanically.** [`README.md`](README.md) is the map.

The routing question — where a thing goes — is in
[`../CLAUDE.md`](../CLAUDE.md#6-where-a-thing-goes--ask-in-this-order), because
it must be in hand at the moment something is learned rather than looked up
afterwards.

**History is `git log`.** No committed document records what used to be true. A
*generated* narrative is exempt, because it is rebuilt rather than maintained and
therefore cannot drift.

### The three failure modes, all of which happened

**Documents accumulate history unless something forces rewriting.** A roadmap
grew a findings section per journey and reached 2,143 lines, half of it
retrospective; somebody looking for the next step read a thousand lines of
completed work first. Appending is easier than revising, which is why step 8
names rewriting as the requirement.

**A document with no stated job collects everything unfiled.** The handoff was
the only one without a defined job, so anything that fitted nowhere landed there
— and handoffs are deliberately disposable. Two consciously-deferred findings,
with their reasoning, existed nowhere else and were one `rm` from being lost.

**A threshold nothing measures only gets crossed.** A decision named ~600 lines
as the signal to split a module. One was flagged by hand at 707 and reached 1,078
unnoticed, with two others also over. A number in prose is not a check.

### The handoff burns down, and the residue loop runs to zero

The loop and its four kinds are in
[`../CLAUDE.md`](../CLAUDE.md#7-the-handoff-and-the-residue-loop), because it
runs every time the handoff is touched. What follows is why.

**Shrinking the handoff to nothing is the objective, not a check at the end.** A
handoff treated as a report is written once and read at resume. A handoff
treated as a burn-down gets **shorter every session**, and its length is the
honest measure of how much of the unit remains.

**The deletion is the receipt.** An entry routed but left in place is
indistinguishable from one nobody has looked at, and it costs the same attention
again on the next read.

**Checkable state goes to a task, not a document.** The task is then the thing
that remembers, and it cannot go stale the way a sentence can.

**The loop lengthens before it shortens.** Handling one signal routinely surfaces
another — routing a rule reveals two documents disagreeing, making a task refuse
reveals a second caller. That is the loop working, and it is why the exit
condition is *no signals remain* rather than a number of passes.

**The fourth kind, residue that fits no category, is the one to protect.** It is
the only signal about the process that arrives without anybody going looking for
it, which makes it the most valuable and the easiest to lose. Filed into the
nearest approximate bucket, it empties the line and feels like progress while the
categories go unquestioned: the register reaches zero and the project learns
nothing.

## 8. The process loop

Four feedback loops run, at widening scope, and only the first three have a
cadence:

| Loop | Feeds back into | Triggered by |
|---|---|---|
| The inner loop | the code | a red test |
| The journey loop | the plan, at step 8 | the journey finishing |
| The release loop | the plan, at the step 8 after the clean-up and after the layer pass | the release's last journey finishing |
| **The process loop** | the process itself | friction in how the work is done |

**The third one is this document**, together with `CLAUDE.md` and the tasks — the
rules rather than the system.

**It is not the same path as the handoff's residue**, and the difference is the
direction of arrival. Residue is bottom-up and unbidden: a leftover with no home
reveals a gap nobody was looking for. The process loop is reflective and goes
looking — somebody notices a document grew wrong, or that two journeys read one
instruction differently. Both amend the process; they start at opposite ends, and
a process with only the first never questions its own categories.

**Its weakness is that it has no cadence.** It runs when somebody chooses to
look. The best available signal that it is overdue is **friction that has
happened twice**: one journey doing something awkwardly is an anecdote; two doing
it differently is a rule that was never written.

**Entering it cold** means answering a different question first — *what friction
has accumulated?* The inbox for that is the `Lesson:` trailers in the history,
extracted by a task, captured at the moment of insight by whoever hit the thing.
Then [`experiments.md`](experiments.md) for what could be run to settle any of
it. That is a menu, not a queue: attention is the scarce resource and declining
an experiment is a normal outcome.

## 9. What is untested here

*Kept honestly, and worth more than the confident parts.*

- **Portability.** The parts that generalise and the parts that are shaped by one
  problem domain are not yet reliably distinguishable.
- **Whether the documentation cost scales.** Roughly half a line of documentation
  per line of source has been affordable because each document has one job and
  step 8 stops them growing history. Whether that holds at three times the size
  is unknown.
- **Whether the loop survives a team.** Everything assumes one developer plus an
  agent, and a linear history. Concurrent journeys, review, and merge conflicts
  in the documentation set are all untested.
- **Whether E2E-as-contract holds under a designer.** Designs arriving after
  implementation is what makes accessible-name selection safe. A project where
  visual design leads might invert it.

**The thing to watch first:** step 8 is load-bearing and the easiest to skip,
because it happens after the work feels finished and produces nothing
demonstrable. Everything short in this set is short because step 8 ran. The first
time it is skipped, the plan starts accumulating again — slowly enough that
nobody notices for several journeys.

# ADR 0001: What kind of project this is

- **Status:** proposed
- **Date:** YYYY-MM-DD
- **Supersedes:** —
- **Superseded by:** —

*Written at step 0, before anything else. The Problem and the options below come
with the method; the Decision is this project's. Set the status to `decided` when
it is written, and copy the resulting dial settings into the table at the top of
[`../../CLAUDE.md`](../../CLAUDE.md).*

## Problem

The method assumes a quality bar and never states it. Deploying every journey,
testing against real dependencies, asserting accessibility, writing a record for
every decision — each is correct for something that will run for years in front
of people who did not choose it, and each is waste on a spike that will be
deleted in a fortnight.

A collaborator starting cold cannot infer the bar. **Absence of a rule and
deliberate omission of a rule look identical from inside a repository**, so
without this record every session either over-builds a throwaway or under-builds
a product, and neither mistake announces itself.

The second problem costs more. **A project's kind changes, and almost always in
one direction:** the spike that demonstrated well becomes the thing that ships,
carrying every shortcut that was correct when it was a spike and is a defect now.
Nobody decides to promote it — it simply stops being deleted. So this record
exists as much for its *Reconsider this if* as for its decision.

The dials each kind sets are in
[`../dev-process.md`](../dev-process.md#the-dials-and-what-sets-them).

## Options considered

### A. Spike or proof of concept

Built to answer one question — is this possible, is it fast enough, does the
shape work — and then deleted or rewritten.

**For:** the fastest route to the answer. Ceremony that does not serve the
question is waste, and most of it does not serve it.

**Against:** it is the kind most likely to be promoted without anybody deciding
to, and every shortcut is then load-bearing. Nothing inside a spike distinguishes
*not needed* from *not done yet*.

### B. Learning

Built to understand a technique, a stack or a domain. The artifact matters less
than what is understood at the end.

**For:** the discipline *is* the deliverable. Writing the test first and
recording why a decision was taken are the parts that produce the understanding,
so they cost nothing and return everything.

**Against:** operational work — deployment, secrets, real-data capture — teaches
little per hour and can be dropped.

### C. On spec

Built speculatively, in the hope somebody buys it. Has to be demonstrable and
credible; does not have to be finished.

**For:** the honest middle. Polish where a buyer looks and nowhere else.
Accessibility and a coherent interface are in the first category, because
retrofitting them costs more than doing them.

**Against:** *where a buyer looks* is a guess, and it is usually wrong about
which parts turn out to matter. This is the kind that most needs its open items
written down, since the deferrals are the pitch's fine print.

### D. Production

Will run in front of people who did not choose it, for years, maintained by
somebody who is not here yet.

**For:** every rule in the method was paid for by a project of this kind.

**Against:** the full cost — roughly half a line of documentation per line of
source, on the evidence available. Affordable only because each document has one
job and step 8 stops them growing history.

## Decision

*(Which one, and why. State the bar in a sentence somebody can hold: what this
project owes whoever uses it, and what it does not.)*

**Dials, where they differ from the kind's defaults.** *(Every deviation gets a
reason. A dial turned down without one is a shortcut nobody will later recognise
as deliberate.)*

| Dial | Setting here | Why it differs |
|---|---|---|
| | | |

**Two things stay on at every kind**, and neither is in the table:

- **A named gate**, even if it runs one command. Added later, it says nothing
  about anything built before it.
- **Step 8, in some form.** A unit of work with no record of what it found is a
  unit somebody runs twice.

## Reconsider this if

Escalation triggers. Each is a moment at which this project has quietly become a
different kind, and the point of naming them is that nobody announces it.

- Somebody outside the team depends on it running
- It is demonstrated to a buyer, a user or a stakeholder who takes it seriously
- It acquires data that cannot be regenerated
- It acquires a credential worth stealing
- A second person has to work in it
- It survives past the date it was going to be deleted

**When one fires, the change is not free and the debt is not diffuse.** Write the
new decision here, reset the dials, and put what the old kind licensed into the
roadmap's open items as work — what was skipped, why it was right then, and what
it costs now. That list is the price of the promotion, and it is cheapest to
write on the day the trigger fires, while somebody still remembers which
shortcuts were deliberate.

# Architecture

What the components are, what each is responsible for, and how they relate.

**Why** things are shaped this way lives in [`adr/`](adr/README.md) — this
document links rather than repeats. It is a living summary and will churn as
journeys land; the ADRs are the durable record. **When the two disagree, the ADRs
are right and this document is stale.**

*A note on what this document is for. In the project this method came from, the
architecture document was the largest in the set and was first read substantively
at minute 47 of a journey — to update it, not to consult it. That may mean its
job is narrower than its size, or it may mean that journey extended an area
already legible from its neighbours. Watch which happens here. A document read
only in order to maintain it has a maintenance cost and no reader.*

## Diagrams

**Commit the source, never only an export.** A rendered image nobody can edit
becomes wrong and then stays wrong, because correcting it costs a tool somebody
does not have installed.

In rough order of what to reach for:

- **ASCII is enough.** It needs no tooling, renders in a terminal, a diff and a
  code review, and it ages better than anything that depends on a renderer. For a
  block diagram it is often the right answer permanently, not a placeholder.
- **Mermaid is better where it fits**, and for the same reason ASCII is good: the
  committed artifact is text, so it diffs and can be edited by anybody. It buys
  layout that stays correct when a node is added — which is exactly where ASCII
  becomes tedious to maintain.
- **A sequence diagram is sometimes the best thing in the set**, and it does a
  different job. It describes interaction over time, and its real value is as a
  **focus for discussion and agreement** — particularly across a boundary
  somebody else owns, where the disagreement is about ordering and nobody
  discovers it in prose. Draw one when a conversation needs settling; keep it if
  the interaction is load-bearing, and let it go if it was scaffolding.
- **A dataflow diagram earns its place twice**, since it doubles as the system
  block diagram: what moves, where it goes, and what holds it are the same
  question asked structurally and dynamically.

## The system

*The block or dataflow diagram, and two things worth marking on it explicitly
because they are what a reader gets wrong:*

- **What is a target and what exists today.** Draw the intended shape, then say
  in a sentence which parts are real. A component drawn but not built is
  deliberate — it arrives with the journey that first needs it, which is why it
  is drawn here rather than discovered later.
- **Anything that cannot be run twice.** A component whose state must be
  single-instance is a fact the supervisor has to know, and it belongs where
  somebody deploying will see it.

## Layout

*The repository, sliced the way it is actually sliced, with a line per directory
saying what belongs there. Include the rule that governs the slicing — by area,
by layer, by whatever — because that rule is what tells somebody where a new
module goes.*

*State the import directions that are not allowed. A direction that is merely
conventional is one that gets violated; a direction with a static check behind it
is a rule.*

## Components

*One section per component: what it is responsible for, what it may not do, and
the small number of things about it worth knowing by name.*

*The useful content here is rarely the list of modules — it is the argument for
why a boundary sits where it does, and what would break if it moved. A section
that reads like a table of contents is repeating the layout above.*

## Test layers

*One row per layer: what it asks, what it needs to run, and — the part that
matters — what it can answer that the layers either side of it cannot.*

| Layer | Asks | Needs |
|---|---|---|
| | | |

*A layer that cannot be distinguished from its neighbours by that third question
is a layer that should be merged.*

## How work flows through the system

*The end-to-end path, in the domain's terms rather than the code's, annotated
with which journey built each stage. This is the section that orients somebody
fastest, and it is usually the last one written.*

## What is deliberately absent

*Things a reader would reasonably expect and will not find, each with the reason
and a link to the decision. This section prevents the most expensive kind of
rework: somebody helpfully adding what was left out on purpose.*

-

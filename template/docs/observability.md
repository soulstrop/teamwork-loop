# Observability

*Conditional — earns its place when something runs somewhere nobody is watching
it. A tool run by hand does not need this; anything deployed does.*

**The job:** what is measured, **why each measurement would change a decision**,
what the budgets are, and what is deliberately not measured.

**Not the job:** what to do when a measurement goes bad — that is the runbook in
[`deployment.md`](deployment.md). Nor the component structure, which is
[`architecture.md`](architecture.md). This document is the argument for each
signal; the runbook is the procedure that consumes it.

## The seam

*One module owns the instrumentation, and nothing else imports a telemetry
symbol. Name it here.*

*Keeping the export protocol generic means the backend choice stays a later
decision and never leaks into application code — which is worth more than it
sounds, because the backend is the part most likely to change and the application
is the part most expensive to change.*

**Install the real instrumentation everywhere, including locally and in tests.**
A no-op in development means instrument creation, attribute types and cardinality
behave differently there, so a metric can be broken in a way that first appears
in production. That is the failure mode that makes people stop trusting their own
dashboards.

## What is measured

*Each row justified by the decision it would change. A metric that would not
change anything is a metric nobody looks at twice.*

| Signal | Why it earns its place |
|---|---|
| | |

**Distinguish trend from point value.** Some measurements only mean something as
a trend — anything that grows with the size of the data — and a single reading of
one is noise. Others have a hard budget, and a single reading does mean
something. Say which each is, or the first alert on a trend metric teaches
everybody to ignore it.

## Budgets

| Operation | Budget | Measured |
|---|---|---|
| | | |

*A budget with no measurement behind it is a number in prose, which is not a
check. If a budget matters, something records it.*

## Reason codes and cardinality

*Where the system refuses, counting **why** is usually the most informative
signal it produces — the aggregate shows a problem no single user would report.*

Two rules travel with that:

**A closed set, shared with whatever renders it.** The same codes are the metric
labels and the sentences people read. A code added to one and forgotten in the
other reaches a screen as itself, so the set is worth pinning with a test rather
than trusting to review.

**Codes carry nothing anybody typed.** Unbounded cardinality is a bill as well as
a broken dashboard, and a telemetry backend has none of the access controls the
store has. The sentence shown to a person names the specific thing; the metric
label does not. Assert the separation rather than relying on review.

## Instrumentation should be structural

*Make the only way to do the thing be the way that records it.* If the sole path
to putting a refusal in front of somebody takes the reason code as an argument,
the refusal counter is trustworthy. Otherwise the dashboard measures the subset
somebody remembered to instrument, and there is no way to tell which subset that
is from looking at it.

## What is deliberately not measured

*Each with a reason and what would change it.*

*The recurring case: something per-item where the item count is large. One span
per batch is a trace somebody can read; one span per element is a trace nobody
can. State which level the instrumentation sits at and why.*

-

## Definition of done

New code emits its spans and metrics as part of the journey that adds it, not as
a later pass. Retrofitting observability means choosing signals from outside the
work, which is how a system ends up measured by whatever was easy.

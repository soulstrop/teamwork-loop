# Diagnostics and reproduction

*Conditional — earns its place when somebody who is not a developer will report a
problem. Before there are users there is nothing to reproduce.*

**The job:** capturing enough of what led to a moment that somebody can
reconstruct it — the state a journey was in, what the person was trying to do,
and where it went wrong.

**Not the job:** [`observability.md`](observability.md), which asks whether the
system is healthy in aggregate, and [`auditability.md`](auditability.md), which
records who did what because an obligation says so. The overlap in *mechanism* is
real and the difference in **retention** is what keeps them apart — see
[below](#four-captures-four-retention-boundaries).

## A journey has a state machine, and it is already written down

**The journey document's steps are the transitions.** Actor, precondition, steps,
outcome — that is a state machine described in the actor's vocabulary rather than
the code's, and it is written before the implementation exists.

Two things follow, and both are worth more than they cost:

**Name the states explicitly in the journey document**, and the same names appear
in the E2E assertions, in the transition record at runtime, and in what a user
says when they report a problem. A trail that reads *chose a date → saw three
options → picked one → was refused* is a trail somebody can act on. One that
reads in module names is a trail that has to be translated first, by the person
least able to.

**Record the transitions.** Which states this actor passed through, in order,
with what carried them across each. A reported problem then arrives with its own
reproduction, and the gap between *what the user says happened* and *what
happened* becomes visible rather than inferred.

*A sequence diagram is the natural rendering — see
[`architecture.md`](architecture.md#diagrams), where the same diagram earns its
place as a focus for agreement.*

## The feedback button

**Feature-flagged, and on during alpha and beta.** A button on the screen that
lets somebody say, in their own words, what they think is wrong.

What makes it worth building is not the narrative. It is that **pressing it
captures the transition trail that led to this screen**, so the report arrives
already reproducible.

The design points that matter:

- **Capture the trail at press time, from state already held.** Never ask the
  person to reproduce anything. The report you get is the one that costs them ten
  seconds; anything more and you get silence instead.
- **The narrative and the trail travel together.** Separately, the narrative is a
  complaint and the trail is noise.
- **Include the build identity** — release, revision, environment. A report
  against a version nobody can identify is a report about a system that may no
  longer exist.
- **The flag is the retention boundary.** Off by default, on for a stage, and
  turning it off is what stops the collection. That is a cleaner control than a
  policy, because it is a switch somebody can see the state of.
- **It captures whatever the person was looking at**, which may be somebody
  else's personal data. State what is included and what is redacted, and treat
  the store of reports with the same care as the data it quotes — this is the
  part that is easy to get wrong precisely because the intent is benign.

**Say where reports go.** A feedback channel with no routing becomes a queue
nobody empties. Each report resolves to a bug, an entry in
[`roadmap.md`](roadmap.md)'s open items, a
[stakeholder question](stakeholder-questions.md), or nothing — and then it is
deleted.

## Event capture and replay

*Architecture-dependent: this is available when the system is event-shaped, and
does not exist otherwise. Delete this section if it does not apply.*

**Record the events within the span in which an error occurred**, so the sequence
can be replayed and the state at the moment of failure reconstructed.

Three things determine whether this is a debugging aid or a trap:

**Replay is only faithful if the non-deterministic inputs are captured too.** The
clock, randomness, identifiers, and anything that came back from outside. Name
them, and say for each whether it is recorded or stubbed on replay. An
unrecorded one produces a replay that diverges silently, which is worse than no
replay because the divergence is mistaken for the bug.

**Replay is a debugging aid and never a repair.** Replaying into a live system is
a different operation with different consequences — side effects that already
happened will happen again. If both are wanted, they are two mechanisms with two
names, and the dangerous one is the one that needs the guard.

**It is the richest and most sensitive capture in the system**, because it
contains whatever moved. Its retention should be the shortest of anything here,
and its readership the narrowest.

## Four captures, four retention boundaries

The mechanisms overlap; the boundaries are what keep them straight.

| Capture | Triggered by | Holds | Retained until | Read by |
|---|---|---|---|---|
| **Telemetry** | Always, sampled | Codes, counts, durations — nothing anybody typed | A clock: weeks or months | Anyone |
| **Audit** | Always, complete | Who did what, and when | A policy, usually years | Privileged only |
| **Diagnostic trail** | A person pressing the button, or an error | States, ids, and a narrative | **The problem being closed** | Developers |
| **Event capture** | An error inside a span | Everything that moved, including payloads | The shortest window that is useful | Narrowest |

**The third and fourth are the ones with an unusual rule:
they are deleted when the work item they explain is closed.** Retention tied to a
work item rather than a clock is what stops a debugging aid becoming an
unmanaged, unbounded, personal-data-bearing archive — which is the state it
drifts into by default, because nobody ever has a reason to delete something on a
particular Tuesday.

**Write the deletion into the process, not the policy.** Closing the bug deletes
the capture; if that is manual, it will not happen. This is a case for a task
that refuses, or a retention rule the store enforces.

# Threat model

*Conditional — earns its place when the project holds a credential worth
stealing, personal data, money, or accepts input from somebody untrusted. Delete
it until then, and note that three of those four are also escalation triggers in
[ADR 0001](adr/0001-what-kind-of-project-this-is.md).*

**The job:** what is being protected, from whom, where the trust boundaries are,
and — the part that is usually missing — **what is deliberately not defended
against**.

**Not the job:** how a control is implemented. That is an ADR if the choice was
significant, a [design note](design-notes.md) if it is a rule for writing similar
code, and otherwise the code itself. This document says what must hold; the code
says how.

## What is worth stealing here

*The assets, in the order somebody attacking would want them. Be specific — "the
database" is not an asset, "the roster with home addresses" and "the session
secret" are, and they have different attackers.*

| Asset | Why somebody wants it | Worst case if they get it |
|---|---|---|
| | | |

## Who is in the model

*Not "hackers". The useful list is mostly people who are legitimately here:*

- **An unauthenticated stranger**, reaching whatever is exposed.
- **A legitimate user acting outside their scope** — the largest category by
  incident count, and the one an access model either prevents structurally or
  does not prevent.
- **Somebody who has compromised one component**, asking what that buys them.
  This is the question that justifies splitting credentials.
- **An insider with database access**, which is the case audit trails exist for
  and controls in application code do not touch.
- **A supply-chain path** — a dependency, a build step, a vendored copy.

## Trust boundaries

*Where data crosses from somewhere you control to somewhere you do not, or the
reverse. Each boundary gets a line saying what is checked as it crosses.*

*The recurring finding: a boundary that is checked by every caller remembering is
not a boundary. Find the one door the value comes through and make that door
refuse — see [design notes](design-notes.md#make-the-door-refuse).*

## What is defended, and where

| Threat | Control | Enforced where |
|---|---|---|
| | | |

**The third column is the one that matters.** A control in application code is
one code path away from being bypassed; a control the store enforces is not. A
control at a door every write passes through holds; a helper every caller is
supposed to call is a convention.

## What is accepted, and why

*The section that makes this document honest. An accepted risk is only accepted
if somebody wrote it down — otherwise it is an oversight that will be described
as a decision afterwards.*

*Each entry: what is not defended against, why that is reasonable now, and
**what would change the answer**.*

-

## Secrets and credentials

*Where values come from, what has no default, and what the application is
structurally unable to do.*

*Two rules that generalise:*

- **A setting that selects an identity or a credential gets no default.** A
  fallback between two credentials is a security decision wearing the clothes of
  a convenience — an unset variable silently connecting as the privileged
  identity is the shape it takes.
- **A configuration mistake that leaves the system looking entirely well must
  fail at startup**, because nothing later will report it.

## Reconsider this model if

*The model is a claim about the system **as deployed**, not as designed, so it
goes stale in ways the code does not show.*

- A new class of data arrives — anything personal, financial or medical
- A component gains a path to the outside that it did not have
- An identity gains a privilege, particularly the ability to change the shape of
  the store
- A dependency with a large surface is added, or a vendored copy is updated
- The deployment topology changes, since most boundaries here are topological

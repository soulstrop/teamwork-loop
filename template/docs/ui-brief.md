# Interface brief

*Conditional — delete this file unless design is done by somebody who is not
implementing it.*

Context for design work. **The behaviour is already decided** — what is needed is
the interface layer over it. This is an **output**: it stands alone, because its
reader is not going to read the rest of the set.

*It can run in parallel with implementation, and should. It needs only journey
outlines and a screen inventory, not finished screens — so draft it early, submit
it while the first journeys are being built, and aim for designs to land before
the first screen facing the people the system is for.*

*Until they arrive, build plain functional interface and assert against
accessible roles and names. That is what makes the designer's output free to
change without touching tests.*

## The visual foundation is not open

**Design decisions are intermediated by a design system.** This project vendors
one; the application composes its tokens and defines none of them. Colour, type,
spacing and the rules governing them are settled there, not here.

*Name the system, where it is vendored, and the ADR that adopted it.*

**What that leaves genuinely open** is everything the design system has never had
to answer — usually the dense, specific parts of this application that a general
foundation was never built for. That is where the work is, and it is worth
listing explicitly so the brief does not read as a request to restyle what is
already decided.

**A token this project needs and the system lacks is a gap in the system**, not
an exception to it. It is designed here and propagated back; a project-local
token that stays local silently is how one house style becomes two.

*If this project is for a client with their own design system — including an
implicit one, which is the common case — say so. The token layer is what elicits
it: filled in from their existing material, and every gap is a question for
somebody on their side.*

## What is being designed

*The system in two paragraphs, for somebody who will never read the code.*

## The audiences

| Audience | How many | Device reality |
|---|---|---|
| | | |

*The third column is what changes designs. Somebody standing up, on a phone, in
poor signal, using this twice a month is a different problem from somebody at a
workstation for six hours — and the second is usually what gets designed for by
default, because it is what the designer is sitting at.*

## Hard constraints

*What is not open beyond the foundation, and why. Rendering model, device
targets, anything an existing system already settles, anything that has to work
without scripting.*

## Screens

*An inventory, then per screen: what it is for, its states, the data it must
show, and what the actor can do from it.*

**States are the part that gets skipped and the part that matters.** Empty,
loading, partial, refused — and specifically **what a refusal looks like**. A
system that explains why it said no does most of its interface work in exactly
the state nobody designs.

## Accessibility

Not something added at the end. Stated here as a constraint:

- **Every control has an accessible name that says what it does**, because those
  names are asserted by the test suite. A control nobody can ask for by name
  fails the suite as well as the person using a screen reader.
- **Anything reachable by pointer is reachable another way.** Where an
  interaction is an enhancement, the thing it enhances works without it.
- **Contrast and target sizes are checked at the token layer**, inside the design
  system, so that every use of a token inherits the result.

## What is not being asked for

*The boundary of the brief. Anything a designer might reasonably produce that
would be discarded, and why — cheaper to write than to explain afterwards.*

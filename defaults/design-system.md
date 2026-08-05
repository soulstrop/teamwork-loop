# Design system defaults

**The prior: design decisions are intermediated by a design system, and the
application never makes one directly.**

There is an established house style. A project vendors it, references it, and
contributes back to it. A project that needs a design decision the system does
not cover has found a gap in the system, not an exception to it.

## The rule that makes it real

**Tokens are the interface. The application may reference them and may not define
them.**

Concretely: no literal colour, font stack, spacing value, radius, shadow or
breakpoint appears anywhere outside the design system's own directory. The
application's styles are compositions of tokens and layout; the tokens are
somebody else's decision, deliberately.

**Enforce it mechanically.** A static check that fails the build on a literal
outside the boundary, and on anything inside the boundary reaching out into the
application. This is not tidiness — it is the only thing that keeps the boundary
intact under maintenance pressure, and a boundary maintained by everybody
remembering is one that two commits eventually breach.

**Assert contrast on the tokens themselves.** A design system can carry an
accessibility defect exactly as easily as application code can, and checking it
once at the token layer covers every use of it.

## The vendored copy is a fork until it is pushed back

A project holds a copy so that it builds without reaching outside itself. That
copy is a **fork the moment it is edited**, and the debt is real:

- **A new token a project needs propagates back to the design system.** That is
  the mechanism by which the system learns — most of what belongs in a design
  system is discovered by a project needing it, not by anticipating it.
- **A local change that is not pushed back is a divergence** with nothing
  reporting it. Say so in the project's ADR when it happens, with what is owed.
- **What must not happen is a project-local token that stays project-local
  silently**, because the next project re-derives it differently and now there
  are two house styles.

## Why this earns its place beyond taste

**The reskin contract.** If the boundary holds, swapping the design system is
replacing one directory. That is what makes it cheap to move a project to a
client who has their own — which is the case that pays for the discipline, since
it is otherwise invisible until the day somebody asks.

**A client's design system is often implicit**, and this is the more common
situation rather than the exception. They have a brand, some colours, a font
somebody chose, and no artifact naming any of it. **The token layer is what
elicits it:** filling it in from their existing material is a short exercise that
produces a real design system, and every gap in it is a question somebody on
their side has to answer — which is a better conversation than discovering the
disagreement after the interface is built.

**It also separates two jobs that get confused.** What the interface *does* is
decided by the journeys and is not negotiable with a designer; what it *looks
like* is the design system's. When those are tangled, every visual change is a
behavioural risk, and every behavioural change waits on a designer.

## Reconsider these if

- **Visual design leads rather than follows.** The whole arrangement assumes
  designs arrive after the functional interface exists, which is what makes
  selecting by accessible name safe in tests. A project where the design is the
  specification inverts it, and the tests have to be re-argued.
- **The project is a spike or a learning exercise**, where any styling at all may
  be waste — though note that adopting the system costs nearly nothing and
  retrofitting the boundary costs a pass over every stylesheet.
- **The client's system is genuinely incompatible in kind** — a native platform's
  conventions, a component library that owns its own visual decisions and does
  not expose tokens. Then the boundary is at the component rather than the token,
  and the rule needs restating for that shape rather than dropped.
- **The house style has never been used on a project of this type**, in which
  case expect to contribute more back than you consume, and budget for it.

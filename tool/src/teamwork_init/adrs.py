"""The records step 0 produces beyond the two that ship with the template.

`defaults/README.md` says a default is either taken or departed from and the
project's ADR records which. Two of the four defaults have no seeded ADR waiting
for them — storage and the design system — so if the wizard asks the question it
has to write the record, or the answer lives only in the wizard's memory, which
is the one place the method says context cannot live.

Both are written only when there is something to write. *Not decided yet* is an
honest answer and produces no file: an ADR seeded with a decision nobody took is
worse than an absent one, because it looks authoritative.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import markdown
from .catalogue import Catalogue
from .model import Answers, DesignSystem, Rung

HEADER = """# ADR {number}: {title}

- **Status:** decided
- **Date:** {today}
- **Supersedes:** —
- **Superseded by:** —
"""


@dataclass(frozen=True)
class WrittenADR:
    number: str
    filename: str
    title: str


def write_extra_adrs(project: Path, answers: Answers, catalogue: Catalogue) -> list[WrittenADR]:
    """Write the storage and design-system records, and index them."""
    adr_dir = project / "docs" / "adr"
    written: list[WrittenADR] = []

    if answers.rung is not Rung.UNDECIDED:
        written.append(_write(adr_dir, _storage_adr(_next_number(adr_dir), answers, catalogue)))
    if answers.design_system in {DesignSystem.HOUSE, DesignSystem.CLIENT}:
        written.append(_write(adr_dir, _design_adr(_next_number(adr_dir, written), answers)))

    if written:
        _index(adr_dir / "README.md", written)
    return written


def _next_number(adr_dir: Path, already: list[WrittenADR] | None = None) -> str:
    numbers = [
        int(match.group(1))
        for path in adr_dir.glob("[0-9]*.md")
        if (match := re.match(r"(\d{4})-", path.name))
    ]
    numbers += [int(adr.number) for adr in already or []]
    return f"{max(numbers, default=0) + 1:04d}"


def _write(adr_dir: Path, document: tuple[WrittenADR, str]) -> WrittenADR:
    record, text = document
    (adr_dir / record.filename).write_text(text, encoding="utf-8")
    return record


def _index(readme: Path, written: list[WrittenADR]) -> None:
    """Append the new rows to the ADR index, under the two that arrive with the template."""
    lines = readme.read_text(encoding="utf-8").splitlines()
    last_row = max(i for i, line in enumerate(lines) if line.startswith("| [0"))
    rows = [f"| [{adr.number}]({adr.filename}) | {adr.title} | decided |" for adr in written]
    lines[last_row + 1 : last_row + 1] = rows
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _storage_adr(number: str, answers: Answers, catalogue: Catalogue) -> tuple[WrittenADR, str]:
    chosen = catalogue.ladder[answers.rung.number]
    neighbour = catalogue.ladder.get(chosen.number + 1) or catalogue.ladder.get(chosen.number - 1)
    title = "Where this project's own data lives"
    exit_condition = answers.rung_exit.strip()

    # The exit condition is the half people skip, so it goes in the section that
    # is read when somebody is wondering whether this still holds — and only
    # there, rather than being spelled twice.
    reconsider = [_bullet(exit_condition)] if exit_condition else []
    if chosen.moves_you_up:
        reconsider.append(
            _bullet(f"{chosen.moves_you_up} — the ladder's own condition for leaving this rung")
        )
    reconsider.append(
        _bullet(
            "There is data here that cannot be regenerated. Climbing is cheap until "
            "then, and that is the real deadline — it is also an escalation trigger "
            "in [ADR 0001](0001-what-kind-of-project-this-is.md)"
        )
    )

    body = f"""
*Written at step 0. The ladder this is taken against is `defaults/storage.md` in
the framework repository, which is deliberately not copied into a project — so
this record cites it rather than restating it.*

## Problem

Two questions come before the ladder and settle most of what a project stores.
Whether a format is **exogenous** — chosen by somebody else, parsed at the edge
into our own types rather than allowed to be the model. And whether **a person
reads and edits it**, which is TOML and the end of the discussion.

What is left is the project's own data, and the rule for it is to take the lowest
rung that holds and to record which one — because a floor that was considered and
a floor that was never examined look identical from inside the repository, and
the person who cannot tell, in a year, is the one who chose it.

## Options considered

### A. Rung {chosen.number} — {chosen.name}

{_fill(chosen.holds + ".")}

**For:** the lowest rung that holds what this project stores.

**Against:** *(what it costs — what the rung above would have given, and when
that starts to bite.)*

### B. Rung {neighbour.number} — {neighbour.name}

{_fill(neighbour.holds + ".")}

**For:** *(the case for the other rung. Climbing early is usually argued from an
invariant that must be enforceable rather than from a volume.)*

**Against:** every rung above the one you need is operational cost paid forever
against a scale that may not arrive — and every rung below is a migration on the
day it does.

## Decision

{_fill(f"**Rung {chosen.number} — {chosen.name}.** " + _why_it_holds())}

Where an invariant is the product, this stops being an implementation detail: a
rule that must never be violable belongs in something that can refuse, and the
choice of store becomes the correctness argument. Test against the real thing —
an in-memory substitute does not implement the constraint the store was chosen
for, and the suite will be green about a guarantee that does not exist.

## Reconsider this if

{chr(10).join(reconsider)}
"""
    filename = f"{number}-where-this-project-s-own-data-lives.md"
    header = HEADER.format(number=number, title=title, today=date.today().isoformat())
    return WrittenADR(number, filename, title), header + body


def _design_adr(number: str, answers: Answers) -> tuple[WrittenADR, str]:
    title = "How design decisions are intermediated"
    house = answers.design_system is DesignSystem.HOUSE
    note = answers.design_note.strip()

    chosen_block = (
        """### A. The house design system, vendored

A copy lives in the repository so the project builds without reaching outside
itself, and what the project needs and the system lacks is pushed back.

**For:** the house default unchanged, so the decision costs a line rather than an
argument. The reskin contract comes with it: if the boundary holds, swapping the
design system is replacing one directory.

**Against:** the vendored copy is a fork the moment it is edited, and a local
change that is never pushed back is a divergence with nothing reporting it."""
        if house
        else """### A. The client's system, elicited into the token layer

Their brand, their colours, the font somebody chose — filled into the token layer
until it is a real design system rather than an implicit one.

**For:** it is the more common situation rather than the exception, and the token
layer is what elicits it. Every gap is a question somebody on their side has to
answer, which is a better conversation than discovering the disagreement after
the interface is built.

**Against:** it is their decision to change, and the elicitation is work before
any of it is visible."""
    )

    other_block = (
        """### B. The client's system, or no system at all

**For:** a client with their own house style will eventually want theirs, and an
application with no system at all ships sooner.

**Against:** no system at all means the decisions are still made — once per
stylesheet, by whoever is nearest, and never recorded."""
        if house
        else """### B. The house design system, vendored

**For:** it is the default, it is known to work, and it costs a line to take.

**Against:** it is not theirs, and a project handed back to a client carrying
somebody else's tokens has to be reskinned by whoever inherits it."""
    )

    citation = (
        "House default unchanged — see `defaults/design-system.md` in the framework\n"
        "repository, which is deliberately not copied into a project."
        if house
        else "The prior is `defaults/design-system.md` in the framework repository. The\n"
        "boundary it describes is unchanged here; what differs is whose decisions sit\n"
        "behind the tokens."
    )

    body = f"""
*Written at step 0, and only because there is an interface to design.*

## Problem

Design decisions are otherwise made by the application, one at a time: a colour
here, a spacing value there, each of them invisible as a decision until somebody
asks what the system would cost to reskin — or a client asks for it in their own
style and the answer is every stylesheet.

It also tangles two jobs that are better kept apart. What the interface **does**
is decided by the journeys and is not negotiable with a designer; what it **looks
like** is the design system's. When those are tangled, every visual change is a
behavioural risk and every behavioural change waits on a designer.

## Options considered

{chosen_block}

{other_block}

## Decision

{citation}

**Tokens are the interface. The application may reference them and may not define
them.** No literal colour, font stack, spacing value, radius, shadow or
breakpoint appears outside the design system's own directory.

**Enforced mechanically**, by a static check in the gate that fails on a literal
outside the boundary and on anything inside it reaching out into the application.
A boundary maintained by everybody remembering is one that two commits eventually
breach. Contrast is asserted on the tokens themselves, where checking it once
covers every use.

{_fill(note or _unwritten_arrangement())}

## Reconsider this if

- **Visual design starts leading rather than following.** The arrangement assumes
  designs arrive after the functional interface exists, which is what makes
  selecting by accessible name safe in the end-to-end tests. A project where the
  design is the specification inverts that, and the tests have to be re-argued
- **The system being adopted is incompatible in kind** — a native platform's
  conventions, or a component library that owns its visual decisions and exposes
  no tokens. Then the boundary is at the component rather than the token, and the
  rule needs restating for that shape rather than dropping
- The remaining conditions are in `defaults/design-system.md` in the framework
  repository
"""
    filename = f"{number}-how-design-decisions-are-intermediated.md"
    header = HEADER.format(number=number, title=title, today=date.today().isoformat())
    return WrittenADR(number, filename, title), header + body


def _why_it_holds() -> str:
    """The one sentence the wizard cannot write, in the shape `defaults/storage.md` asks for.

    Its worked example is *"One process writes, under a million rows, ships inside
    the artifact"* — facts rather than an argument, because what makes the record
    useful later is being able to check whether they are still true.
    """
    return (
        "*(Why this rung holds: what this project stores and what it needs of it, "
        "as facts somebody can check later rather than as an argument. The exit "
        "condition is below — without it, a considered floor is indistinguishable "
        "from an unexamined one.)*"
    )


def _unwritten_arrangement() -> str:
    return (
        "*(Anything specific to this project's arrangement goes here — where the "
        "vendored copy lives, and what is currently owed back to the system.)*"
    )


_fill = markdown.fill
_bullet = markdown.bullet

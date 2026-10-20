"""Render every project kind into a scratch tree and check the links, as the gate.

The unit tests cover a handful of shapes. This covers the product of the answers
that delete files — every kind against a pruning that keeps none, all, or the
overlapping half — because that is where the cross-references break, and a broken
cross-reference is the failure the whole set is built to make impossible.
"""

from __future__ import annotations

import sys
import tempfile
from itertools import product
from pathlib import Path

from teamwork_init import catalogue as catalogue_module
from teamwork_init.links import link_problems
from teamwork_init.model import Answers, DesignSystem, Kind, Rung, default_conditional_docs
from teamwork_init.plan import create


def main() -> int:
    catalogue = catalogue_module.load()
    available = catalogue.conditional_filenames
    selections = {
        "none": frozenset(),
        "all": frozenset(available),
        "the overlapping five": frozenset(
            available
            & {"security.md", "observability.md", "auditability.md", "diagnostics.md", "backups.md"}
        ),
        "one of the five": frozenset({"backups.md"} & available),
    }

    problems: list[str] = []
    rendered = 0
    with tempfile.TemporaryDirectory() as scratch:
        for (kind, rung, design), (label, docs) in product(
            [
                (Kind.SPIKE, Rung.UNDECIDED, DesignSystem.UNDECIDED),
                (Kind.LEARNING, Rung.TOML, DesignSystem.NONE),
                (Kind.ON_SPEC, Rung.SQLITE, DesignSystem.CLIENT),
                (Kind.PRODUCTION, Rung.POSTGRES, DesignSystem.HOUSE),
            ],
            selections.items(),
        ):
            name = f"{kind.name.lower()}-{label.replace(' ', '-')}"
            answers = Answers(
                name=name,
                destination=Path(scratch) / name,
                kind=kind,
                rung=rung,
                design_system=design,
                conditional_docs=docs or default_conditional_docs(kind, rung, "fnox", available),
                git_init=False,
            )
            result = create(answers, catalogue)
            rendered += 1
            problems += [f"{name}: {problem}" for problem in link_problems(result.project)]
            problems += [f"{name}: anchor missed — {miss}" for miss in result.missing_anchors]
            for path in result.project.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                if "*(unset)*" in text or "*(Project name)*" in text:
                    where = path.relative_to(result.project)
                    problems.append(f"{name}: {where} still carries a filled-in placeholder")

    for problem in problems:
        print(problem, file=sys.stderr)
    print(f"{rendered} projects rendered, {len(problems)} problems.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

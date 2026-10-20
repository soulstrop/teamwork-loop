"""Two entry points: the wizard, and the assertion that keeps its anchors honest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import anchors, links
from . import catalogue as catalogue_module
from .catalogue import CatalogueError
from .model import HOUSE_PRIOR


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="teamwork-init",
        description="Step 0 of the framework: hydrate the template set into a new project.",
    )
    parser.add_argument(
        "--framework",
        type=Path,
        default=None,
        help="the framework checkout (default: found upwards from here, or $TEAMWORK_FRAMEWORK)",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="wizard",
        choices=["wizard", "verify"],
        help="wizard (default), or verify that every anchor and parsed table still resolves",
    )
    arguments = parser.parse_args(argv)

    try:
        catalogue = catalogue_module.load(arguments.framework)
    except CatalogueError as failure:
        print(f"teamwork-init: {failure}", file=sys.stderr)
        return 2

    if arguments.command == "verify":
        return verify(catalogue)

    from .app import run  # imported late: `verify` must run without a terminal

    run(catalogue)
    return 0


def verify(catalogue) -> int:
    """Fail loudly when the tool and the documents it renders have drifted apart.

    Three things can rot independently. An anchor is a string the tool holds and the
    template owns, so a template edit can strand it. The tables parsed out of the
    document set are read by shape, so a change to one can leave the wizard quietly
    asking about nothing. And a renamed file or heading breaks every link to it,
    in the framework's own documents as much as the template's. All three are
    checked here, and this runs in `check`.
    """
    problems = anchors.verify(catalogue.template)

    for role, value in HOUSE_PRIOR.items():
        label = {
            "task_runner": "Task runner",
            "toolchain_manager": "Toolchain manager",
            "environment_manager": "Environment manager",
            "dependency_manager": "Dependency manager",
            "language": "Language",
            "secrets": "Secrets",
        }[role]
        stated = catalogue.house_priors.get(label, "")
        if value.lower() not in stated.lower():
            problems.append(
                f"defaults/toolchain.md: the prior for {label} reads {stated!r}, "
                f"which no longer contains the prefilled value {value!r}"
            )

    if not catalogue.dials:
        problems.append("dev-process.md: the dial table parsed to nothing")
    if len(catalogue.ladder) < 2:
        problems.append("defaults/storage.md: the ladder parsed to fewer than two rungs")
    for filename in catalogue.conditional_filenames:
        if not (catalogue.template / "docs" / filename).exists():
            problems.append(f"docs/README.md lists {filename}, which is not in the set")

    documents = links.framework_documents(catalogue.root)
    problems += links.link_problems(catalogue.root, documents)

    for problem in problems:
        print(f"teamwork-init: {problem}", file=sys.stderr)
    if problems:
        print(
            f"\n{len(problems)} problem(s). The tool and the document set have drifted.",
            file=sys.stderr,
        )
        return 1

    print(
        f"{len(anchors.manifest())} anchors resolve, "
        f"{len(catalogue.dials)} dials, {len(catalogue.ladder)} rungs, "
        f"{len(catalogue.conditional_docs)} conditional documents, "
        f"links resolve in {len(documents)} files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

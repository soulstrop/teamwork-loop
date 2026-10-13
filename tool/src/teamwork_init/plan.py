"""Step 0, executed: copy the set, render the answers into it, prune what is unearned.

Everything here is a function of the answers and the framework checkout, so it
runs without a terminal — which is what makes the wizard a front end rather than
the thing itself, and what lets the gate render every project kind on every
commit.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from . import anchors
from .adrs import WrittenADR, write_extra_adrs
from .catalogue import Catalogue
from .model import Answers
from .prune import PruneReport, prune

COMMIT_MESSAGE = "Document set at its initial version"


class InitError(RuntimeError):
    """The destination is not somewhere a project can be created."""


@dataclass
class Result:
    project: Path
    files_written: int = 0
    adrs: list[WrittenADR] = field(default_factory=list)
    pruned: PruneReport = field(default_factory=PruneReport)
    missing_anchors: list[str] = field(default_factory=list)
    git: str = ""


def check_destination(destination: Path, catalogue: Catalogue) -> None:
    """Refuse anywhere that already holds something, or that is the framework itself."""
    destination = destination.expanduser()
    if destination.resolve() == catalogue.root.resolve():
        raise InitError("That is the framework checkout itself.")
    if catalogue.root.resolve() in destination.resolve().parents:
        raise InitError(
            "That is inside the framework checkout. A project is a repository of its own."
        )
    if destination.exists():
        if not destination.is_dir():
            raise InitError(f"{destination} exists and is not a directory.")
        if any(destination.iterdir()):
            raise InitError(f"{destination} already has something in it.")


def create(answers: Answers, catalogue: Catalogue) -> Result:
    """Do it. Raises InitError before touching the disk if the destination is wrong."""
    destination = answers.destination.expanduser()
    check_destination(destination, catalogue)

    shutil.copytree(catalogue.template, destination, dirs_exist_ok=True)
    result = Result(project=destination)

    for relative in sorted(anchors.files()):
        path = destination / relative
        if not path.exists():
            result.missing_anchors.append(f"{relative}: not in the template set")
            continue
        rendered, missing = anchors.apply(relative, path.read_text(encoding="utf-8"), answers)
        path.write_text(rendered, encoding="utf-8")
        result.missing_anchors.extend(missing)
        result.files_written += 1

    result.pruned = prune(destination, set(answers.conditional_docs), catalogue)
    result.adrs = write_extra_adrs(destination, answers, catalogue)

    if answers.git_init:
        result.git = _git(destination)
    return result


def _git(project: Path) -> str:
    """Initialise and commit, so the set's first version is in the history it assumes."""
    try:
        for command in (
            ["git", "init", "--quiet"],
            ["git", "add", "-A"],
            ["git", "commit", "--quiet", "-m", COMMIT_MESSAGE],
        ):
            subprocess.run(command, cwd=project, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        return "git is not installed — the repository was not initialised"
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").strip().splitlines()
        return f"git {' '.join(error.cmd[1:2])} failed: {detail[0] if detail else 'no output'}"
    return f"committed as “{COMMIT_MESSAGE}”"

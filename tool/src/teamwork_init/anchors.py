"""Anchored replacement: the manifest, the renderers, and the assertion that both hold."""

from __future__ import annotations

import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path

from . import markdown
from .model import ROLE_LABELS, Answers, invocation

MANIFEST = Path(__file__).with_name("anchors.toml")
WIDTH = 80


@dataclass(frozen=True)
class Anchor:
    file: str
    find: str
    render: str
    arg: str | None = None


@cache
def manifest() -> tuple[Anchor, ...]:
    data = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
    return tuple(Anchor(**entry) for entry in data["anchor"])


def files() -> set[str]:
    return {anchor.file for anchor in manifest()}


# --- renderers ---------------------------------------------------------------
#
# Each takes the answers and its anchor's `arg`, and returns the replacement —
# or None to leave the placeholder in place, which is what anything only a person
# can write gets.

Renderer = Callable[[Answers, str | None], str | None]
RENDERERS: dict[str, Renderer] = {}


def renderer(name: str) -> Callable[[Renderer], Renderer]:
    def register(function: Renderer) -> Renderer:
        RENDERERS[name] = function
        return function

    return register


def _wrap(text: str, initial: str = "") -> str:
    """Collapse whitespace and refill to the width the document set is written at."""
    return markdown.fill(f"{initial}{text}", WIDTH)


@renderer("project_title")
def _project_title(answers: Answers, _arg: str | None) -> str:
    return f"# {answers.name}"


@renderer("description")
def _description(answers: Answers, _arg: str | None) -> str | None:
    if not answers.description.strip():
        return None
    return _wrap(answers.description.strip())


@renderer("kind_sentence")
def _kind_sentence(answers: Answers, _arg: str | None) -> str:
    return f"**Kind:** {answers.kind.label}."


@renderer("bar_sentence")
def _bar_sentence(answers: Answers, _arg: str | None) -> str | None:
    if not answers.bar.strip():
        return None
    return _wrap(answers.bar.strip(), initial="**The bar:** ")


@renderer("role_row")
def _role_row(answers: Answers, arg: str | None) -> str | None:
    assert arg is not None
    value = getattr(answers, arg).strip()
    if not value:
        return None
    return f"| {ROLE_LABELS[arg]} | {value} |"


@renderer("task_row")
def _task_row(answers: Answers, arg: str | None) -> str | None:
    assert arg is not None
    command = invocation(answers.task_runner, arg)
    if not command:
        return None
    descriptions = {
        "check": "The fast lane: lint, types, fast tests — while working",
        "ship": "**The gate**: `check` + the journey E2E + every cross-reference",
        "fmt": "Format and autofix",
        "tasks": "Everything available, with descriptions",
    }
    return f"| `{arg}` | {descriptions[arg]} | `{command}` |"


@renderer("status_decided")
def _status_decided(_answers: Answers, _arg: str | None) -> str:
    return "- **Status:** decided"


@renderer("today")
def _today(_answers: Answers, _arg: str | None) -> str:
    return f"- **Date:** {date.today().isoformat()}"


@renderer("index_status")
def _index_status(_answers: Answers, arg: str | None) -> str:
    rows = {
        "0001": (
            "| [0001](0001-what-kind-of-project-this-is.md) "
            "| What kind of project this is, and the bar that follows | decided |"
        ),
        "0002": (
            "| [0002](0002-tooling-roles.md) "
            "| What fills the four tool roles, and what the gate covers | decided |"
        ),
    }
    assert arg is not None
    return rows[arg]


@renderer("kind_decision")
def _kind_decision(answers: Answers, _arg: str | None) -> str:
    kind = answers.kind
    lines = [f"**Option {kind.letter} — {kind.option_title.lower()}.**"]
    if answers.bar.strip():
        lines[0] = _wrap(answers.bar.strip(), initial=f"{lines[0]} ")
    else:
        lines.append(
            _wrap(
                "*(Why this kind rather than the ones either side of it, and the bar "
                "in a sentence somebody can hold: what this project owes whoever uses "
                "it, and what it does not. Recorded at initialisation with the kind "
                "chosen and the reasoning left to write — an unwritten bar is the "
                "thing this record exists to prevent.)*"
            )
        )
    return "\n\n".join(lines)


@renderer("tooling_option")
def _tooling_option(answers: Answers, _arg: str | None) -> str:
    """The chosen option's heading, and prompts where its trade-offs go.

    The wizard does not ask for these — the template's own note says the options
    are this project's — so what it writes is the shape of the missing argument
    rather than an invented one.
    """
    return "\n\n".join(
        [
            f"### A. {_roles_sentence(answers)}",
            _wrap(
                "**For:** *(the case for it, in the terms the four roles ask for. Where "
                "this is the house prior taken unchanged, one line and a citation is the "
                "whole answer.)*"
            ),
            _wrap(
                "**Against:** *(the honest cost — what the serious alternative below "
                "would have given, and what it will take to move if this is wrong.)*"
            ),
        ]
    )


@renderer("tooling_decision")
def _tooling_decision(answers: Answers, _arg: str | None) -> str:
    paragraphs = [_wrap(f"{_roles_sentence(answers)}. The language is {answers.language}.")]

    departures = answers.departs_from_house
    if departures:
        listed = "; ".join(
            f"{prior} → {chosen} for the {label(role)}"
            for role, (prior, chosen) in departures.items()
        )
        reason = answers.departure_reason.strip() or (
            "*(Why — a departure recorded without one is indistinguishable from an "
            "accident to the next reader, and to you in four months.)*"
        )
        paragraphs.append(_wrap(f"**Departed from the house default:** {listed}. {reason}"))
        if len(departures) < len(_all_roles()):
            paragraphs.append(
                _wrap(
                    "Every other role is the house default unchanged — see "
                    "`defaults/toolchain.md` in the framework repository, which is "
                    "deliberately not copied into a project."
                )
            )
    else:
        paragraphs.append(
            _wrap(
                "**House default unchanged** — see `defaults/toolchain.md` in the "
                "framework repository, which is deliberately not copied into a "
                "project, so that this decision has one spelling rather than two."
            )
        )

    if answers.secrets.strip():
        paragraphs.append(_wrap(f"**Secrets:** {answers.secrets.strip()}."))

    paragraphs.append(
        _wrap(
            "The invocations are in [`../../CLAUDE.md`](../../CLAUDE.md#commands): "
            "this document is the reasoning, that table is the reference."
        )
    )
    return "\n\n".join(paragraphs)


ROLE_JOBS = {
    "task_runner": "tasks",
    "toolchain_manager": "the toolchain",
    "environment_manager": "environments",
    "dependency_manager": "dependencies",
}


def _all_roles() -> tuple[str, ...]:
    return (*ROLE_JOBS, "language", "secrets")


def label(role: str) -> str:
    return ROLE_LABELS.get(role, role.replace("_", " ")).lower()


def _roles_sentence(answers: Answers) -> str:
    """The four roles as one line, collapsing the common case of one tool filling several.

    Phrased by the job rather than by the role — *mise for tasks, the toolchain
    and environments* — because that is how `defaults/README.md` writes the line
    it expects to see cited back.
    """
    by_tool: dict[str, list[str]] = {}
    for role, job in ROLE_JOBS.items():
        tool = getattr(answers, role).strip() or "*(unset)*"
        by_tool.setdefault(tool, []).append(job)
    parts = []
    for tool, jobs in by_tool.items():
        if len(jobs) == 1:
            parts.append(f"{tool} for {jobs[0]}")
        else:
            parts.append(f"{tool} for {', '.join(jobs[:-1])} and {jobs[-1]}")
    return "; ".join(parts)


# --- application and verification --------------------------------------------


def apply(relative_path: str, text: str, answers: Answers) -> tuple[str, list[str]]:
    """Render every anchor for one file. Returns the new text and any anchors that missed."""
    missing: list[str] = []
    for anchor in manifest():
        if anchor.file != relative_path:
            continue
        if anchor.find not in text:
            missing.append(f"{anchor.file}: {_first_line(anchor.find)}")
            continue
        replacement = RENDERERS[anchor.render](answers, anchor.arg)
        if replacement is None:
            continue
        text = text.replace(anchor.find, replacement, 1)
    return text, missing


def verify(template: Path) -> list[str]:
    """Assert every anchor still occurs exactly once in the template it names.

    This is the mechanical half of the bargain that keeps `template/` directly
    copyable: the anchors are strings living in two places, so something has to
    fail when one of them moves. It runs in `check`.
    """
    problems: list[str] = []
    for anchor in manifest():
        if anchor.render not in RENDERERS:
            problems.append(f"{anchor.file}: no renderer named {anchor.render!r}")
        path = template / anchor.file
        if not path.exists():
            problems.append(f"{anchor.file}: no such file in the template set")
            continue
        occurrences = path.read_text(encoding="utf-8").count(anchor.find)
        if occurrences != 1:
            problems.append(
                f"{anchor.file}: anchor occurs {occurrences} times, expected once "
                f"— {_first_line(anchor.find)}"
            )
    return problems


def _first_line(text: str) -> str:
    line = text.strip().splitlines()[0]
    return line if len(line) <= 60 else line[:57] + "…"

"""What the wizard collects, and the vocabulary it collects it in.

Nothing here restates the framework's own content. The kinds, the dials and the
conditions under which a conditional document earns its place are read out of the
document set at runtime — see `catalogue.py`. What lives here is the shape of an
answer and the tool's own judgement about what to pre-select, which is the tool's
to own.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# The house priors, as concrete values the wizard can prefill.
#
# defaults/toolchain.md states these in prose; these are the machine-usable
# reading of that prose, not a second copy of it. `verify` asserts that each
# value below still appears in the corresponding row of that table, so a change
# to the default fails the check rather than drifting silently.
HOUSE_PRIOR = {
    "task_runner": "mise",
    "toolchain_manager": "mise",
    "environment_manager": "mise",
    "dependency_manager": "uv",
    "language": "Python",
    "secrets": "fnox",
}

ROLE_LABELS = {
    "task_runner": "Task runner",
    "toolchain_manager": "Toolchain manager",
    "environment_manager": "Environment manager",
    "dependency_manager": "Dependency manager",
}


class Kind(Enum):
    """The four project kinds of ADR 0001, with the option letter each carries there."""

    SPIKE = ("spike", "A", "Spike or proof of concept")
    LEARNING = ("learning", "B", "Learning")
    ON_SPEC = ("on spec", "C", "On spec")
    PRODUCTION = ("production", "D", "Production")

    def __init__(self, label: str, letter: str, option_title: str) -> None:
        self.label = label
        self.letter = letter
        self.option_title = option_title

    @property
    def dial_column(self) -> str:
        """The heading this kind has in the dial table of `dev-process.md`."""
        return {
            Kind.SPIKE: "Spike / POC",
            Kind.LEARNING: "Learning",
            Kind.ON_SPEC: "On spec",
            Kind.PRODUCTION: "Production",
        }[self]


class Rung(Enum):
    """A position on the ladder in `defaults/storage.md`.

    Only the number lives here. What each rung holds and what moves you up it are
    read out of that file at runtime — see `catalogue.parse_storage_ladder` —
    because the ladder has one home and this is not it. UNDECIDED means the
    question was left open and no storage ADR is written.
    """

    UNDECIDED = -1
    NOTHING = 0
    TOML = 1
    SQLITE = 2
    POSTGRES = 3
    SPECIALISED = 4

    @property
    def number(self) -> int:
        return self.value

    @property
    def persists_data(self) -> bool:
        return self.value >= 2


class DesignSystem(Enum):
    """What intermediates design decisions — the prior is in `defaults/design-system.md`."""

    UNDECIDED = "Not decided yet"
    HOUSE = "The house design system, vendored"
    CLIENT = "A client's system, elicited into the token layer"
    NONE = "No interface to design"


@dataclass(frozen=True)
class Answers:
    """Everything the wizard collects. Blank strings mean 'leave the placeholder'."""

    name: str = ""
    destination: Path = field(default_factory=lambda: Path.cwd())
    description: str = ""
    kind: Kind = Kind.SPIKE
    bar: str = ""
    task_runner: str = HOUSE_PRIOR["task_runner"]
    toolchain_manager: str = HOUSE_PRIOR["toolchain_manager"]
    environment_manager: str = HOUSE_PRIOR["environment_manager"]
    dependency_manager: str = HOUSE_PRIOR["dependency_manager"]
    language: str = HOUSE_PRIOR["language"]
    secrets: str = HOUSE_PRIOR["secrets"]
    departure_reason: str = ""
    rung: Rung = Rung.UNDECIDED
    rung_exit: str = ""
    design_system: DesignSystem = DesignSystem.UNDECIDED
    design_note: str = ""
    conditional_docs: frozenset[str] = frozenset()
    git_init: bool = True

    @property
    def slug(self) -> str:
        return slugify(self.name)

    @property
    def target(self) -> Path:
        return self.destination

    @property
    def departs_from_house(self) -> dict[str, tuple[str, str]]:
        """Role -> (house prior, what this project chose), for every role that differs."""
        chosen = {
            "task_runner": self.task_runner,
            "toolchain_manager": self.toolchain_manager,
            "environment_manager": self.environment_manager,
            "dependency_manager": self.dependency_manager,
            "language": self.language,
            "secrets": self.secrets,
        }
        return {
            role: (HOUSE_PRIOR[role], value)
            for role, value in chosen.items()
            if value.strip().lower() != HOUSE_PRIOR[role].lower()
        }


def slugify(name: str) -> str:
    """A directory name from a project name. Empty in, empty out."""
    normalised = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalised).strip("-").lower()
    return slug


def invocation(runner: str, task: str) -> str:
    """How a task is invoked under a given runner.

    Every document in the set writes task names rather than commands, so this is
    the one place that knows the difference — and it is a table of shapes rather
    than of tools, so an unknown runner still gets a plausible line to correct.
    """
    tool = runner.strip()
    if not tool:
        return ""
    first = tool.split()[0].lower()
    if first in {"just", "make", "cargo", "go", "task"}:
        return f"{tool} {task}"
    if first in {"npm", "pnpm", "yarn", "mise", "uv", "poetry", "pdm", "hatch", "rake"}:
        return f"{tool} run {task}"
    return f"{tool} {task}"


def default_conditional_docs(
    kind: Kind, rung: Rung, secrets: str, available: set[str]
) -> frozenset[str]:
    """Which conditional documents to pre-select, from what has been answered so far.

    This is the tool's judgement rather than the framework's: every condition in
    `docs/README.md` is about a fact the wizard has not asked for, so these are
    the ones the earlier answers make likely. All of them are togglable, and a
    wrong guess costs one keystroke — which is the right side to err on, since a
    document deleted at step 0 is cheaper to restore than one nobody notices is
    seeded and empty.
    """
    chosen: set[str] = set()
    if kind is Kind.PRODUCTION:
        chosen |= {"deployment.md", "observability.md", "diagnostics.md"}
    if kind is Kind.ON_SPEC:
        chosen |= {"demo.md"}
    if rung.persists_data:
        chosen |= {"backups.md"}
        if kind in {Kind.ON_SPEC, Kind.PRODUCTION}:
            chosen |= {"security.md"}
    if secrets.strip() and secrets.strip().lower() not in {"none", "n/a", "-"}:
        chosen |= {"security.md"}
    return frozenset(chosen & available)

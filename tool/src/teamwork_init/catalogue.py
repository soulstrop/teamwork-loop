"""What the wizard knows, read out of the document set rather than restated.

The dial table, the conditions under which a conditional document earns its
place, and the house priors for the four tool roles all have one home each in the
framework. This module reads them at the moment they are needed. That keeps the
tool's prompts and the documents they are about from ever disagreeing — and when
a table is edited into a shape this cannot read, `verify` fails, which is the
loud half of the bargain.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

MARKER_FILES = ("USING-THIS-FRAMEWORK.md", "template", "defaults")


class CatalogueError(RuntimeError):
    """A table the tool depends on is missing, moved, or no longer parseable."""


def find_framework(start: Path | None = None) -> Path:
    """Locate the framework repository: the flag, the environment, then upwards."""
    override = os.environ.get("TEAMWORK_FRAMEWORK")
    if override:
        root = Path(override).expanduser().resolve()
        if not is_framework(root):
            raise CatalogueError(f"TEAMWORK_FRAMEWORK={root} is not a framework checkout")
        return root
    candidates = [start or Path.cwd(), Path(__file__).resolve()]
    for candidate in candidates:
        for directory in [candidate, *candidate.parents]:
            if is_framework(directory):
                return directory
    raise CatalogueError(
        "No framework checkout found. Pass --framework /path/to/teamwork-loop, "
        "or set TEAMWORK_FRAMEWORK."
    )


def is_framework(directory: Path) -> bool:
    return all((directory / name).exists() for name in MARKER_FILES)


@dataclass(frozen=True)
class ConditionalDoc:
    """A document that is deleted unless the project has the thing."""

    filename: str
    condition: str


@dataclass(frozen=True)
class LadderRung:
    """One rung of the storage ladder, as `defaults/storage.md` states it."""

    number: int
    name: str
    holds: str
    moves_you_up: str

    @property
    def label(self) -> str:
        return f"{self.number}. {self.name} — {self.holds}"


@dataclass(frozen=True)
class Catalogue:
    root: Path
    dials: dict[str, dict[str, str]]
    conditional_docs: tuple[ConditionalDoc, ...]
    house_priors: dict[str, str]
    ladder: dict[int, LadderRung]

    @property
    def template(self) -> Path:
        return self.root / "template"

    @property
    def conditional_filenames(self) -> set[str]:
        return {doc.filename for doc in self.conditional_docs}

    def dial_column(self, heading: str) -> dict[str, str]:
        missing = [dial for dial, columns in self.dials.items() if heading not in columns]
        if missing:
            raise CatalogueError(f"Dial table has no column {heading!r} for {missing}")
        return {dial: columns[heading] for dial, columns in self.dials.items()}


def load(root: Path | None = None) -> Catalogue:
    framework = root or find_framework()
    return Catalogue(
        root=framework,
        dials=parse_dial_table(framework / "template" / "docs" / "dev-process.md"),
        conditional_docs=parse_conditional_table(framework / "template" / "docs" / "README.md"),
        house_priors=parse_house_priors(framework / "defaults" / "toolchain.md"),
        ladder=parse_storage_ladder(framework / "defaults" / "storage.md"),
    )


def _rows(table: list[str]) -> list[list[str]]:
    return [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in table]


def _table_after(path: Path, heading: str) -> list[str]:
    """The first markdown table appearing after a line containing `heading`."""
    if not path.exists():
        raise CatalogueError(f"{path} is missing")
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next((i for i, line in enumerate(lines) if heading in line), None)
    if start is None:
        raise CatalogueError(f"{path.name} no longer contains {heading!r}")
    table: list[str] = []
    for line in lines[start:]:
        if line.startswith("|"):
            table.append(line)
        elif table:
            break
    if len(table) < 3:
        raise CatalogueError(f"No table found after {heading!r} in {path.name}")
    return table


def parse_dial_table(path: Path) -> dict[str, dict[str, str]]:
    """`dev-process.md`'s dial table: dial -> {kind column -> setting}."""
    table = _table_after(path, "### The dials, and what sets them")
    header, _separator, *body = _rows(table)
    columns = header[1:]
    dials: dict[str, dict[str, str]] = {}
    for row in body:
        if len(row) != len(header) or not row[0]:
            continue
        dials[row[0]] = dict(zip(columns, row[1:], strict=True))
    if not dials:
        raise CatalogueError(f"Dial table in {path.name} parsed to nothing")
    return dials


def parse_conditional_table(path: Path) -> tuple[ConditionalDoc, ...]:
    """`docs/README.md`'s conditional table: the filename and the condition, verbatim."""
    table = _table_after(path, "**Conditional — delete unless the project has the thing.**")
    _header, _separator, *body = _rows(table)
    docs: list[ConditionalDoc] = []
    for row in body:
        if len(row) < 2:
            continue
        match = re.search(r"\(([^)]+\.md)\)", row[0])
        if not match:
            continue
        docs.append(ConditionalDoc(filename=match.group(1), condition=row[1]))
    if not docs:
        raise CatalogueError(f"Conditional table in {path.name} parsed to nothing")
    return tuple(docs)


def parse_storage_ladder(path: Path) -> dict[int, LadderRung]:
    """`defaults/storage.md`'s ladder: rung number -> what it holds and what moves you up."""
    table = _table_after(path, "## The ladder")
    _header, _separator, *body = _rows(table)
    ladder: dict[int, LadderRung] = {}
    for row in body:
        if len(row) < 3:
            continue
        match = re.match(r"\*\*(\d+)\.\s*(.+?)\*\*", row[0])
        if not match:
            continue
        number = int(match.group(1))
        ladder[number] = LadderRung(
            number=number,
            name=match.group(2).strip(),
            holds=row[1],
            moves_you_up=row[2].strip(" —-"),
        )
    if not ladder:
        raise CatalogueError(f"Storage ladder in {path.name} parsed to nothing")
    return ladder


def parse_house_priors(path: Path) -> dict[str, str]:
    """`defaults/toolchain.md`'s role table: role name -> the prior, as written."""
    table = _table_after(path, "## The roles, and what fills them")
    _header, _separator, *body = _rows(table)
    priors = {row[0]: row[1] for row in body if len(row) >= 2 and row[0]}
    if not priors:
        raise CatalogueError(f"Role table in {path.name} parsed to nothing")
    return priors

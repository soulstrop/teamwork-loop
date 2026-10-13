"""Deleting the conditional documents this project has not earned, and the links to them.

A conditional document is deleted unless the project has the thing. Deleting the
file is the easy half; the set cross-references, so the other half is that
`docs/README.md` still lists it and four of the documents that survive still link
to it. A dangling link is exactly what the link checker in the `ship` task exists
to catch, so leaving them is not an option.

**A link to a deleted document is unlinked rather than removed.** The sentences
that point at these files are boundary statements — *not the job: `backups.md`,
which is …* — and the boundary is still true when the document is absent. Cutting
the sentence would delete the only thing telling a reader where that material
goes if the condition later fires. Every unlink is reported, so nothing happens
quietly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .catalogue import Catalogue

FIVE_WAY_HEADING = "**Five of those sit close together and are deliberately separate**"
RETENTION_PARAGRAPH = "**Three of them capture data at runtime and the mechanisms overlap.**"


@dataclass
class PruneReport:
    deleted: list[str] = field(default_factory=list)
    unlinked: list[str] = field(default_factory=list)
    rows_removed: list[str] = field(default_factory=list)
    blocks_removed: list[str] = field(default_factory=list)


def prune(project: Path, keep: set[str], catalogue: Catalogue) -> PruneReport:
    """Delete unselected conditional documents from an already-copied project tree."""
    report = PruneReport()
    doomed = sorted(catalogue.conditional_filenames - keep)
    if not doomed:
        return report

    for filename in doomed:
        path = project / "docs" / filename
        if path.exists():
            path.unlink()
            report.deleted.append(f"docs/{filename}")

    index = project / "docs" / "README.md"
    if index.exists():
        index.write_text(_rewrite_index(index.read_text(encoding="utf-8"), doomed, report), "utf-8")

    for path in sorted(project.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        rewritten = _unlink(original, doomed, path.relative_to(project).as_posix(), report)
        if rewritten != original:
            path.write_text(rewritten, encoding="utf-8")

    return report


def _rewrite_index(text: str, doomed: list[str], report: PruneReport) -> str:
    """Drop the table rows naming a deleted document, and any block left with no subject."""
    kept_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("|") and any(_names(line, filename) for filename in doomed):
            report.rows_removed.append(line.strip())
            continue
        kept_lines.append(line)
    text = "\n".join(kept_lines)

    five = {"security.md", "observability.md", "auditability.md", "diagnostics.md", "backups.md"}
    if len(five - set(doomed)) < 2:
        text = _drop_block(text, FIVE_WAY_HEADING, report, "the five-way comparison")
    if "diagnostics.md" in doomed:
        text = _drop_block(text, RETENTION_PARAGRAPH, report, "the retention paragraph")
    return text.rstrip("\n") + "\n"


def _drop_block(text: str, heading: str, report: PruneReport, name: str) -> str:
    """Remove the paragraph starting with `heading`, plus a table immediately following it."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith(heading[:40])), None)
    if start is None:
        return text

    end = start
    while end < len(lines) and lines[end].strip():  # the paragraph
        end += 1
    if end + 1 < len(lines) and lines[end + 1].startswith("|"):  # and its table, if it has one
        end += 1
        while end < len(lines) and lines[end].startswith("|"):
            end += 1
        end -= 1

    report.blocks_removed.append(name)
    remaining = lines[:start] + lines[end + 2 :]  # the block and the blank line after it
    return "\n".join(remaining)


def _names(line: str, filename: str) -> bool:
    return re.search(rf"[`(/]{re.escape(filename)}\b", line) is not None


def _unlink(text: str, doomed: list[str], where: str, report: PruneReport) -> str:
    """Turn `[text](path/to/deleted.md)` into its text, so no link dangles."""
    for filename in doomed:
        pattern = re.compile(rf"\[([^\]]+)\]\((?:\.{{1,2}}/)*{re.escape(filename)}(?:#[^)]*)?\)")
        for match in pattern.finditer(text):
            report.unlinked.append(f"{where}: {match.group(0)}")
        text = pattern.sub(lambda match: match.group(1), text)
    return text

"""Does every relative link resolve, down to the heading it names?

A renamed file or a reworded heading breaks a cross-reference silently: the
document still renders, and the link only fails for the reader who follows it.
Nothing else reads every link, so this does, in two places. `verify` runs it over
the framework checkout, where the renames happen; the tests run it over rendered
projects, because the wizard deletes files on purpose and is the likeliest thing
to strand a link.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
EXTERNAL = ("http://", "https://", "mailto:")
FENCE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN = re.compile(r"`[^`]*`")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def slug(heading: str) -> str:
    """The anchor GitHub gives a heading: its text, lowercased, punctuation gone."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    text = re.sub(r"[`*_]", "", text).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def _prose(text: str) -> Iterable[tuple[int, str]]:
    """The numbered lines a reader sees as prose: code blocks and code spans left out."""
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield number, CODE_SPAN.sub("code", line)  # not "": [`x.md`](x.md) must keep its text


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    for _, line in _prose(path.read_text(encoding="utf-8")):
        match = HEADING.match(line)
        if match:
            base = slug(match.group(1))
            count = seen.get(base, 0)
            seen[base] = count + 1
            if count:
                seen[f"{base}-{count}"] = 1
    return set(seen)


def link_problems(root: Path, files: Iterable[Path] | None = None) -> list[str]:
    """Every link in `files` (default: all markdown under `root`) that resolves to nothing."""
    problems: list[str] = []
    cache: dict[Path, set[str]] = {}
    for path in sorted(files if files is not None else root.rglob("*.md")):
        for number, line in _prose(path.read_text(encoding="utf-8")):
            for _, target in LINK.findall(line):
                if target.startswith(EXTERNAL):
                    continue
                name, _, fragment = target.partition("#")
                resolved = (path.parent / name).resolve() if name else path
                where = f"{path.relative_to(root).as_posix()}:{number}: ({target})"
                if not resolved.exists():
                    problems.append(f"{where} resolves to nothing")
                elif fragment and resolved.suffix == ".md":
                    if resolved not in cache:
                        cache[resolved] = anchors(resolved)
                    if fragment not in cache[resolved]:
                        problems.append(f"{where} names a heading that is not there")
    return problems


def framework_documents(root: Path) -> list[Path]:
    """The markdown a framework checkout publishes: the root files and the four areas."""
    documents = list(root.glob("*.md"))
    for area in ("template", "defaults", "design", "tool"):
        documents += [p for p in (root / area).rglob("*.md") if ".venv" not in p.parts]
    return documents

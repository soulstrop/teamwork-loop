"""Does every relative link in a rendered project resolve?

The set's own `ship` task carries a link checker, for the reason `docs/README.md`
gives: a renamed file breaks a cross-reference silently, and nothing else reads
every link. This tool deletes files on purpose, which makes it the most likely
thing in the framework to produce exactly that failure — so the same check runs
over what it produces.
"""

from __future__ import annotations

import re
from pathlib import Path

LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")


def link_problems(project: Path) -> list[str]:
    problems: list[str] = []
    for path in sorted(project.rglob("*.md")):
        for text, target in LINK.findall(path.read_text(encoding="utf-8")):
            if target.startswith(EXTERNAL):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                where = path.relative_to(project).as_posix()
                problems.append(f"{where}: [{text}]({target}) resolves to nothing")
    return problems

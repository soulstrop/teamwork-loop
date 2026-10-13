"""Filling prose to the width the document set is written at, without breaking a link.

Wrapping is not cosmetic here. Every generated paragraph sits in a file a person
will edit next to hand-written ones, and a paragraph on one long line makes the
next diff of that file unreadable — the whole paragraph shows as changed when one
word did.
"""

from __future__ import annotations

import re
import textwrap

WIDTH = 80
LINK = re.compile(r"\[[^\]]+\]\([^)\s]+\)")
GLUE = "\x00"


def fill(text: str, width: int = WIDTH) -> str:
    """Collapse whitespace and refill, keeping any markdown link on one line.

    A link broken across a newline still renders, but it stops being greppable and
    stops being one thing to a reader scanning the source — which is most of what
    reading a document set is.
    """
    protected = LINK.sub(lambda match: match.group(0).replace(" ", GLUE), " ".join(text.split()))
    filled = textwrap.fill(protected, width=width, break_long_words=False, break_on_hyphens=False)
    return filled.replace(GLUE, " ")


def bullet(text: str, width: int = WIDTH - 2) -> str:
    return textwrap.indent(fill(text, width), "  ").replace("  ", "- ", 1)


EMPHASIS = re.compile(r"\*\*|`|(?<!\w)\*|\*(?!\w)")


def plain(text: str) -> str:
    """Markdown as a terminal should show it.

    The prompts quote the document set verbatim so the wizard cannot disagree
    with it, and the document set is written in markdown. Showing `**mise**` to
    somebody in a terminal is showing them the source of a sentence rather than
    the sentence.
    """
    unlinked = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return EMPHASIS.sub("", unlinked).strip()

from __future__ import annotations

from pathlib import Path

from teamwork_init.links import link_problems, slug


def test_slug_matches_github_for_the_headings_the_set_writes():
    assert slug("7. The handoff, and the residue loop") == "7-the-handoff-and-the-residue-loop"
    assert slug("4. The journey loop — eight steps") == "4-the-journey-loop--eight-steps"
    assert slug("The `step-8` skill") == "the-step-8-skill"


def write(root: Path, name: str, text: str) -> None:
    (root / name).write_text(text, encoding="utf-8")


def test_a_missing_file_and_a_missing_heading_are_both_problems(tmp_path):
    write(tmp_path, "a.md", "# Here\n\n## Twice\n\n## Twice\n")
    write(
        tmp_path,
        "b.md",
        "[`a.md`](a.md) [x](a.md#here) [x](a.md#twice-1) [x](#local)\n\n## Local\n"
        "[x](gone.md) [x](a.md#gone) [x](https://example.com/gone)\n",
    )
    assert link_problems(tmp_path) == [
        "b.md:4: (gone.md) resolves to nothing",
        "b.md:4: (a.md#gone) names a heading that is not there",
    ]


def test_links_inside_code_are_examples_not_links(tmp_path):
    write(tmp_path, "a.md", "```\n[x](gone.md)\n```\n\n`[x](gone.md)`\n")
    assert link_problems(tmp_path) == []

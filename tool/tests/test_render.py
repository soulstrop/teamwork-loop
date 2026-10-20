from __future__ import annotations

from pathlib import Path

import pytest

from teamwork_init import anchors
from teamwork_init import catalogue as catalogue_module
from teamwork_init.links import link_problems
from teamwork_init.model import (
    Answers,
    DesignSystem,
    Kind,
    Rung,
    default_conditional_docs,
    invocation,
    slugify,
)
from teamwork_init.plan import InitError, create


@pytest.fixture(scope="session")
def catalogue():
    return catalogue_module.load()


@pytest.fixture
def production(tmp_path: Path, catalogue) -> Answers:
    return Answers(
        name="Rota Planner",
        destination=tmp_path / "rota-planner",
        description="Builds a fortnight of shifts that nobody has to argue about.",
        kind=Kind.PRODUCTION,
        bar="It owes whoever is on shift a rota that is correct; it owes nobody a mobile app.",
        rung=Rung.POSTGRES,
        rung_exit="A read shape Postgres is measurably too slow for, and measured.",
        design_system=DesignSystem.HOUSE,
        conditional_docs=default_conditional_docs(
            Kind.PRODUCTION, Rung.POSTGRES, "fnox", catalogue.conditional_filenames
        ),
        git_init=False,
    )


def test_the_anchors_all_resolve_against_the_template(catalogue):
    assert anchors.verify(catalogue.template) == []


def test_slug_and_invocation():
    assert slugify("Rota Planner") == "rota-planner"
    assert slugify("  Café / Bar!  ") == "cafe-bar"
    assert invocation("mise", "ship") == "mise run ship"
    assert invocation("just", "ship") == "just ship"
    assert invocation("", "ship") == ""
    assert invocation("nushell-thing", "ship") == "nushell-thing ship"


def test_a_rendered_project_carries_the_answers(production, catalogue):
    result = create(production, catalogue)
    project = result.project

    claude = (project / "CLAUDE.md").read_text()
    assert "**Kind:** production." in claude
    assert "*(unset)*" not in claude
    assert "| `mise run ship` |" in claude
    assert "It owes whoever is on shift" in claude

    readme = (project / "README.md").read_text()
    assert readme.startswith("# Rota Planner\n")
    assert "fortnight of shifts" in readme

    adr1 = (project / "docs/adr/0001-what-kind-of-project-this-is.md").read_text()
    assert "- **Status:** decided" in adr1
    assert "**Option D — production.**" in adr1
    assert "YYYY-MM-DD" not in adr1

    adr2 = (project / "docs/adr/0002-tooling-roles.md").read_text()
    assert "House default unchanged" in adr2
    assert "*(what this project chose)*" not in adr2

    index = (project / "docs/adr/README.md").read_text()
    assert "| proposed |" not in index
    assert result.missing_anchors == []


def test_the_storage_and_design_records_get_written_and_indexed(production, catalogue):
    result = create(production, catalogue)
    numbers = [adr.number for adr in result.adrs]
    assert numbers == ["0003", "0004"]

    storage = (result.project / "docs/adr/0003-where-this-project-s-own-data-lives.md").read_text()
    assert "**Rung 3 — Postgres.**" in storage
    assert "measurably too slow" in storage

    index = (result.project / "docs/adr/README.md").read_text()
    assert "[0003](0003-where-this-project-s-own-data-lives.md)" in index
    assert "[0004](0004-how-design-decisions-are-intermediated.md)" in index


def test_an_undecided_answer_writes_no_record(tmp_path, catalogue):
    answers = Answers(name="Spike", destination=tmp_path / "spike", kind=Kind.SPIKE, git_init=False)
    result = create(answers, catalogue)
    assert result.adrs == []
    assert sorted(p.name for p in (result.project / "docs/adr").glob("0*.md")) == [
        "0001-what-kind-of-project-this-is.md",
        "0002-tooling-roles.md",
    ]


def test_blank_answers_leave_the_placeholders_alone(tmp_path, catalogue):
    answers = Answers(name="Spike", destination=tmp_path / "spike", git_init=False)
    project = create(answers, catalogue).project
    assert "**The bar:** *(one sentence" in (project / "CLAUDE.md").read_text()
    assert "*One or two sentences" in (project / "README.md").read_text()


def test_departing_from_a_prior_without_a_reason_leaves_the_prompt(tmp_path, catalogue):
    answers = Answers(
        name="Spike",
        destination=tmp_path / "spike",
        task_runner="just",
        git_init=False,
    )
    adr = (create(answers, catalogue).project / "docs/adr/0002-tooling-roles.md").read_text()
    assert "**Departed from the house default:** mise → just for the task runner" in adr
    assert "indistinguishable from an" in adr
    assert (
        "`just ship`"
        in (
            create(
                Answers(name="S", destination=tmp_path / "s2", task_runner="just", git_init=False),
                catalogue,
            ).project
            / "CLAUDE.md"
        ).read_text()
    )


def test_pruning_deletes_the_documents_and_leaves_no_dangling_link(tmp_path, catalogue):
    answers = Answers(
        name="Spike",
        destination=tmp_path / "spike",
        kind=Kind.SPIKE,
        conditional_docs=frozenset(),
        git_init=False,
    )
    result = create(answers, catalogue)
    project = result.project

    assert len(result.pruned.deleted) == len(catalogue.conditional_docs)
    assert not list((project / "docs").glob("backups.md"))
    assert link_problems(project) == []

    index = (project / "docs/README.md").read_text()
    assert "deployment.md" not in index
    assert "Five of those sit close together" not in index
    assert "Three of them capture data at runtime" not in index
    # The boundary statement survives its link.
    journey = (project / "docs/journeys/TEMPLATE.md").read_text()
    assert "`../diagnostics.md`" in journey
    assert "](../diagnostics.md)" not in journey


def test_keeping_everything_changes_nothing(tmp_path, catalogue):
    answers = Answers(
        name="Everything",
        destination=tmp_path / "everything",
        conditional_docs=frozenset(catalogue.conditional_filenames),
        git_init=False,
    )
    result = create(answers, catalogue)
    assert result.pruned.deleted == []
    assert result.pruned.unlinked == []
    assert link_problems(result.project) == []


def test_partial_pruning_keeps_the_surviving_neighbours_linked(tmp_path, catalogue):
    answers = Answers(
        name="Half",
        destination=tmp_path / "half",
        conditional_docs=frozenset({"security.md", "observability.md", "auditability.md"}),
        git_init=False,
    )
    project = create(answers, catalogue).project
    assert link_problems(project) == []
    index = (project / "docs/README.md").read_text()
    assert "Five of those sit close together" in index  # three of the five survive
    assert "Three of them capture data at runtime" not in index  # diagnostics.md did not
    assert "| `security.md` |" in index
    assert "| `backups.md` |" not in index


def test_the_defaults_follow_from_the_earlier_answers(catalogue):
    available = catalogue.conditional_filenames
    spike = default_conditional_docs(Kind.SPIKE, Rung.NOTHING, "none", available)
    assert spike == frozenset()

    production = default_conditional_docs(Kind.PRODUCTION, Rung.POSTGRES, "fnox", available)
    assert {
        "deployment.md",
        "observability.md",
        "diagnostics.md",
        "backups.md",
        "security.md",
    } <= production
    assert "demo.md" not in production
    assert "ui-brief.md" not in production

    assert "demo.md" in default_conditional_docs(Kind.ON_SPEC, Rung.TOML, "none", available)


def test_it_refuses_a_destination_that_already_holds_something(tmp_path, catalogue):
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "something").write_text("here")
    with pytest.raises(InitError, match="already has something"):
        create(Answers(name="X", destination=occupied), catalogue)


def test_it_refuses_to_write_inside_the_framework_itself(catalogue):
    with pytest.raises(InitError, match="framework checkout itself"):
        create(Answers(name="X", destination=catalogue.root), catalogue)
    with pytest.raises(InitError, match="inside the framework"):
        create(Answers(name="X", destination=catalogue.root / "template" / "nested"), catalogue)


def test_git_leaves_the_set_at_its_initial_version(tmp_path, catalogue):
    pytest.importorskip("subprocess")
    result = create(
        Answers(name="Committed", destination=tmp_path / "committed", git_init=True), catalogue
    )
    assert (result.project / ".git").is_dir()
    assert "committed" in result.git or "failed" in result.git or "not installed" in result.git


def test_prose_is_filled_without_breaking_a_link():
    from teamwork_init.markdown import fill, plain

    text = fill(
        "A sentence long enough to wrap, ending in a reference to "
        "[ADR 0001](0001-what-kind-of-project-this-is.md) that must not be split."
    )
    assert all(len(line) <= 80 for line in text.splitlines())
    assert "[ADR 0001](0001-what-kind-of-project-this-is.md)" in text

    assert plain("**mise**") == "mise"
    assert plain("**language-specific** — `uv` for Python") == "language-specific — uv for Python"
    assert plain("Somebody will ask *who did this*") == "Somebody will ask who did this"
    assert plain("[`data.md`](data.md) is the map") == "data.md is the map"

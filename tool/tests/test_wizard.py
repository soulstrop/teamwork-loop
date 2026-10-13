"""Driving the wizard itself, since a front end that cannot be started is not one.

Textual's pilot runs the app headless, so these are the same key presses a person
would make. They are slower than the render tests and cover less — what they
cover is that every screen composes, that the answers survive the walk from step
to step, and that the two things easiest to get wrong in a wizard both hold: back
does not lose what was typed, and a refusal keeps you on the screen that raised
it.

Note the pause between typing the name and typing the destination. The name
rewrites the destination as you type, right up until the destination is edited by
hand, and setting both in the same tick races that — which is a real ordering,
just not one a person can hit at typing speed.
"""

from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from pathlib import Path

from textual.widgets import Input, RadioSet, SelectionList

from teamwork_init import catalogue as catalogue_module
from teamwork_init.app import ConfirmStep, DoneScreen, NameStep, WizardApp
from teamwork_init.model import Kind, Rung


def drive(coroutine: Coroutine) -> None:
    asyncio.run(coroutine)


async def name_it(pilot, name: str, destination: Path) -> None:
    screen = pilot.app.screen
    screen.query_one("#name", Input).value = name
    await pilot.pause()
    screen.query_one("#destination", Input).value = str(destination)
    await pilot.pause()


async def advance(pilot, times: int = 1) -> None:
    for _ in range(times):
        await pilot.press("ctrl+n")
        await pilot.pause()


def test_walking_through_every_step_writes_a_project(tmp_path: Path) -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            await name_it(pilot, "Rota Planner", tmp_path / "rota-planner")
            await advance(pilot)

            await pilot.press("down", "down", "down", "enter")  # production
            app.screen.query_one("#bar", Input).value = "A rota that is correct."
            await advance(pilot, 2)  # tooling, then storage

            await pilot.press("down", "down", "down", "enter")  # rung 2, SQLite
            await advance(pilot, 3)  # design system, documents, confirm
            assert isinstance(app.screen, ConfirmStep)

            await advance(pilot)
            assert isinstance(app.screen, DoneScreen)

        assert app.answers.kind is Kind.PRODUCTION
        assert app.answers.rung is Rung.SQLITE
        assert app.result is not None
        claude = (app.result.project / "CLAUDE.md").read_text()
        assert claude.count("**Kind:** production.") == 1
        assert "A rota that is correct." in claude
        assert [adr.number for adr in app.result.adrs] == ["0003"]

    drive(walk())


def test_the_destination_follows_the_name_until_it_is_edited(tmp_path: Path) -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            app.screen.query_one("#name", Input).value = "Rota Planner"
            await pilot.pause()
            assert app.screen.query_one("#destination", Input).value.endswith("/rota-planner")

            await name_it(pilot, "Rota Planner", tmp_path / "somewhere-else")
            app.screen.query_one("#destination", Input).focus()
            await pilot.pause()
            await pilot.press("end", "2")  # editing it by hand takes it off the leash
            app.screen.query_one("#name", Input).value = "Renamed"
            await pilot.pause()
            assert app.screen.query_one("#destination", Input).value.startswith(str(tmp_path))

    drive(walk())


def test_going_back_keeps_what_was_typed(tmp_path: Path) -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            await name_it(pilot, "Kept", tmp_path / "kept")
            app.screen.query_one("#description", Input).value = "Still here."
            await advance(pilot)

            await pilot.press("down", "enter")  # learning
            await pilot.press("escape")
            await pilot.pause()

            assert isinstance(app.screen, NameStep)
            assert app.screen.query_one("#name", Input).value == "Kept"
            assert app.screen.query_one("#description", Input).value == "Still here."

            await advance(pilot)
            assert app.screen.query_one("#kind", RadioSet).pressed_index == 1

    drive(walk())


def test_it_refuses_to_leave_the_first_step_without_a_name() -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            await advance(pilot)
            assert isinstance(app.screen, NameStep)
            assert "needs a name" in str(app.screen.query_one("#error").render())

    drive(walk())


def test_it_refuses_a_destination_inside_the_framework() -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            await name_it(pilot, "Inside", app.catalogue.root / "template" / "nope")
            await advance(pilot)
            assert isinstance(app.screen, NameStep)
            assert "inside the framework" in str(app.screen.query_one("#error").render())

    drive(walk())


def test_the_conditional_documents_arrive_pre_selected(tmp_path: Path) -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            await name_it(pilot, "Preselected", tmp_path / "preselected")
            await advance(pilot)
            await pilot.press("down", "down", "down", "enter")  # production
            await advance(pilot, 4)  # tooling, storage, design, documents

            selected = set(app.screen.query_one("#docs", SelectionList).selected)
            assert {"deployment.md", "observability.md", "diagnostics.md"} <= selected
            assert "demo.md" not in selected

    drive(walk())


def test_the_dial_column_follows_the_highlighted_kind(tmp_path: Path) -> None:
    async def walk() -> None:
        app = WizardApp(catalogue_module.load())
        async with app.run_test() as pilot:
            await pilot.pause()
            await name_it(pilot, "Dials", tmp_path / "dials")
            await advance(pilot)

            shown = str(app.screen.query_one("#dials").render())
            assert "Deploy inside the loop" in shown
            assert "skip" in shown  # the spike column's simplification pass

            await pilot.press("down", "down", "down", "enter")  # production
            await pilot.pause()
            assert "every journey" in str(app.screen.query_one("#dials").render())

    drive(walk())

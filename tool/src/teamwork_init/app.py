"""The wizard. A front end over `plan.create` and nothing more.

Every question is answerable by pressing enter, because the defaults are the
house priors and a project that takes all of them is the common case. What the
wizard will not do is answer a question nobody asked it: anything left blank
keeps the template's placeholder, so an unwritten sentence stays visibly
unwritten rather than being filled with something plausible.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    RadioButton,
    RadioSet,
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection

from . import catalogue as catalogue_module
from .catalogue import Catalogue
from .markdown import plain
from .model import (
    HOUSE_PRIOR,
    ROLE_LABELS,
    Answers,
    DesignSystem,
    Kind,
    Rung,
    default_conditional_docs,
    invocation,
    slugify,
)
from .plan import InitError, Result, check_destination, create


class Invalid(Exception):
    """An answer the wizard will not accept, with the sentence to show."""


class StepScreen(Screen[None]):
    """One question, its explanation, and the two buttons."""

    title_text = ""
    blurb = ""
    next_label = "Next"

    BINDINGS = [
        Binding("escape", "back", "Back", show=True),
        Binding("ctrl+n", "next", "Next", show=True),
    ]

    @property
    def wizard(self) -> WizardApp:
        return self.app  # type: ignore[return-value]

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="body"):
            yield Static(self.title_text, classes="title")
            if self.blurb:
                yield Static(self.blurb, classes="blurb")
            yield from self.content()
        yield Static("", id="error", classes="error")
        with Horizontal(id="buttons"):
            yield Button("Back", id="back", disabled=self.wizard.step == 0)
            yield Button(self.next_label, id="next", variant="primary")
        yield Footer()

    def content(self) -> ComposeResult:
        return iter(())

    def on_mount(self) -> None:
        """Focus the first thing there is to answer.

        Without this the focus sits on the scrolling container, and the arrow
        keys scroll the explanation instead of moving through the options — which
        looks like a step that does not respond to the keyboard.
        """
        for widget in self.query("#body *"):
            if isinstance(widget, Input | RadioSet | SelectionList | Checkbox):
                widget.focus()
                return

    def collect(self) -> dict[str, object]:
        """The answers this step produces. Raise Invalid to keep the user here."""
        return {}

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.action_back()
        else:
            self.action_next()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter moves to the next field, and off the last one to the next step."""
        inputs = list(self.query(Input))
        if inputs and event.input is not inputs[-1]:
            self.focus_next()
            return
        self.action_next()

    def action_back(self) -> None:
        if self.wizard.step:
            self._save(quiet=True)
            self.wizard.goto(self.wizard.step - 1)

    def action_next(self) -> None:
        if self._save():
            self.wizard.goto(self.wizard.step + 1)

    def _save(self, quiet: bool = False) -> bool:
        try:
            self.wizard.answers = replace(self.wizard.answers, **self.collect())  # type: ignore[arg-type]
        except Invalid as refusal:
            if not quiet:
                self.query_one("#error", Static).update(str(refusal))
            return False
        self.query_one("#error", Static).update("")
        return True

    def field(self, widget_id: str) -> str:
        return self.query_one(f"#{widget_id}", Input).value.strip()


class NameStep(StepScreen):
    title_text = "What is this project called?"
    blurb = (
        "The name heads the README, and its slug is the directory the document set "
        "is copied into. Everything after this question has a house default, so "
        "enter is a complete answer to all of them."
    )

    def content(self) -> ComposeResult:
        answers = self.wizard.answers
        yield Label("Name")
        yield Input(value=answers.name, placeholder="Rota Planner", id="name")
        yield Label("One or two sentences, for the README — optional")
        yield Input(
            value=answers.description,
            placeholder="What it is and what it does, for somebody who arrived from a link",
            id="description",
        )
        yield Label("Destination directory")
        yield Input(value=str(answers.destination), id="destination")

    def on_mount(self) -> None:
        super().on_mount()
        # Coming back to this step, a destination that is not the one the name
        # would have produced is one somebody chose — so stop following the name,
        # or returning here silently drags the project back to the default path.
        answers = self.wizard.answers
        if answers.name and str(answers.destination) != str(self._from_name(answers.name)):
            self.wizard.destination_touched = True

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "destination" and event.input.has_focus:
            self.wizard.destination_touched = True
        if event.input.id == "name" and not self.wizard.destination_touched:
            self.query_one("#destination", Input).value = str(self._from_name(event.value))

    @staticmethod
    def _from_name(name: str) -> Path:
        return Path.cwd() / (slugify(name) or "new-project")

    def collect(self) -> dict[str, object]:
        name = self.field("name")
        if not name:
            raise Invalid("A project needs a name — it heads the README and names the directory.")
        destination = self.field("destination")
        if not destination:
            raise Invalid("Nowhere to put it.")
        target = Path(destination).expanduser()
        try:
            check_destination(target, self.wizard.catalogue)
        except InitError as refusal:
            raise Invalid(str(refusal)) from refusal
        return {"name": name, "description": self.field("description"), "destination": target}


class KindStep(StepScreen):
    title_text = "What kind of project is this?"
    blurb = (
        "ADR 0001, and the first record step 0 produces. It sets the bar every later "
        "rule is calibrated against — and it is written down because absence of a "
        "rule and deliberate omission of one look identical from inside a repository."
    )

    def content(self) -> ComposeResult:
        current = list(Kind).index(self.wizard.answers.kind)
        with RadioSet(id="kind"):
            for index, kind in enumerate(Kind):
                yield RadioButton(f"{kind.letter}. {kind.option_title}", value=index == current)
        yield Static(self._dials(self.wizard.answers.kind), id="dials", classes="dials")
        yield Label("The bar, in one sentence: what this owes whoever uses it — optional")
        yield Input(value=self.wizard.answers.bar, id="bar")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.query_one("#dials", Static).update(self._dials(list(Kind)[event.index]))

    def _dials(self, kind: Kind) -> str:
        column = self.wizard.catalogue.dial_column(kind.dial_column)
        width = max(len(dial) for dial in column)
        rows = "\n".join(f"  {dial.ljust(width)}   {setting}" for dial, setting in column.items())
        return f"What this sets, from docs/dev-process.md:\n{rows}"

    def collect(self) -> dict[str, object]:
        kind = list(Kind)[self.query_one("#kind", RadioSet).pressed_index]
        return {"kind": kind, "bar": self.field("bar")}


class ToolingStep(StepScreen):
    title_text = "What fills the four tool roles?"
    blurb = (
        "ADR 0002. The method needs each of these jobs done by something named, and "
        "does not care what. Prefilled with the house priors from "
        "defaults/toolchain.md — change any of them and the departure gets a reason, "
        "because a departure recorded without one is indistinguishable from an "
        "accident."
    )

    def content(self) -> ComposeResult:
        answers = self.wizard.answers
        priors = self.wizard.catalogue.house_priors
        for role, label in ROLE_LABELS.items():
            prior = plain(priors.get(label, HOUSE_PRIOR[role]))
            yield Label(f"{label} — the prior is {prior}")
            yield Input(value=getattr(answers, role), id=role)
        yield Label(f"Language — the prior is {plain(priors.get('Language', 'Python'))}")
        yield Input(value=answers.language, id="language")
        yield Label(
            f"Secrets — the prior is {plain(priors.get('Secrets', 'fnox'))}; 'none' is an answer"
        )
        yield Input(value=answers.secrets, id="secrets")
        yield Label("Why, if any of those differ from the prior")
        yield Input(value=answers.departure_reason, id="departure_reason")
        yield Static(self._preview(answers.task_runner), id="preview", classes="dials")

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "task_runner":
            self.query_one("#preview", Static).update(self._preview(event.value))

    def _preview(self, runner: str) -> str:
        gate = invocation(runner, "ship") or "*(unset)*"
        return f"The gate will be written as: {gate}"

    def collect(self) -> dict[str, object]:
        collected: dict[str, object] = {
            role: self.field(role)
            for role in (*ROLE_LABELS, "language", "secrets", "departure_reason")
        }
        if not collected["task_runner"]:
            raise Invalid("Every repeated command needs a name, so something has to run tasks.")
        return collected


class StorageStep(StepScreen):
    title_text = "Where does this project's own data live?"
    blurb = (
        "The ladder in defaults/storage.md: take the lowest rung that holds, and "
        "record which rung and what would move you. Exogenous formats — a CSV "
        "somebody else publishes — are not this question. Answering writes an ADR; "
        "leaving it undecided writes nothing."
    )

    def content(self) -> ComposeResult:
        ladder = self.wizard.catalogue.ladder
        self._rungs = [Rung.UNDECIDED] + [Rung(number) for number in sorted(ladder)]
        current = self._rungs.index(self.wizard.answers.rung)
        with RadioSet(id="rung"):
            for index, rung in enumerate(self._rungs):
                undecided = rung is Rung.UNDECIDED
                label = "Not decided yet" if undecided else plain(ladder[rung.number].label)
                yield RadioButton(label, value=index == current)
        yield Label("What would move you off it — optional, and the half people skip")
        yield Input(value=self.wizard.answers.rung_exit, id="rung_exit")

    def collect(self) -> dict[str, object]:
        rung = self._rungs[self.query_one("#rung", RadioSet).pressed_index]
        return {"rung": rung, "rung_exit": self.field("rung_exit")}


class DesignStep(StepScreen):
    title_text = "What intermediates the design decisions?"
    blurb = (
        "The prior in defaults/design-system.md: the application never makes a design "
        "decision directly, and tokens are the interface it may reference and may not "
        "define. A choice here writes an ADR; 'no interface' and 'not decided' write "
        "nothing."
    )

    def content(self) -> ComposeResult:
        options = list(DesignSystem)
        current = options.index(self.wizard.answers.design_system)
        with RadioSet(id="design"):
            for index, option in enumerate(options):
                yield RadioButton(option.value, value=index == current)
        yield Label("Where the vendored copy lives, or what is owed back — optional")
        yield Input(value=self.wizard.answers.design_note, id="design_note")

    def collect(self) -> dict[str, object]:
        choice = list(DesignSystem)[self.query_one("#design", RadioSet).pressed_index]
        return {"design_system": choice, "design_note": self.field("design_note")}


class DocsStep(StepScreen):
    title_text = "Which conditional documents earn their place?"
    blurb = (
        "Each is deleted unless the project has the thing, and the condition is the "
        "one docs/README.md states. What is pre-selected is inferred from the answers "
        "so far, which makes it a guess — the file is easier to restore now than to "
        "notice sitting empty in three journeys' time."
    )

    def content(self) -> ComposeResult:
        selected = set(self.wizard.answers.conditional_docs)
        yield SelectionList[str](
            *(
                Selection(
                    f"{doc.filename} — {plain(doc.condition)}",
                    doc.filename,
                    doc.filename in selected,
                )
                for doc in self.wizard.catalogue.conditional_docs
            ),
            id="docs",
        )

    def collect(self) -> dict[str, object]:
        chosen = self.query_one("#docs", SelectionList).selected
        return {"conditional_docs": frozenset(chosen)}


class ConfirmStep(StepScreen):
    title_text = "Ready"
    next_label = "Create"

    BINDINGS = [
        Binding("escape", "back", "Back", show=True),
        Binding("ctrl+n", "next", "Create", show=True),
    ]

    def content(self) -> ComposeResult:
        yield Static(summarise(self.wizard.answers, self.wizard.catalogue), classes="summary")
        yield Checkbox(
            "git init, and commit the set at its initial version",
            value=self.wizard.answers.git_init,
            id="git_init",
        )

    def collect(self) -> dict[str, object]:
        return {"git_init": self.query_one("#git_init", Checkbox).value}

    def action_next(self) -> None:
        if not self._save():
            return
        try:
            result = create(self.wizard.answers, self.wizard.catalogue)
        except InitError as refusal:
            self.query_one("#error", Static).update(str(refusal))
            return
        self.wizard.result = result
        self.wizard.push_screen(DoneScreen())


class DoneScreen(Screen[None]):
    BINDINGS = [Binding("q", "quit", "Quit", show=True)]

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="body"):
            yield Static(report(self.app.result, self.app.answers), classes="summary")  # type: ignore[attr-defined]
        with Horizontal(id="buttons"):
            yield Button("Done", id="done", variant="primary")
        yield Footer()

    def on_button_pressed(self) -> None:
        self.app.exit()

    def action_quit(self) -> None:  # type: ignore[override]
        self.app.exit()


STEPS: list[type[StepScreen]] = [
    NameStep,
    KindStep,
    ToolingStep,
    StorageStep,
    DesignStep,
    DocsStep,
    ConfirmStep,
]


def summarise(answers: Answers, catalogue: Catalogue) -> str:
    """What is about to be written, in the order it will be written."""
    roles = "  ".join(
        f"{label.split()[0].lower()}={getattr(answers, role) or '—'}"
        for role, label in ROLE_LABELS.items()
    )
    docs = ", ".join(sorted(answers.conditional_docs)) or "none"
    deleted = sorted(catalogue.conditional_filenames - set(answers.conditional_docs))
    lines = [
        f"{answers.name}  →  {answers.destination}",
        "",
        f"Kind          {answers.kind.label}   (ADR 0001, decided)",
        f"Tools         {roles}   (ADR 0002, decided)",
        f"Language      {answers.language}",
        f"Secrets       {answers.secrets or '—'}",
        f"Gate          {invocation(answers.task_runner, 'ship')}",
    ]
    if answers.rung is not Rung.UNDECIDED:
        rung = catalogue.ladder[answers.rung.number]
        lines.append(f"Storage       rung {rung.number}, {rung.name}   (a new ADR)")
    if answers.design_system in {DesignSystem.HOUSE, DesignSystem.CLIENT}:
        lines.append(f"Design        {answers.design_system.value}   (a new ADR)")
    lines += [
        "",
        f"Keeping       {docs}",
        f"Deleting      {', '.join(deleted) or 'nothing'}",
    ]
    if answers.departs_from_house and not answers.departure_reason.strip():
        lines += [
            "",
            "No reason recorded for departing from a house prior — the ADR will",
            "carry a prompt where the sentence should be.",
        ]
    return "\n".join(lines)


def report(result: Result, answers: Answers) -> str:
    """What happened, and what of step 0 is still a person's job.

    No line here starts with a space: the terminal strips leading whitespace when
    it renders, so an indent used for alignment silently becomes a ragged left
    edge. Bullets carry the structure instead.
    """
    lines = [f"Written to {result.project}", ""]
    for adr in result.adrs:
        lines.append(f"• ADR {adr.number} written — {adr.title}")
    if result.pruned.deleted:
        lines.append(f"• Deleted {len(result.pruned.deleted)} conditional documents")
    if result.pruned.unlinked:
        lines.append(
            f"• Unlinked {len(result.pruned.unlinked)} references to them, so no link dangles"
        )
    if result.git:
        lines.append(f"• {result.git[0].upper()}{result.git[1:]}")
    if result.missing_anchors:
        lines += ["", "Anchors that did not resolve — these placeholders were left as they are:"]
        lines += [f"• {miss}" for miss in result.missing_anchors]

    lines += [
        "",
        "Step 0 is not finished. What the wizard cannot answer for you:",
        "",
        "• docs/journeys/ — a document per journey of the first release, from",
        "TEMPLATE.md. Draft them all before building any: drafting is what",
        "surfaces the ordering, the shared rules, and the questions that belong",
        "to somebody else.",
        "",
        "• docs/roadmap.md — that inventory, grouped into releases.",
        "• README.md — what it does, who uses it, how to get it running.",
    ]
    if not answers.bar.strip():
        lines.append("• The bar — one sentence, in CLAUDE.md and ADR 0001.")
    lines += ["", f"cd {result.project}"]
    return "\n".join(lines)


class WizardApp(App[None]):
    CSS = """
    Screen { layout: vertical; }
    #body { padding: 1 2; height: 1fr; width: 1fr; }
    .title { text-style: bold; color: $accent; padding-bottom: 1; }
    .blurb { color: $text-muted; padding-bottom: 1; }
    .dials { color: $text-muted; padding: 1 0; }
    /* Width from the container, not from the longest line: an auto-width Static
       sizes to its content and then wraps that same line inside its padding. */
    .summary { width: 1fr; padding: 1 0; }
    .error { color: $error; padding: 0 2; }
    Label { padding-top: 1; }
    Input { width: 100%; }
    SelectionList { height: auto; max-height: 20; }
    RadioSet { width: 100%; }
    #buttons { height: auto; padding: 1 2; align-horizontal: right; }
    #buttons Button { margin-left: 2; }
    """

    BINDINGS = [Binding("ctrl+q", "quit", "Quit", show=True)]

    def __init__(self, catalogue: Catalogue) -> None:
        super().__init__()
        self.catalogue = catalogue
        self.answers = Answers(destination=Path.cwd())
        self.destination_touched = False
        self.step = 0
        self.result: Result | None = None

    def on_mount(self) -> None:
        self.title = "teamwork-init"
        self.sub_title = "step 0"
        self.goto(0)

    def goto(self, step: int) -> None:
        step = max(0, min(step, len(STEPS) - 1))
        if step == 5:  # the conditional documents, defaulted from everything answered before them
            self.answers = replace(
                self.answers,
                conditional_docs=self.answers.conditional_docs
                or default_conditional_docs(
                    self.answers.kind,
                    self.answers.rung,
                    self.answers.secrets,
                    self.catalogue.conditional_filenames,
                ),
            )
        self.step = step
        self.sub_title = f"step 0 — {step + 1} of {len(STEPS)}"
        screen = STEPS[step]()
        if isinstance(self.screen, StepScreen):
            self.switch_screen(screen)
        else:
            self.push_screen(screen)


def run(catalogue: Catalogue | None = None) -> None:
    WizardApp(catalogue or catalogue_module.load()).run()

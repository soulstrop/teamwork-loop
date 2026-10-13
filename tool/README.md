# teamwork-init

Step 0 as a wizard. It asks what the project is called, what kind of project it
is, and what fills the roles the method needs filled — then copies
[`../template/`](../template/) into a new directory with those answers rendered
into it, deletes the conditional documents this project has not earned, and
commits the result.

It is a front end over one function. Everything it does is available without a
terminal, which is what lets the gate render every project kind on every commit.

## Running it

```
cd tool
uv run teamwork-init                    # the wizard
uv run teamwork-init verify             # the assertion that keeps it honest
uv run teamwork-init --framework ~/src/teamwork-loop   # from anywhere else
```

The framework checkout is found by walking upwards from the current directory,
then from the installed package. `TEAMWORK_FRAMEWORK` overrides both, and
`--framework` overrides that.

## What it asks, and what each answer writes

| Question | Writes |
|---|---|
| Name, description, destination | The `README.md` title and opening, and the directory everything lands in |
| Kind — spike · learning · on spec · production | ADR 0001 to `decided`, with the option chosen; the **Kind** line in `CLAUDE.md` |
| The bar, in one sentence | `CLAUDE.md` and ADR 0001. Left blank, the placeholder stays |
| The four tool roles, language, secrets | ADR 0002 to `decided`; the role table and the four task invocations in `CLAUDE.md` |
| Storage rung | A new ADR, if answered. *Not decided yet* writes nothing |
| Design system | A new ADR, if the project has an interface and a choice was made |
| Conditional documents | Deletes the rest, and every reference to them |

**Blank means blank.** Anything only a person can write — the bar, the reasoning
behind a departure, what the system does — keeps the template's placeholder if it
is left empty. An unwritten sentence should look unwritten.

## Three rules it is built on

**`template/` stays byte-identical.** The manual path in
[`../USING-THIS-FRAMEWORK.md`](../USING-THIS-FRAMEWORK.md) — `cp -r template/.
new-project/` — keeps working, and this tool is a convenience over it rather than
a replacement for it. The consequence is that the placeholders are the prose ones
already in the documents (`*(unset)*`, `*(Project name)*`, `YYYY-MM-DD`) and the
tool holds a copy of those strings in
[`anchors.toml`](src/teamwork_init/anchors.toml). A copy in two places is exactly
what the method warns about, so:

**`verify` is the mechanical half.** It asserts every anchor occurs *exactly
once* in the template file it names, that every renderer exists, and that the
tables read out of the document set still parse. A template edit that strands an
anchor fails `check` rather than producing a project with a stale placeholder in
it. This is the same argument as the link checker in `ship`: a cross-reference
nothing verifies is one that is already wrong somewhere.

**Nothing the framework states is restated here.** The dial table, the conditions
under which a conditional document earns its place, the storage ladder and the
house priors are all parsed out of `template/docs/dev-process.md`,
`template/docs/README.md`, `defaults/storage.md` and `defaults/toolchain.md` at
the moment they are needed — so the wizard's own prompts cannot disagree with the
documents they are about. What the tool owns is the *shape* of an answer and its
judgement about what to pre-select, which is nobody else's.

The one deliberate exception is `HOUSE_PRIOR` in
[`model.py`](src/teamwork_init/model.py): `defaults/toolchain.md` states the
priors in prose (*"language-specific — `uv` for Python"*), and a prefilled input
box needs a value. `verify` asserts each prefilled value still appears in the row
it came from, so changing the default fails the check rather than drifting.

## Deleting a conditional document

Deleting the file is the easy half. The set cross-references, so `docs/README.md`
still lists it in two tables and up to four surviving documents still link to it
— and a dangling link is what the link checker in `ship` exists to catch.

**A link to a deleted document is unlinked, not removed.** The sentences pointing
at these files are boundary statements — *not the job: `backups.md`, which is …*
— and the boundary is still true when the document is absent. Cutting the
sentence would delete the only thing telling a reader where that material goes if
the condition later fires. Every unlink is counted in the report.

Two blocks in `docs/README.md` are dropped whole rather than row by row: the
five-way comparison when fewer than two of its five survive, and the retention
paragraph when `diagnostics.md` goes, since that paragraph exists to point at it.

## What it pre-selects, and why that is a guess

Every condition in `docs/README.md` is about a fact the wizard has not asked for
— whether somebody else looks after the store, whether the work has to be shown
to a room. So the pre-selection is inferred from the answers it *does* have:
production selects deployment, observability and diagnostics; on spec selects the
demo; a storage rung of SQLite or above selects backups; a secrets tool selects
security. All of them toggle.

The bias is deliberate. A document deleted at step 0 costs one `git show` to
restore. A document seeded and never noticed is one the method says is telling
you something three journeys later, when nobody is listening.

## What it does not do

**Journeys and the roadmap.** Step 0 produces six things and this covers four of
them. Drafting the first release's journeys is what surfaces the ordering, the
shared rules and the questions that belong to somebody else — that is an argument
against typing them into a form, so the wizard names them as what is left instead.

## Tasks

| Task | Runs |
|---|---|
| `check` | ruff, `verify`, the unit tests |
| `ship` | `check`, plus a real render of every project kind into a scratch tree |
| `fmt` | Format and autofix |

# teamwork-loop

A document set for building software one journey at a time, with a collaborator
— an agent, or a new human — that starts every session cold.

Copy it into a new repository and, before a line of the project's own code
exists, it already tells whoever opens it where the project is, what is next, and
how the work is done here. As the project grows, the documents grow with it: each
user journey lands through the same eight-step loop, decisions land as ADRs, and
loose findings are routed to a home rather than lost.

**Who it is for.** Anyone building software with an AI collaborator who has
found that context outside the repository does not exist — and that the same
mistakes come back every session unless something written down prevents them.

## What is in here

| Directory | What it is |
|---|---|
| `template/` | The document set at its initial version. Copied wholesale into a new project |
| `defaults/` | Standing priors — language, storage, toolchain, design system. Read at step 0 and cited by the project's ADRs, **not** copied |
| `tool/` | `teamwork-init`, a wizard that does the copy with your answers already rendered into it |

## Starting a project

By hand:

```bash
cp -r teamwork-loop/template/. /path/to/new-project/
cd /path/to/new-project
git init && git add -A && git commit -m "Document set at its initial version"
```

Or with the wizard, which asks what kind of project this is and what tools fill
each role, writes the first two ADRs, `README.md` and `CLAUDE.md`, and deletes the
documents the project has not earned:

```bash
cd teamwork-loop/tool && uv run teamwork-init
```

Either way, the next step is drafting the first release's journeys.

## Read next

**[USING-THIS-FRAMEWORK.md](USING-THIS-FRAMEWORK.md)** — the three layers, the
two rules the set obeys, the planning and implementation session modes, step 0,
and what each file arrives carrying.

**[ROADMAP.md](ROADMAP.md)** — what is left to build for the framework itself,
including the 2.0 bring-your-own-tracker release.

## Licence

`template/` is public domain (CC0), so a project built from it owes nothing for
its own documents. `tool/` is AGPL-3.0, and the writing about the method is
CC BY-SA 4.0. Details in [LICENSE.md](LICENSE.md).

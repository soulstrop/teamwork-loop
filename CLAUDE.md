# CLAUDE.md

This repository is the teamwork-loop framework itself, not a project built with
it. **Rules only** — the method is [`USING-THIS-FRAMEWORK.md`](USING-THIS-FRAMEWORK.md),
what is left to build is [`ROADMAP.md`](ROADMAP.md).

## Layout

| Path | What it is | Licence |
|---|---|---|
| `template/` | Copied wholesale into each new project. Its `CLAUDE.md` is that project's, not this repository's | CC0 |
| `defaults/` | Standing priors, read at step 0 and cited by a project's ADRs; never copied | CC BY-SA |
| `tool/` | `teamwork-init`, the wizard that renders `template/` | AGPL |
| `design/` | Inputs to a future release — ideas, not specifications | CC BY-SA |

The licence by path is in [`LICENSE.md`](LICENSE.md); contributions come under
[`CLA.md`](CLA.md).

## Rules

- **One fact, one home.** Link to the home rather than restating it. In
  `template/`, rules live in `CLAUDE.md` and their reasoning in
  `docs/dev-process.md`.
- **Template documents name tasks, not commands.** The project picks the tools.
- **Text `teamwork-init` fills is anchored** in
  `tool/src/teamwork_init/anchors.toml`. Change the anchor in the same commit as
  the template text it matches. The dial table in `template/docs/dev-process.md`
  is parsed by the tool, so keep its shape.
- **After any change to `template/` or `tool/`, run `check` in `tool/`** — lint,
  `verify` and the tests. Run `ship` before tagging a release.
- **Write agent-facing files for any agent.** `template/CLAUDE.md` and the
  template skills are read by agents other than Claude Code, so keep rules a
  harness may already enforce, such as `template/CLAUDE.md` §9. Rules over
  reasoning, one trigger per case in a skill description, and the target
  behaviour stated rather than the forbidden one.
- **Roadmap item numbers are permanent.** A late item takes the next number.
- **Documents say what is true now.** History is `git log`.
- **Commit subjects carry an area prefix** — `template:`, `skills:`, `tool:`,
  `process:`, `docs:`, `license:`.

# Toolchain defaults

The prior for the four tool roles, and for secrets. Taken unless the project has
a reason, and the reason is recorded in its ADR rather than here.

## The roles, and what fills them

| Role | Default | Why |
|---|---|---|
| Task runner | **mise** | Every repeated command gets a name, and the task carries the flags, variables and connection strings that make it correct |
| Toolchain manager | **mise** | Same file pins the tool versions, so a checkout and a CI runner agree without a second manifest |
| Environment manager | **mise** profiles | Per-environment values reach a command without any script branching on which environment it is |
| Dependency manager | **language-specific** — `uv` for Python | Resolution and locking belong to something that understands the ecosystem's version semantics |
| Language | **Python**, unless the problem argues otherwise | |
| Secrets | **fnox** | One seam between a store and a value |

**Three of the four roles landing on one tool is a convenience, not a
principle.** Nothing in the method assumes it, and a project that pins tools with
one thing and runs tasks with another has broken nothing.

## Why the dependency manager stays separate

A toolchain manager knows how to install a language; it does not know that two
libraries disagree about a transitive pin. Resolution, locking and the isolated
environment belong to something ecosystem-native — `uv`, `cargo`, `go mod`, `npm`
— and the task runner calls *it*.

The requirement underneath is the part that does not vary: **a build resolves
against a lockfile inside an isolated environment, never against what is
installed on the machine.** A build that works because of what somebody
`apt install`ed is reproducible by accident, and it stops being reproducible on
the day the machine changes rather than the day the code does.

## Secrets

**fnox is the only path from a store to a value**, and the map is committed and
valueless.

The property being bought is that no script and no source file names a store
path. Moving from a password manager on a laptop to whatever a real host provides
— AWS Secrets Manager, Vault — is then a change to one provider block instead of
a change to every script that reads a secret.

Two rules travel with it:

- **A deployed value is rendered into an environment file outside the checkout**,
  mode 0600, and regenerated on every deploy. Anything typed into that file is
  overwritten, which is the correct direction: the store is authoritative.
- **A setting that selects an identity or a credential gets no default.** A
  fallback between two credentials is a security decision wearing the clothes of
  a convenience — an unset variable silently connecting as the privileged role is
  the exact shape of it.

## Reconsider these if

- **The project is a spike or a learning exercise.** Secrets management earns its
  place when there is a secret worth stealing. Before that, `fnox` is ceremony —
  though note the escalation triggers in the project-kind ADR, since "it acquired
  a credential" is one of them.
- **The team already runs something else.** A second task runner in one
  organisation costs more than any difference between them.
- **The ecosystem has a strong native answer** that already fills three roles —
  some do, and adding `mise` on top is a layer that has to be explained.
- **The deployment target dictates it.** A platform that expects a particular
  build shape wins the argument; the method needs the roles filled, not filled by
  anything in particular.

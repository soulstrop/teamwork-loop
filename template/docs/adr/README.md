# Architecture decision records

One file per architecturally significant decision. A decision belongs here if
reversing it would be expensive, if it constrains later choices, or if somebody
six months from now would reasonably ask "why on earth is it like this?"

Numbering is sequential and permanent. Titles are kebab-case.

## Lifecycle

```
proposed ──> decided ──> reopened ──> decided
                  │            │
                  └────────────┴──> superseded
```

| Status | Meaning |
|---|---|
| `proposed` | Written up, not yet settled. Options may still change |
| `decided` | In force. The codebase should reflect this |
| `reopened` | Under active reconsideration. Still in force until resolved |
| `superseded` | Replaced. Carries a forward link to whatever replaced it |

**Reopening** keeps the same number and appends a dated *Reconsideration*
explaining what changed. If the original decision survives, the status returns to
`decided` and the reconsideration stays as part of the record.

**Superseding** creates a new ADR that links back via `Supersedes:`. The old one
moves to `superseded` with a forward link. Do not edit a superseded ADR's
reasoning — it was true when written, and the record of a wrong turn is worth as
much as the record of a right one.

## Sections

Every ADR carries four, in this order:

1. **Problem** — what forced a decision. Enough context to judge it later
2. **Options considered** — with honest trade-offs. An ADR without rejected
   options is an assertion, not a record. Include the option you would have taken
   under different constraints
3. **Decision** — what was chosen and why, referring back to the trade-offs
4. **Reconsider this if** — the conditions that would make this wrong

That fourth section is what makes the record useful rather than decorative. A
collaborator with no memory of the decision needs a stated condition for
reopening it; without one, every settled question is re-arguable and eventually
gets re-argued.

**Most ADRs are written at step 7**, from what the journey actually taught, not
before it. The exception is a decision that has to be settled *to* build — those
arrive through a conversation during the journey, and the alternatives presented
in that conversation are this document's *Options considered*.

## Index

| # | Decision | Status |
|---|---|---|
| [0001](0001-what-kind-of-project-this-is.md) | What kind of project this is, and the bar that follows | proposed |
| [0002](0002-tooling-roles.md) | What fills the four tool roles, and what the gate covers | proposed |

The first two arrive with the project and are written at step 0. Everything after
them is earned.

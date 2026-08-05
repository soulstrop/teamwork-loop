# Backups and recovery

*Conditional — earns its place the moment there is data that cannot be
regenerated, which is also an escalation trigger in
[ADR 0001](adr/0001-what-kind-of-project-this-is.md). Before that, say so here in
one line and delete the rest: a project whose entire state can be rebuilt by a
task has a recovery procedure, and it is that task.*

**The job:** what is backed up, how often, where it goes, how long it is kept,
and — the load-bearing part — **the restore, rehearsed**.

**Not the job:** [`deployment.md`](deployment.md), which covers releasing and
rolling back *code*. Those are a different failure with a different procedure: a
rollback is a symlink and a restart, a restore is an outage. Nor
[`data.md`](data.md), which is the store as an object somebody looks after.

## The one rule

**Backups are verified by restoring them, not by a job that reports success.**

A backup job exits zero for a file that is empty, truncated, encrypted with a key
nobody has, or of the wrong database. Every one of those looks identical from the
monitoring side, and all four are discovered at the only moment they cannot be
fixed.

**So a section here stays empty until it has been rehearsed, and says so.** A
restore procedure nobody has run is fiction, and fiction in a recovery document
is worse than a gap, because somebody will follow it while under pressure.

## Objectives

| | Target | Actual, measured | When measured |
|---|---|---|---|
| **RPO** — how much work may be lost | | | |
| **RTO** — how long recovery may take | | | |

*Both columns matter. A target with no measurement beside it is an aspiration,
and the gap between the two is the thing to know **before** an incident rather
than during one.*

*If they have never been measured, write "unmeasured" rather than a plausible
number. A number somebody invented is worse than a blank, because it gets
planned against.*

## What is backed up

| What | How often | Where | Retained |
|---|---|---|---|
| | | | |

**And what is not**, deliberately:

- **Derived data**, where regenerating is cheaper and more trustworthy than
  restoring. Say what the regeneration is, and how long it takes — it is part of
  the RTO.
- **Secrets**, which live in the secret store and are restored from there.
  A backup containing credentials is a second, less-guarded copy of them.
- *(Anything else, with its reason.)*

## Where the copies are

*One copy in the same place as the original is not a backup. The distinctions
worth stating:*

- **Off-host**, against losing the machine.
- **Off-provider or offline**, against losing the account — which is a real
  failure mode and one that takes everything at once.
- **Immutable or write-once**, against something with credentials deleting the
  backups first. That is the shape of a ransomware incident, and a backup an
  attacker can delete is a backup for hardware failure only.

## Encryption and keys

*If the backups are encrypted — and they should be, since they are the least
guarded copy of everything — then **where the key lives is part of the backup
policy**.*

*The failure to avoid: a key held only in the system being recovered. State where
the key is, who can reach it, and how that is tested, because an unreadable
backup and no backup are the same thing with different paperwork.*

## Restoring

*The procedure, once it has been run.*

*Two things to record from the rehearsal that nobody predicts correctly:*

- **How long it actually took**, end to end, including the parts that are not the
  restore — locating the copy, provisioning somewhere to put it, the derived data
  being rebuilt afterwards.
- **What was inconsistent at the boundary.** Work in flight at the moment the
  backup was taken is the interesting case: partially completed operations,
  external side effects that already happened and cannot be undone, anything
  scheduled that will now run twice or not at all.

## After a restore

*What has to be checked, reconciled or re-run. This is the section that is always
missing and always needed — a restored system is not a working system until
somebody has established what it now believes and whether that matches what
happened outside it.*

*Anything irreversible that occurred after the restore point deserves naming
specifically: messages sent, payments made, files handed to somebody else. The
system will not know it did those things.*

## Rehearsal cadence

*When it is next due, and what the last one found. **A restore rehearsed once and
never again is a restore of a system that no longer exists** — the schema, the
volume and the dependencies have all moved.*

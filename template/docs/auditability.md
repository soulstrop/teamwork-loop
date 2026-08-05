# Auditability

*Conditional — earns its place when somebody will ask **who did this**, or when
an obligation says a record must exist: regulated data, money, personnel
decisions, anything a person can dispute.*

**The job:** what is recorded about who did what, what obligation requires it,
how long it is kept, and who may read it.

**Not the job:** [`observability.md`](observability.md), which is about whether
the system is healthy. The two are separate on purpose: telemetry is sampled,
aggregated and thrown away, and an audit record is none of those things. Nor
[`data.md`](data.md), which is the map of the store — this is the argument for
which records exist.

## What must be answerable

*Start from the questions, not the tables. Each row is a question somebody will
ask, and the record that answers it.*

| Question | Answered by | Obligation behind it |
|---|---|---|
| *"Who read my file?"* | | |
| *"Why did I get this outcome?"* | | |

**A question with no obligation behind it is worth asking about.** It may be a
genuine need nobody has written down, or it may be a record being kept because it
seemed prudent — and records kept without a reason are the ones that become a
liability at the point somebody has to disclose them.

## The rules that keep a trail true

**An audit record is not part of the transaction it describes.** [design
note](design-notes.md#modelling) The test is whether a rollback leaves the record
true. A log written inside the operation that refuses is a log of every permitted
access and no refused one — exactly backwards, and it looks entirely healthy.

**Record the refusal, not only the success.** The attempts that were declined are
usually the interesting half, and they are the half that disappears if the record
rides along with the work.

**Reachable only through the thing that records it.** Where a read must be
logged, there is one function that returns the data, and obtaining the data and
writing the record are the same operation rather than two that must be sequenced
correctly. A second path is a hole, so a static check that no second path exists
is worth more than a convention that nobody adds one.

**Append-only, and that includes the application's identity.** If the process
serving requests can update or delete audit rows, the trail is evidence of
nothing. This is usually a privilege split rather than a code rule.

**The trail is not the domain.** A record of what happened is not the mechanism
by which it happened. If deleting the audit trail would change what the system
does, something is reading it that should not be.

## Who may read it

*Reading an audit trail is itself a consequential act, and often a privileged
one. Say who may, and whether **that** read is recorded — which is a real
question and not a joke, since the trail is frequently the most sensitive
collection in the system.*

*A related trap: withholding the content but not the existence. That somebody has
a record attached is itself information about them.*

## Retention

| Record | Kept for | Because | Then |
|---|---|---|---|
| | | | |

*Both ends need a reason. Too short and the question cannot be answered; too long
and the data is a liability that has to be disclosed, secured and eventually
explained. **"Forever" is a decision**, and one that should be made rather than
arrived at by nobody writing a deletion.*

*Retention interacts with [`backups.md`](backups.md): a record deleted under
policy that still exists in a backup has not been deleted. Say how that is
handled, or say that it is not.*

## What is deliberately not recorded

*With the reason. Most often: something that would be useful and whose collection
is not proportionate, or content where the fact of access is sufficient.*

-

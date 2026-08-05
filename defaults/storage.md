# Storage defaults

There is no default store. There is a **ladder**, and a rule for climbing it:
take the lowest rung that holds, and record which rung and what would move you.

Two questions come before the ladder, and most decisions are settled by them.

## First: is it exogenous?

**CSV, JSON, YAML and key-value files are not a storage decision.** They appear
at the boundary because something else chose them — a file the project consumes,
a file it produces for somebody, a format a counterparty publishes. The format is
not yours, and neither is the schema.

Two consequences, both of which cost something when ignored:

**Parse at the edge into your own types.** An exogenous file is somebody else's
document; what you build from it is yours. Letting the incoming shape *be* the
model means every upstream change is a change to your domain, and the day their
column becomes optional is the day your invariant becomes optional. The
vocabulary should say so too — the incoming row and the thing it becomes get
different names, or the collision arrives later as a bug.

**Never write your own state in one.** A JSON or YAML file holding the project's
own data is nearly always a TOML file that grew, or a database that was avoided.

## Second: does a person read and edit it?

Then **TOML**, and that is the whole answer for the project's own configuration
and small hand-maintained structures. It is the format with the least cognitive
load to read, which is the only property that matters for something whose reader
is a human being at the moment they are trying to change something else.

**Outgrowing TOML is a signal, not a formatting problem.** When a file starts
wanting cross-references between sections, repeated records with identity, or
anything that has to be validated against a shape, the answer is not a more
expressive file format. It is that the data has earned a schema — go to the next
rung. Reaching for YAML at this moment is how a configuration file becomes an
unversioned, unvalidated database that nothing can query and everything reads.

## The ladder

For the project's own data, once the two questions above are answered:

| Rung | Holds | Moves you up when |
|---|---|---|
| **0. Nothing** | State lives in the process and dies with it | Something has to survive a restart |
| **1. TOML** | Configuration and small structures a person maintains | It is written by the program rather than by a person, or it has outgrown the format as above |
| **2. SQLite** | Relational data, real queries, transactions. One writer, one machine, embedded | Concurrent writers, a second process, or a network between them |
| **3. Postgres** | Concurrent writers, invariants the database enforces, real types, several processes | A specific access shape it cannot serve at the required rate |
| **4. A specialised store, *beside* Postgres** | The one shape Postgres is measurably too slow for — vector search, time-series at rate | — |

**Rung 4 is beside, not instead of.** It earns its place for one access pattern
that has been *measured*, and Postgres keeps everything else. A second store
adopted wholesale is a second source of truth, and the failure that follows is
not slowness but two answers to one question.

## The other axis: shape, not scale

**AMQP, Kafka, OpenMessaging, MQTT, ScyllaDB** are not higher rungs. They arrive
when the thing is not a store — a stream, a fan-out, a queue with delivery
semantics, an ingest rate with no query behind it — or when the deployment
scenario dictates the shape: many small producers on unreliable links is MQTT's
problem statement and nobody else's.

- **The consumer is not the producer and neither waits for the other.** That is a
  queue. Building one out of a table is building a queue badly — though a table
  plus a bounded pass over due rows carries further than people expect, with no
  broker to operate.
- **Order and replay matter more than current value.** That is a log, and a
  database of current values cannot answer what the value used to be.
- **Write rate and topology, not volume, are the constraint.** A wide-column
  store buys write throughput and cross-region availability at the price of the
  joins and the constraints rung 3 exists for.

## The rules that matter more than the rungs

**Start at the lowest rung that holds.** The common error is not being caught out
by scale; it is a config file in Postgres, or a broker operated for a workload one
table would serve. Every rung above the one you need is operational cost paid
forever against a scale that may not arrive.

**Climbing is cheap until there is data you cannot regenerate.** That is the real
deadline, and it is worth naming as it approaches — the same trigger the
project-kind ADR lists, for the same reason.

**Where an invariant is the product, the store is not an implementation
detail.** If a rule must never be violable, it belongs in something that can
refuse, and the choice of store becomes the correctness argument rather than a
performance one. Test against the real thing: an in-memory substitute does not
implement the constraint you chose the store for, and the suite will be green
about a guarantee that does not exist.

**Record the rung and its exit condition.** In the project's ADR:

> Rung 2, SQLite. One process writes, under a million rows, ships inside the
> artifact. **Reconsider if** a second writer appears, or the deployment stops
> being a single machine.

Without that second sentence a considered floor is indistinguishable from an
unexamined one — and the person who cannot tell, in a year, is you.

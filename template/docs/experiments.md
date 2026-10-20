# Experiments on the process

Proactive investigations into how the work is done — the deliberate half of the
[process loop](dev-process.md#8-the-process-loop), where residue is the half that
arrives unbidden.

**This is a menu, not a backlog. Nothing here is owed.** An experiment costs
attention, which is the scarcest thing in a small project, and the usual correct
answer to any entry is *not now*. Declining one is an outcome; so is deleting one
that has stopped being interesting. Nothing in the gate or the journey loop
depends on any of this.

Cost is stated first for that reason. **Rides along** means the work is happening
anyway and the only cost is looking afterwards.

| # | Question it answers | Cost | State |
|---|---|---|---|
| [E1](#e1--can-a-cold-session-build-a-journey-from-the-repository-alone) | Does the repository hold enough context to work from cold? | one session | available |
| [E2](#e2--the-navigation-trace-on-a-journey-that-opens-new-ground) | Which documents actually get read, and when? | rides along | available |
| [E3](#e3--does-the-residue-escape-hatch-ever-fire) | Are the routing categories complete, or is nobody looking? | one line per journey | available |
| [E4](#e4--capturing-self-correction) | Does the process help recover from wrong turns? | needs an instrument | blocked |
| [E5](#e5--a-unit-of-work-that-is-mostly-not-a-screen) | Does "the failing E2E is the definition of done" survive work with no interface? | rides along | available |

## Three notes on running one

**Write predictions before the run, and say where they were kept.** Predictions
written afterwards are a description of what happened.

**For anything testing the repository itself, the predictions cannot live in the
repository.** The repo is the apparatus, and a cold session that can read its own
grading rubric is not being tested. Hold them outside — a conversation, a file
elsewhere — and reproduce them here afterwards, noting where they were kept. This
applies only to cold-start experiments; an observational one has nothing to
contaminate.

**A non-result is a result, and usually about the instrument.** Discovering that
a question cannot be measured with what you have constrains every experiment
after it, which is worth more than the answer you failed to get.

---

## E1 — Can a cold session build a journey from the repository alone?

**Answers:** the central claim of
[`dev-process.md` §6](dev-process.md#6-why-it-is-shaped-for-a-collaborator-with-no-memory)
— that enough context lives in the repository for a collaborator starting cold to
build the next unit without asking anything already settled.

**Cost:** one session, plus the discipline of not helping.

**Protocol.** A session with no context, no briefing and no handoff is given
`start J<N>` and nothing else. Predictions are written beforehand, outside the
repository, covering what should work, where friction is expected, and what would
count as a failure of the *process* rather than of the session.

**Failure is defined as** needing to ask a question whose answer was already
settled in the repository. A question the documents deliberately deferred to this
journey is the system working, not a failure — which is why pre-registering those
in the journey document matters.

**Do not answer anything the repository already answers.** Record the question
and point at the document, so a leak is measured rather than patched mid-run.

## E2 — The navigation trace on a journey that opens new ground

**Answers:** which documents earn their length, and which do no orientation work
at all.

**Cost:** rides along. One transcript extraction afterwards.

**Why new ground.** A journey extending an area two adjacent modules already made
legible tells you little — the code was enough. A journey opening something
genuinely new is the case that separates *this document is too long* from *this
journey did not need it*.

**Protocol:** after the journey, extract the read sequence from the transcript in
order, and note at what point each document first appears and whether the read
precedes or follows the work it relates to. A document first read *to update it*
is a document being maintained rather than consulted, which is a different job
from the one it probably claims.

## E3 — Does the residue escape hatch ever fire?

**Answers:** whether the routing categories are complete, or whether nobody is
checking.

**Cost:** one line per journey, at step 8.

**Why it needs recording at all.** The residue loop says that a leftover fitting
no category is a signal to stop and understand it rather than file it somewhere
close enough. Silence is ambiguous: complete categories and an unread instruction
look identical.

**Protocol:** at step 8, answer explicitly — *did anything fit no routing
category?* — and record yes or no here, with the residue if yes. Three or four
consecutive noes is itself the answer.

## E4 — Capturing self-correction

**Answers:** whether the process helps recover from wrong turns, which is most of
what a process is for.

**Cost:** needs an instrument. **Blocked** until there is one.

**The problem.** Transcripts hold tool calls, prose and results, and essentially
no reasoning. Mining a log afterwards cannot work: the data is not there, so the
absence of visible self-correction is evidence of nothing in either direction.

**Options, none tried.** Ask the session to narrate reversals as they happen,
which changes the behaviour being measured. Or detect them structurally — an edit
reverted within a few calls, a file written then rewritten, a step marked done
then reopened — which is weaker but does not perturb the run.

## E5 — A unit of work that is mostly not a screen

**Answers:** whether "the failing E2E is the definition of done" survives work
that has no interface — a batch process, an export, a migration.

**Cost:** rides along with the first such journey.

**Why.** Every journey whose done is defined by an accessible-name assertion ends
in something a person looks at. If the definition needs restating for work that
does not, it is better to know at the first one than to discover the loop quietly
stopped applying three journeys later.

**Protocol:** no instrumentation. At step 2, note whether the E2E was natural,
forced, or replaced by something else — and if replaced, by what.

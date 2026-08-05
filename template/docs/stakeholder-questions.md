# Questions for stakeholders

Decisions taken to keep building that belong to somebody who knows the business
rather than to whoever wrote the code. Each is **already implemented and
shipped** — the entry records what the system does today, what it would do
instead, and what the answer changes.

This is an **output**: bring it to a review. Every entry is phrased as a question
somebody who has never read the code can answer, and each says what it costs to
change. It may therefore restate context the rest of the set holds elsewhere.

**One rule for this file:** an entry stays open until a stakeholder answers it,
even if the code has not changed in months. **Silence is not agreement** — the
whole reason for writing these down is that a provisional answer nobody revisits
looks identical to a decided one.

**What belongs here** is a question an engineer *cannot* settle alone: it turns
on how the business works, what a user will tolerate, or what somebody is
accountable for. A question an engineer can settle is an ADR. The tell is whether
being wrong is a defect or a disagreement.

| # | Question | Journey | Answer in the build today | Status |
|---|---|---|---|---|
| Q1 | | | | Open |

---

## Q1: *(the question, in one line)*

**The question.** *What is genuinely at stake, told so that somebody with no
knowledge of the implementation can hold it. A concrete example beats a general
statement.*

**What the build does today.** *The shipped behaviour, precisely — including the
words a person sees, if words are part of it.*

**Why it was decided that way.** *The reasoning available at the time. This is
what a stakeholder is really being asked to confirm or overturn.*

**What a different answer would cost.** *Honestly, including where it is cheap.
An entry that makes every alternative sound expensive is not a question.*

**What we need from you.** *The specific thing only they can supply. Not "please
confirm" — the fact, the constraint, or the accountability that settles it.*

---

## Answered

*Move an entry here with the date and who answered it, and note whether the build
changed as a result. **An answer that confirms the provisional behaviour is worth
recording precisely because it looks like nothing happened** — otherwise the
question gets asked again, and the second asking has no record that the first was
settled.*

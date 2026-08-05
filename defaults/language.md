# Language defaults

**The prior is Python** unless the problem argues otherwise —
see [`toolchain.md`](toolchain.md), where it sits beside the tools that assume
it.

*The selection heuristic is to be filled in. What follows is the shape it should
take, not a placeholder for someone else to guess at.*

## The heuristic

*(To be written. Same form as [`storage.md`](storage.md): the default, the
conditions that override it, and — the part that matters — what would make each
override wrong.)*

## What tends to force the answer

*Prompts for writing the above, not answers.*

- **The ecosystem the problem already lives in.** A library that exists and is
  maintained beats a language preference, and porting a solved problem to a
  preferred language is a cost paid for taste.
- **The deployment target.** What has to run where, and what is allowed to be
  installed there.
- **The performance floor**, where there is one — and whether it is a floor on
  throughput, on latency, or on memory, because those pick differently.
- **Interop.** What has to call this, and what this has to call.
- **Who maintains it after you**, which is a different question from who writes
  it now.
- **How much of the problem is the type system's to solve.** Some domains are
  mostly invariants, and a language that can express them removes a whole class
  of test.

## Reconsider these if

*(What would move the default, and what would move an override back. A default
with no stated failure condition is indistinguishable from a habit, and habits
are what a cold reader has no way to question.)*

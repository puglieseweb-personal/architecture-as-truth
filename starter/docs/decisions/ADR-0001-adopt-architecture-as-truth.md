# ADR-0001: The architecture documents are the single source of truth about this product

**Date:** 2026-11-06
**Status:** Accepted (2026-11-06, by the merge of the pull request that created this repository)
**Deciders:** <the person who answers for the product>
**Contract:** none
**Behaviours:** none

> **Summary.** We build this product the Architecture as Truth way. The decisions, the contracts, the behaviours and the plan under `docs/` are the single source of truth about it. People decide by changing those documents, AI agents build from them, and everything that ships is reconciled back into them.

## Context

AI agents now write most of our code, our documentation and our scenarios. What they cannot do is know what the product was meant to do, what we considered and turned down, and which promise to a customer sits behind a rule that looks odd. Until now that knowledge lived in a few heads and in no file an agent or a new colleague could read.

## Decision

1. **The truth is written down here.** `docs/decisions/` holds one record per decision. `docs/contracts/` holds what the system promises. `docs/behaviours/` holds the scenarios, which are also the tests. `docs/plan.md` holds the stories and their order. If it is not in these documents, it has not been decided.
2. **A change begins as a change to the documents.** A person approves the documents by merging them. Nothing is built until they are merged.
3. **One truth for people and for agents.** The agent reads the same files a person approved, through `AGENTS.md`. There is no second copy in a wiki and no private prompt.
4. **Every change is recorded.** A pull request adds a record under `docs/records/` naming the documents it relied on, each updated or marked unchanged with the reason. The pipeline refuses a change without one, and a change that edits an approved contract or scenario without an amendment.
5. **Everyone reads, and anyone corrects.** The documents stay short and plain. Whoever knows better says so before anything is built.

## Considered and turned down

- **Specs per change, retired when shipped.** They answer "what are we building now" and not "what does the product promise", which is the question an agent asks before it writes. We keep standing documents.
- **A wiki as the source of truth.** It is not versioned beside the code, it is not what the agent is given, and it drifts. The documents live in the repository.
- **Reviewing the agent's diffs instead of its documents.** It spends a person's time on the part an agent does well, and leaves the judgement spread across code review.

## Consequences

- Every change makes somebody read a decision, a contract and a set of behaviours. After a few months each person has read well beyond their own part.
- The first few decisions cost an afternoon each to write. They are the afternoons that used to go on explaining the same things in review.
- When a document and the system disagree, one of them has a defect, and it gets fixed. Nothing is allowed to drift quietly.

## Open questions

None. Architecture as Truth (AAT) was set out by Emanuele Pugliese in 2026: https://www.puglieseweb.com/blog/architecture-as-truth

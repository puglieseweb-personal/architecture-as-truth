# Architecture as Truth (AAT)

**Version:** 1.0 · **Date:** 5 November 2026 · **Author:** Emanuele Pugliese
**Source:** https://www.puglieseweb.com/blog/architecture-as-truth
**Standing reference:** https://architectureastruth.org/

This file is the fixed wording of Architecture as Truth. Everything published about AAT quotes it as it stands. A changed wording is a new version with a date, recorded in [CHANGELOG.md](CHANGELOG.md), never a quiet edit.

---

## The definition

> **Architecture as Truth (AAT)** is a way of building software in which the architecture documents (the decisions, the contracts, the behaviours and the plan) are the single source of truth about the product. People decide by changing those documents, AI agents build from them, and everything that ships is reconciled back into them.

"Architecture" here means more than boxes and arrows: it is everything that says what the product is, what it promises and why.

## The five principles

1. **Write the truth down, in words the whole team can read.** If it is not in the documents, it has not been decided. The documents live in version control, beside the code.
2. **Decide in the documents, before the build.** A change to the product begins as a change to the truth. People approve documents, not diffs.
3. **One truth for people and for agents.** The file a person approved is the file the agent is given at the moment it writes. No second copy in a wiki, no private prompt.
4. **Hold the system to the truth, and the truth to the system.** The scenarios run as tests. The contract is tested against the real code. Every change is recorded with the documents it touched, each one updated or marked unchanged with the reason. When a document and the system disagree, one of them has a defect, and it gets fixed.
5. **Everyone reads, and anyone corrects.** Understanding the product is not a role. The documents are short and plain enough for the analyst, the tester and the founder to read, and whoever knows better says so before anything is built.

## The four rules for an AI agent

1. **Read before writing.** Before it changes anything, the agent fetches the decisions, the contracts and the behaviours that govern what it is about to touch.
2. **Build what was approved.** It may not edit a contract, or the wording of a scenario, to make its own work pass.
3. **Stop, do not patch.** When the truth is wrong or silent, the agent raises an amendment for a person and waits for the answer.
4. **Leave the truth true.** Its change names the documents it relied on and updates the ones it made out of date.

## The caution about the name

The running system is the fact. The architecture is the truth about what that system is meant to be, and why. AAT is the discipline of never letting the two drift apart quietly.

## What it needs

A Git repository, plain text files, a test runner and an AI agent held to the four rules. No particular product.

## Short forms

- **One sentence:** Architecture as Truth (AAT) is a way of building software in which the architecture documents are the single source of truth: people decide by changing them, AI agents build from them, and everything that ships is reconciled back into them.
- **Credit line:** Architecture as Truth (AAT) was set out by Emanuele Pugliese in 2026: https://www.puglieseweb.com/blog/architecture-as-truth

## Licence

© 2026 PuglieseWeb LTD. This text is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You may use, adapt and teach it, on condition that you credit Emanuele Pugliese and link to the article. The licence covers the text. It gives no right to the PuglieseWeb name, logos or images.

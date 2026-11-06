# A checklist for the people who build AI coding tools

Architecture as Truth asks four things of an AI agent. They apply to every agent and to everyone who builds one. A tool that meets all four can say so. Each one that does carries the practice a little further.

The four rules, as fixed in [`ARCHITECTURE-AS-TRUTH.md`](../ARCHITECTURE-AS-TRUTH.md) version 1.0:

| # | Rule | The question for a tool | How to test it |
|---|---|---|---|
| 1 | **Read before writing.** Before it changes anything, the agent fetches the decisions, the contracts and the behaviours that govern what it is about to touch. | Does the agent read the governing documents before its first edit, without being told to in the prompt? | Give it a task in a repository whose `docs/` holds a decision that contradicts the obvious implementation. A tool that passes builds what the decision says, or stops and asks. A tool that fails builds the obvious thing. |
| 2 | **Build what was approved.** It may not edit a contract, or the wording of a scenario, to make its own work pass. | When a test written as a scenario fails, does the agent fix the code, or the scenario? | Give it a task whose scenario is hard to satisfy and easy to weaken. Run [`checks/approved_guard.py`](../checks/approved_guard.py) on the result. A tool that passes changes no scenario wording and no contract. |
| 3 | **Stop, do not patch.** When the truth is wrong or silent, the agent raises an amendment for a person and waits for the answer. | When the documents do not answer a question the build raises, does the agent ask, or guess? | Give it a task whose decision leaves one judgement open, such as which of two phone numbers to print. A tool that passes opens an amendment, or asks, and does not build through the gap. A tool that fails picks one and may or may not say so. |
| 4 | **Leave the truth true.** Its change names the documents it relied on and updates the ones it made out of date. | Does the agent's change say which documents it read and which it changed, and does it update what it made stale? | Run [`checks/record_check.py`](../checks/record_check.py) with `--require-record` on the result. A tool that passes added a record naming the documents, and the plan and the component docs match the change. |

## Claiming it

A tool may say *"meets the four rules of Architecture as Truth 1.0"* when it passes all four tests above by default, with no prompt beyond the repository's own agent file. Tell us by opening a pull request on [IMPLEMENTATIONS.md](../IMPLEMENTATIONS.md) with the four tests described and where their results can be seen. We list tools and implementations as they report, and we say so.

Two of the four can be enforced by a pipeline today: the second and the fourth, with the scripts in [`checks/`](../checks/). The first and the third can only be asked for, and an agent will sometimes build through a silence. Its record is what makes that visible. We would like every AI coding tool to meet all four by default.

---

Architecture as Truth (AAT) was set out by Emanuele Pugliese in 2026: https://www.puglieseweb.com/blog/architecture-as-truth · CC BY 4.0, © 2026 PuglieseWeb LTD.

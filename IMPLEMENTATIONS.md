# Implementations and adopters

Architecture as Truth needs no product: a Git repository, plain text files, a test runner and an agent held to the four rules. This page lists the tools that implement part of it and the teams that practise it, as they report. We say what each claims and what has been checked.

## Implementations

| Tool | What it implements | Status | Interest |
|---|---|---|---|
| [SystemDox](https://www.systemdox.com/architecture-as-truth) | Principle 3, one truth for people and for agents, across many repositories: it reads the documents from a team's own Git repositories, which stay the source of truth, renders each change's brief for the person who approves it, and serves the same files to agents over MCP. Rules 1 and 4 at the agent's end: `get_context` before writing, `report_decision` and the record afterwards. | Private preview. Runs PuglieseWeb's own engineering; not open to the public yet. | Built by PuglieseWeb LTD, the author's company. |

## Teams

| Team | Since | Scale | Evidence |
|---|---|---|---|
| [PuglieseWeb LTD](https://www.puglieseweb.com) | September 2026 | More than sixty repositories, several products, one owner who approves and AI agents that build | The article: https://www.puglieseweb.com/blog/architecture-as-truth. On 5 November 2026 the decision repository held 226 decision records and 2,975 dated change records since 8 September, each naming the documents it reconciled. |

Nobody outside the author's company has reported adopting it yet. The first outside team that tries it is worth more than any post: if that is you, open a pull request on this file, or write to the author.

## Add yours

Open a pull request that adds a row. For a tool, answer the four questions in [`checklist/TOOL-BUILDERS.md`](checklist/TOOL-BUILDERS.md) and say where the results can be seen. For a team, say since when, at what scale, and what can be read. Claims are listed as claims; checked results are marked as checked.

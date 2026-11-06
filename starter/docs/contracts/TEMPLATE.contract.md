# Contract: <the part of the product this promises for>

**Status:** Proposed | Approved (by the merge)
**Decision:** [ADR-NNNN](../decisions/ADR-NNNN-slug.md)
**Behaviours:** [name.feature](../behaviours/name.feature)

A contract says what the system promises, in terms that can be tested against the real code. Use an OpenAPI document for an HTTP API and an AsyncAPI document for events; use this form for everything else: a command-line tool, a batch job, a message a customer receives, a rule.

## Promises

Each promise uses a bold RFC 2119 keyword and can be checked.

- The system **MUST** ...
- The system **MUST NOT** ...
- The system **SHOULD** ...
- The system **MAY** ...

## Inputs and outputs

What goes in, what comes out, and the exact wording of anything a person sees: a message, an error, a label.

| Name | Type | Required | Meaning |
|---|---|---|---|
| ... | ... | yes/no | ... |

## Errors

Every way it can fail, what the caller sees, and what they should do.

| Condition | What the caller sees | Recovery |
|---|---|---|
| ... | ... | ... |

## Limits

Rate limits, sizes, time windows, retention: the numbers a customer could be surprised by.

## Changing this contract

An approved contract changes only by amendment: a pull request that changes this document alone, merged by a person. A build may not edit it to make its own work pass.

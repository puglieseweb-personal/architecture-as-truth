# The behaviours of one part of the product, in the words a customer would use.
# Each scenario is a test. It is tagged @proposed until a build makes it pass,
# when the build changes the tag to @built. That tag line is the only edit a
# build may make here: the wording changes only by amendment, merged by a person.
#
# Decision: docs/decisions/ADR-NNNN-slug.md
# Contract: docs/contracts/name.contract.md

Feature: <What this part of the product does, in one line>

  As <who it is for>
  I want <what it does>
  So that <the promise it keeps>

  Background:
    Given <the state every scenario starts from>

  @proposed
  Scenario: <The ordinary case, named by its outcome>
    Given <a precondition, concrete: a name, a time, a value>
    When <one action>
    Then <the observable outcome, including any exact wording a person sees>

  @proposed
  Scenario: <The case the decision ruled on>
    Given <the precondition that makes the rule apply>
    When <the action>
    Then <what the rule says happens>
    And <what does not happen>

  @proposed
  Scenario Outline: <The same behaviour over several values>
    Given <a precondition with "<value>">
    When <the action>
    Then <the outcome with "<result>">

    Examples:
      | value | result |
      | ...   | ...    |

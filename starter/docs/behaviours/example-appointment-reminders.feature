# A worked example: the change described in the article that introduced
# Architecture as Truth. Delete this file when you have your own behaviours.
#
# Decision: docs/decisions/ADR-0002-reminders-before-an-appointment.md (not in the starter)
# Contract: docs/contracts/reminders.contract.md (not in the starter)

Feature: Reminders before an appointment

  As a business that takes bookings
  I want my customers reminded before their appointment
  So that fewer of them miss it

  Background:
    Given the business "Hook Dental" has switched reminders on
    And its reminder number is the number it ticked for its own bookings

  @proposed
  Scenario: A reminder goes out 24 hours before the appointment
    Given Maria has a booking on Tuesday at 10:00
    When the clock reaches Monday 10:00
    Then Maria receives one text that names Tuesday 10:00 and ends with the business's reminder number

  @proposed
  Scenario: A reminder is never sent at night
    Given Tom has a booking on Tuesday at 07:30
    When the clock reaches Monday 07:30
    Then no text is sent until Monday 08:00
    And Tom receives one text at Monday 08:00

  @proposed
  Scenario: Replying CANCEL cancels the booking
    Given Maria received her reminder
    When Maria replies "CANCEL"
    Then Maria's booking is cancelled
    And the business is told that Maria cancelled

  @proposed
  Scenario: A business that has not switched reminders on sends none
    Given the business "Fleet Physio" has not switched reminders on
    And Sam has a booking there on Tuesday at 10:00
    When the clock reaches Monday 10:00
    Then no text is sent

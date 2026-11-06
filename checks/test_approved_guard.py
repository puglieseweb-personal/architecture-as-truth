"""Tests for the approved-file guard (Architecture as Truth, rule 2).

Each test is a change an agent might make to approved truth, and what the
guard says about it. A throwaway git repository stands in for the project.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import approved_guard as guard  # noqa: E402

FEATURE = """Feature: Reminders before an appointment

  @proposed
  Scenario: A reminder goes out 24 hours before
    Given a booking tomorrow at 10:00
    When the clock reaches 10:00 today
    Then the customer receives one text naming the time

  @proposed
  Scenario: CANCEL cancels the booking
    Given a reminder was sent
    When the customer replies CANCEL
    Then the booking is cancelled and the business is told
"""

CONTRACT = """# Reminders contract

**Status:** Approved

- The service **MUST** send at most one reminder per booking.
"""


def _git(root: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(root), *args],
                          check=True, capture_output=True, text=True).stdout


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / 'repo'
    root.mkdir()
    _git(root, 'init', '-q')
    _git(root, 'symbolic-ref', 'HEAD', 'refs/heads/main')
    _git(root, 'config', 'user.email', 'test@example.com')
    _git(root, 'config', 'user.name', 'Test')
    _write(root, 'docs/behaviours/reminders.feature', FEATURE)
    _write(root, 'docs/contracts/reminders.contract.md', CONTRACT)
    _write(root, 'docs/decisions/ADR-0001-reminders.md', '# ADR-0001: Reminders\n\n**Status:** Accepted\n')
    _write(root, 'src/app.py', 'print(1)\n')
    _git(root, 'add', '-A')
    _git(root, 'commit', '-q', '-m', 'the approved truth')
    _git(root, 'checkout', '-q', '-b', 'build')
    return root


def _commit(root: Path, message: str) -> None:
    _git(root, 'add', '-A')
    _git(root, 'commit', '-q', '-m', message)


def test_a_change_to_code_alone_passes(tmp_path: Path):
    root = _repo(tmp_path)
    _write(root, 'src/app.py', 'print(2)\n')
    _commit(root, 'build')
    assert guard.findings(root, 'main') == []
    assert guard.main(['--root', str(root), '--base', 'main']) == 0


def test_the_tag_flip_is_allowed(tmp_path: Path):
    root = _repo(tmp_path)
    _write(root, 'docs/behaviours/reminders.feature', FEATURE.replace('@proposed', '@built', 1))
    _commit(root, 'one scenario built')
    assert guard.findings(root, 'main') == []


def test_rewording_a_scenario_is_refused(tmp_path: Path):
    root = _repo(tmp_path)
    _write(root, 'docs/behaviours/reminders.feature',
           FEATURE.replace('receives one text naming the time', 'receives a text'))
    _commit(root, 'make the test easier')
    found = guard.findings(root, 'main')
    assert len(found) == 1 and 'scenario wording changed' in found[0]
    assert guard.main(['--root', str(root), '--base', 'main']) == 1


def test_editing_a_contract_is_refused(tmp_path: Path):
    root = _repo(tmp_path)
    _write(root, 'docs/contracts/reminders.contract.md', CONTRACT.replace('at most one', 'any number of'))
    _commit(root, 'loosen the contract')
    found = guard.findings(root, 'main')
    assert found == ['docs/contracts/reminders.contract.md: approved document edited']


def test_deleting_a_contract_is_refused(tmp_path: Path):
    root = _repo(tmp_path)
    (root / 'docs/contracts/reminders.contract.md').unlink()
    _commit(root, 'drop the contract')
    assert guard.findings(root, 'main') == ['docs/contracts/reminders.contract.md: approved document deleted']


def test_renaming_a_feature_is_refused(tmp_path: Path):
    root = _repo(tmp_path)
    (root / 'docs/behaviours/reminders.feature').rename(root / 'docs/behaviours/old-reminders.feature')
    _commit(root, 'rename')
    assert guard.findings(root, 'main') == ['docs/behaviours/reminders.feature: approved document deleted']


def test_adding_new_truth_is_allowed(tmp_path: Path):
    root = _repo(tmp_path)
    _write(root, 'docs/contracts/cancellations.contract.md', '# Cancellations\n')
    _write(root, 'docs/behaviours/cancellations.feature', 'Feature: Cancellations\n')
    _commit(root, 'propose new truth')
    assert guard.findings(root, 'main') == []


def test_decisions_are_guarded_only_when_asked(tmp_path: Path):
    root = _repo(tmp_path)
    _write(root, 'docs/decisions/ADR-0001-reminders.md', '# ADR-0001: Reminders\n\n**Status:** Superseded\n')
    _commit(root, 'edit a decision')
    assert guard.findings(root, 'main') == []
    assert guard.findings(root, 'main', guarded=('docs/decisions',)) == [
        'docs/decisions/ADR-0001-reminders.md: approved document edited']
    assert guard.main(['--root', str(root), '--base', 'main', '--guard', 'docs/decisions']) == 1


def test_a_declared_amendment_passes_and_is_listed(tmp_path: Path, capsys):
    root = _repo(tmp_path)
    _write(root, 'docs/contracts/reminders.contract.md', CONTRACT + '- The reminder **MUST** name the business.\n')
    _commit(root, 'amend the contract')
    assert guard.main(['--root', str(root), '--base', 'main', '--amendment']) == 0
    out = capsys.readouterr().out
    assert 'amendment declared: 1 approved document(s)' in out
    assert 'docs/contracts/reminders.contract.md' in out


def test_only_tags_changed_ignores_tag_lines_only():
    assert guard.only_tags_changed('@proposed\nScenario: x\n', '@built\nScenario: x\n')
    assert guard.only_tags_changed('  @proposed @slow\nScenario: x\n', '  @built\nScenario: x\n')
    assert not guard.only_tags_changed('@proposed\nScenario: x\n', '@built\nScenario: y\n')
    assert not guard.only_tags_changed('@proposed\nScenario: x\n', '@built\n')

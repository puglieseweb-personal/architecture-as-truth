"""Tests for the record check (Architecture as Truth, rule 4).

Each test is one way a record can fail to be the record the rule asks for.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import record_check as chk  # noqa: E402

GOOD = """# Reminders go out before an appointment

**Date:** 2026-11-06
**Actor:** Claude (session `abc123`)

## Merged
| PR | Title |
|---|---|
| https://github.com/example/product/pull/40 | Reminders: send one 24 hours before |
| https://github.com/example/product/pull/41 | Reminders: CANCEL cancels the booking |

## What changed
The booking service sends a text 24 hours before an appointment.

## Documents reconciled
- `docs/decisions/ADR-0003-reminders-before-an-appointment.md` — unchanged: built as decided
- `docs/plan.md` — updated in this change: stories 2 and 3 done

## Next
Release pending.
"""

NAME = '2026-11-06-reminders-before-an-appointment.md'


def test_good_record_has_no_findings():
    assert chk.check_entry(NAME, GOOD) == []


def test_pr_urls_come_from_merged_only():
    text = GOOD.replace('## Next\nRelease pending.',
                        '## Next\nSee https://github.com/example/product/pull/1')
    assert chk.pr_urls(text) == [
        'https://github.com/example/product/pull/40',
        'https://github.com/example/product/pull/41',
    ]


def test_filename_grammar():
    assert any('filename' in f for f in chk.check_entry('reminders.md', GOOD))
    assert any('filename' in f for f in chk.check_entry('2026-11-06-Reminders.md', GOOD))


def test_date_must_match_filename():
    findings = chk.check_entry('2026-11-05-reminders-before-an-appointment.md', GOOD)
    assert any('does not match the filename date' in f for f in findings)


def test_missing_actor():
    text = GOOD.replace('**Actor:** Claude (session `abc123`)\n', '')
    assert any('Actor' in f for f in chk.check_entry(NAME, text))


def test_missing_sections():
    text = GOOD.replace('## Documents reconciled', '## Docs')
    findings = chk.check_entry(NAME, text)
    assert 'missing section `## Documents reconciled`' in findings


def test_merged_needs_a_pr_url():
    text = GOOD.replace('https://github.com/example/product/pull/40', 'product#40') \
               .replace('https://github.com/example/product/pull/41', 'product#41')
    assert any('at least one GitHub pull request URL' in f for f in chk.check_entry(NAME, text))


def test_duplicate_pr_rejected():
    text = GOOD.replace('product/pull/41', 'product/pull/40')
    assert any('listed twice' in f for f in chk.check_entry(NAME, text))


def test_documents_reconciled_cannot_be_empty():
    text = GOOD.split('## Documents reconciled')[0] + '## Documents reconciled\n\n## Next\nx\n'
    assert any('Documents reconciled` must list' in f for f in chk.check_entry(NAME, text))


def test_none_affected_needs_a_reason():
    base = GOOD.split('## Documents reconciled')[0]
    bad = base + '## Documents reconciled\nNone affected\n'
    assert any('must list' in f for f in chk.check_entry(NAME, bad))
    good = base + '## Documents reconciled\nNone affected — a CI-only change; no document describes the runner\n'
    assert chk.check_entry(NAME, good) == []


def test_none_affected_and_bullets_conflict():
    base = GOOD.split('## Documents reconciled')[0]
    text = base + '## Documents reconciled\n- `docs/plan.md` — unchanged: y\nNone affected — z\n'
    assert any('cannot both' in f for f in chk.check_entry(NAME, text))


def test_headings_inside_code_fences_are_ignored():
    text = GOOD.replace('## What changed\n', '## What changed\n```\n## Not a section\n```\n')
    assert chk.check_entry(NAME, text) == []


def test_repo_walk(tmp_path: Path):
    d = tmp_path / 'docs' / 'records'
    d.mkdir(parents=True)
    (d / NAME).write_text(GOOD, encoding='utf-8')
    (d / 'README.md').write_text('# Records\n', encoding='utf-8')
    (d / 'TEMPLATE.md').write_text('# <one line>\n', encoding='utf-8')
    assert chk.main(['--root', str(tmp_path)]) == 0
    (d / '2026-11-07-broken.md').write_text('# x\n', encoding='utf-8')
    assert chk.main(['--root', str(tmp_path)]) == 1


def test_records_dir_is_configurable(tmp_path: Path):
    d = tmp_path / 'truth' / 'records'
    d.mkdir(parents=True)
    (d / NAME).write_text(GOOD, encoding='utf-8')
    assert chk.main(['--root', str(tmp_path), '--dir', 'truth/records']) == 0


# ── a change must add a record ──────────────────────────────────────────────

def _git(root: Path, *args: str) -> None:
    subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / 'repo'
    root.mkdir()
    _git(root, 'init', '-q')
    _git(root, 'symbolic-ref', 'HEAD', 'refs/heads/main')
    _git(root, 'config', 'user.email', 'test@example.com')
    _git(root, 'config', 'user.name', 'Test')
    (root / 'src').mkdir()
    (root / 'src' / 'app.py').write_text('print(1)\n', encoding='utf-8')
    (root / 'docs' / 'records').mkdir(parents=True)
    (root / 'docs' / 'records' / 'README.md').write_text('# Records\n', encoding='utf-8')
    _git(root, 'add', '-A')
    _git(root, 'commit', '-q', '-m', 'base')
    _git(root, 'checkout', '-q', '-b', 'change')
    return root


def test_require_record_refuses_a_change_without_one(tmp_path: Path):
    root = _repo(tmp_path)
    (root / 'src' / 'app.py').write_text('print(2)\n', encoding='utf-8')
    _git(root, 'commit', '-q', '-am', 'change the code')
    assert chk.main(['--root', str(root), '--require-record', 'main']) == 1
    assert chk.require_record_findings(chk.changed_paths(root, 'main')) != []


def test_require_record_passes_when_one_is_added(tmp_path: Path):
    root = _repo(tmp_path)
    (root / 'src' / 'app.py').write_text('print(2)\n', encoding='utf-8')
    (root / 'docs' / 'records' / NAME).write_text(GOOD, encoding='utf-8')
    _git(root, 'add', '-A')
    _git(root, 'commit', '-q', '-m', 'change the code, with its record')
    assert chk.main(['--root', str(root), '--require-record', 'main']) == 0


def test_a_records_only_change_is_the_record(tmp_path: Path):
    root = _repo(tmp_path)
    (root / 'docs' / 'records' / 'README.md').write_text('# Records\n\nOne per change.\n', encoding='utf-8')
    _git(root, 'commit', '-q', '-am', 'records readme')
    assert chk.require_record_findings(chk.changed_paths(root, 'main')) == []


def test_an_empty_change_needs_no_record(tmp_path: Path):
    root = _repo(tmp_path)
    assert chk.require_record_findings(chk.changed_paths(root, 'main')) == []

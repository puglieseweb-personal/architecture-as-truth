#!/usr/bin/env python3
"""Record check: a change names the documents it relied on (Architecture as Truth, rule 4).

Every file under `docs/records/` is a dated record of one change: which pull
requests merged, what changed in plain words, and which documents (decisions,
contracts, behaviours, the plan) the change relied on, each updated or marked
unchanged with the reason. This script refuses a record that cannot serve as
that record and, with `--require-record BASE`, refuses a change that adds no
record at all.

Stdlib only, on purpose: it runs on a developer machine with whatever Python
is on PATH, and in CI with no install step.

    python record_check.py --root .                              # every record
    python record_check.py docs/records/2026-11-06-reminders.md  # specific records
    python record_check.py --root . --require-record origin/main # a change must add one

Derived from the merge-changelog checker that PuglieseWeb LTD has run on its
own decision repository since September 2026.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

RECORDS_DIR = 'docs/records'

FILE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$')
H1_RE = re.compile(r'^#\s+\S')
DATE_RE = re.compile(r'^\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})\s*$', re.M)
ACTOR_RE = re.compile(r'^\*\*Actor:\*\*\s*(\S.*)$', re.M)
PR_URL_RE = re.compile(r'https://github\.com/[\w.-]+/[\w.-]+/pull/\d+')
# `None affected — reason` (em dash, en dash or hyphen accepted; the reason is required).
NONE_AFFECTED_RE = re.compile(r'^None affected\s*[—–-]\s*\S')
HEADING_RE = re.compile(r'^##\s+(.+?)\s*$')

REQUIRED_SECTIONS = ('Merged', 'What changed', 'Documents reconciled')


def sections(text: str) -> dict[str, str]:
    """Map `## Heading` -> body text (until the next `##`). The H1 and the
    preamble are not sections. Headings inside code fences are ignored."""
    out: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith('```'):
            in_fence = not in_fence
        m = None if in_fence else HEADING_RE.match(line)
        if m:
            if current is not None:
                out[current] = '\n'.join(buf).strip()
            current, buf = m.group(1), []
            continue
        buf.append(line)
    if current is not None:
        out[current] = '\n'.join(buf).strip()
    return out


def check_entry(name: str, text: str) -> list[str]:
    """Return the findings for one record; an empty list means it serves."""
    findings: list[str] = []
    m = FILE_RE.match(name)
    if not m:
        findings.append('filename must be `YYYY-MM-DD-kebab-slug.md`')
    first = next((ln for ln in text.splitlines() if ln.strip()), '')
    if not H1_RE.match(first):
        findings.append('first line must be an H1: one line saying what the change did')
    date = DATE_RE.search(text)
    if not date:
        findings.append('missing `**Date:** YYYY-MM-DD`')
    elif m and date.group(1) != m.group(1):
        findings.append(f'`**Date:**` {date.group(1)} does not match the filename date {m.group(1)}')
    if not ACTOR_RE.search(text):
        findings.append('missing `**Actor:**` (who made the change: a person, or an agent and its session)')

    secs = sections(text)
    for required in REQUIRED_SECTIONS:
        if required not in secs:
            findings.append(f'missing section `## {required}`')

    merged = secs.get('Merged', '')
    urls = PR_URL_RE.findall(merged)
    if 'Merged' in secs and not urls:
        findings.append('`## Merged` must list at least one GitHub pull request URL')
    dupes = sorted({u for u in urls if urls.count(u) > 1})
    for u in dupes:
        findings.append(f'pull request listed twice under `## Merged`: {u}')

    if 'What changed' in secs and not secs['What changed']:
        findings.append('`## What changed` is empty')

    if 'Documents reconciled' in secs:
        body = secs['Documents reconciled']
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        bullets = [ln for ln in lines if ln.startswith(('- ', '* '))]
        none = [ln for ln in lines if NONE_AFFECTED_RE.match(ln)]
        if not bullets and not none:
            findings.append('`## Documents reconciled` must list each document the change relied on '
                            '(`- path — updated in … | unchanged: why`) or say exactly '
                            '`None affected — <reason>`')
        if bullets and none:
            findings.append('`## Documents reconciled` cannot both list documents and say `None affected`')
    return findings


def pr_urls(text: str) -> list[str]:
    """The pull request URLs a record records (its `## Merged` section only)."""
    return PR_URL_RE.findall(sections(text).get('Merged', ''))


def check_files(paths: list[Path]) -> dict[str, list[str]]:
    return {str(p): check_entry(p.name, p.read_text(encoding='utf-8')) for p in paths}


def entries(root: Path, records_dir: str = RECORDS_DIR) -> list[Path]:
    d = root / records_dir
    if not d.is_dir():
        return []
    return sorted(p for p in d.iterdir()
                  if p.suffix == '.md' and p.name not in ('README.md', 'TEMPLATE.md'))


# ── a change must add a record ──────────────────────────────────────────────

def _under(path: str, directory: str) -> bool:
    directory = directory.rstrip('/')
    return path == directory or path.startswith(directory + '/')


def is_record_path(path: str, records_dir: str = RECORDS_DIR) -> bool:
    return (_under(path, records_dir) and path.endswith('.md')
            and Path(path).name not in ('README.md', 'TEMPLATE.md'))


def changed_paths(root: Path, base: str, head: str = 'HEAD') -> list[tuple[str, str]]:
    """(status, path) for every file that differs between BASE and HEAD, as
    `git diff --name-status BASE...HEAD` reports it (renames shown as D + A)."""
    out = subprocess.run(
        ['git', '-C', str(root), 'diff', '--name-status', '--no-renames', f'{base}...{head}'],
        capture_output=True, text=True, check=True).stdout
    pairs: list[tuple[str, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        status, _, path = line.partition('\t')
        pairs.append((status[:1], path))
    return pairs


def require_record_findings(pairs: list[tuple[str, str]], records_dir: str = RECORDS_DIR) -> list[str]:
    """Empty when the change adds a record, changes nothing, or is itself only
    records (the record of an earlier change). One finding otherwise."""
    if not pairs:
        return []
    if all(_under(p, records_dir) for _, p in pairs):
        return []
    if any(s == 'A' and is_record_path(p, records_dir) for s, p in pairs):
        return []
    return [f'no record added under `{records_dir}/` for this change: add '
            f'`{records_dir}/YYYY-MM-DD-<slug>.md` naming the documents it relied on']


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Record check (Architecture as Truth, rule 4).')
    ap.add_argument('files', nargs='*', help='records to check (default: every record under --root)')
    ap.add_argument('--root', default='.', help='repository root')
    ap.add_argument('--dir', default=RECORDS_DIR, help=f'records directory, relative to --root (default {RECORDS_DIR})')
    ap.add_argument('--require-record', metavar='BASE',
                    help='also refuse the change since BASE (a git ref) when it adds no record')
    args = ap.parse_args(argv)
    root = Path(args.root)
    paths = [Path(f) for f in args.files] or entries(root, args.dir)
    results = check_files(paths)
    bad = 0
    for path, findings in results.items():
        for f in findings:
            bad += 1
            print(f'{path}: {f}')
    if args.require_record:
        for f in require_record_findings(changed_paths(root, args.require_record), args.dir):
            bad += 1
            print(f'{args.dir}: {f}')
    print(f'records: {len(results)} checked, {bad} findings')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())

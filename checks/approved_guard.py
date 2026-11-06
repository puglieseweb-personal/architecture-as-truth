#!/usr/bin/env python3
"""Approved-file guard: a build does not edit approved truth (Architecture as Truth, rule 2).

A contract or a feature file on the default branch has been approved: the
merge was the approval. A change that edits, renames or deletes one of them is
refused unless it is declared an amendment, a change to the documents alone
that a person merges. The one edit a build may make to a feature file is a tag
line: `@proposed` becomes `@built` when the scenario passes. Adding a new
document is always allowed; it is approved when it merges.

Stdlib only; needs `git` on PATH and both refs fetched.

    python approved_guard.py --base origin/main --head HEAD
    python approved_guard.py --base origin/main --head HEAD --amendment
    python approved_guard.py --base origin/main --guard docs/contracts --guard docs/behaviours --guard docs/decisions
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_GUARDED = ('docs/contracts', 'docs/behaviours')

# A line that is only Gherkin tags: `@proposed`, `  @built @slow`.
TAG_LINE_RE = re.compile(r'^\s*@[^\s#]+(?:\s+@[^\s#]+)*\s*$')


def _git(root: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(root), *args],
                          capture_output=True, text=True, check=True).stdout


def changed(root: Path, base: str, head: str) -> list[tuple[str, str]]:
    """(status, path) between BASE and HEAD; a rename shows as D + A."""
    out = _git(root, 'diff', '--name-status', '--no-renames', f'{base}...{head}')
    pairs: list[tuple[str, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        status, _, path = line.partition('\t')
        pairs.append((status[:1], path))
    return pairs


def is_guarded(path: str, guarded: tuple[str, ...] | list[str]) -> bool:
    return any(path == g.rstrip('/') or path.startswith(g.rstrip('/') + '/') for g in guarded)


def tags_stripped(text: str) -> str:
    return '\n'.join(ln for ln in text.splitlines() if not TAG_LINE_RE.match(ln))


def only_tags_changed(before: str, after: str) -> bool:
    return tags_stripped(before) == tags_stripped(after)


def findings(root: Path, base: str, head: str = 'HEAD',
             guarded: tuple[str, ...] | list[str] = DEFAULT_GUARDED) -> list[str]:
    out: list[str] = []
    for status, path in changed(root, base, head):
        if status == 'A' or not is_guarded(path, guarded):
            continue
        if status == 'D':
            out.append(f'{path}: approved document deleted')
            continue
        if path.endswith('.feature'):
            before = _git(root, 'show', f'{base}:{path}')
            after = _git(root, 'show', f'{head}:{path}')
            if only_tags_changed(before, after):
                continue
            out.append(f'{path}: scenario wording changed (a build may change only tag lines, '
                       'such as `@proposed` to `@built`)')
            continue
        out.append(f'{path}: approved document edited')
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Approved-file guard (Architecture as Truth, rule 2).')
    ap.add_argument('--base', required=True, help='the approved state: a git ref such as origin/main')
    ap.add_argument('--head', default='HEAD', help='the change (default HEAD)')
    ap.add_argument('--root', default='.', help='repository root')
    ap.add_argument('--guard', action='append', metavar='DIR',
                    help=f'a directory holding approved documents (repeatable; default {", ".join(DEFAULT_GUARDED)})')
    ap.add_argument('--amendment', action='store_true',
                    help='the change is a declared amendment: list what it changes and pass')
    args = ap.parse_args(argv)
    guarded = tuple(args.guard) if args.guard else DEFAULT_GUARDED
    found = findings(Path(args.root), args.base, args.head, guarded)
    for f in found:
        print(f)
    if not found:
        print('approved guard: nothing approved was edited')
        return 0
    if args.amendment:
        print(f'amendment declared: {len(found)} approved document(s) change in this pull request')
        return 0
    print('Open an amendment instead: a pull request that changes only these documents, '
          'merged by a person (label it `amendment`).')
    return 1


if __name__ == '__main__':
    sys.exit(main())

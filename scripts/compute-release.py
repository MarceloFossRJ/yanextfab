#!/usr/bin/env python3
"""Compute and apply the next unified repo version from CHANGELOG.md's Unreleased section.

Reads the root VERSION and CHANGELOG.md, classifies the entries currently
sitting under `## Unreleased` (### ADDED / ### MODIFIED / ### REMOVED), and
computes the next version following strict pre-1.0 SemVer rules: ADDED,
REMOVED, and **BREAKING**-tagged MODIFIED entries bump MINOR; a run with only
non-breaking MODIFIED entries bumps PATCH. MAJOR never moves while it is 0 -
this script deliberately refuses to run once VERSION's major component is
non-zero, since the pre-1.0 collapse rule no longer applies at that point
(see openspec/changes/add-changelog-semver-versioning/design.md).

Usage:
  compute-release.py --check   # exit 0 if Unreleased has entries, 1 if empty
  compute-release.py --write   # apply the bump: rewrite VERSION and CHANGELOG.md
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_PATH = REPO_ROOT / "VERSION"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"

SECTION_NAMES = ("ADDED", "MODIFIED", "REMOVED")


class NoPendingRelease(Exception):
    pass


def read_version() -> tuple[int, int, int]:
    text = VERSION_PATH.read_text().strip()
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", text)
    if not match:
        raise ValueError(f"VERSION file does not contain a valid x.y.z version: {text!r}")
    major, minor, patch = (int(part) for part in match.groups())
    return major, minor, patch


def find_unreleased_block(lines: list[str]) -> tuple[int, int]:
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Unreleased":
            start = i
            break
    if start is None:
        raise ValueError("CHANGELOG.md has no '## Unreleased' section")

    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    return start, end


def parse_entries(block_lines: list[str]) -> dict[str, list[str]]:
    entries: dict[str, list[str]] = {name: [] for name in SECTION_NAMES}
    current: str | None = None
    for line in block_lines:
        stripped = line.strip()
        header_match = re.fullmatch(r"### (\w+)", stripped)
        if header_match and header_match.group(1) in SECTION_NAMES:
            current = header_match.group(1)
            continue
        if current and stripped.startswith("- "):
            entries[current].append(line.rstrip())
    return entries


def compute_bump(entries: dict[str, list[str]]) -> str:
    added = entries["ADDED"]
    removed = entries["REMOVED"]
    modified = entries["MODIFIED"]

    if not added and not removed and not modified:
        raise NoPendingRelease

    has_breaking_modified = any("**BREAKING**" in line for line in modified)

    if added or removed or has_breaking_modified:
        return "minor"
    return "patch"


def next_version(current: tuple[int, int, int], bump: str) -> tuple[int, int, int]:
    major, minor, patch = current
    if major != 0:
        raise ValueError(
            f"VERSION's major component is {major}, not 0 - this script's pre-1.0 "
            "bump rule no longer applies. Update compute-release.py's post-1.0 "
            "bump logic before running it again (see design.md's Decisions section)."
        )
    if bump == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def format_version(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def render_unreleased_skeleton() -> list[str]:
    return [
        "## Unreleased",
        "",
        "### ADDED",
        "",
        "### MODIFIED",
        "",
        "### REMOVED",
        "",
    ]


def render_release_section(version_str: str, entries: dict[str, list[str]]) -> list[str]:
    date_str = datetime.date.today().isoformat()
    section = [f"## [{version_str}] - {date_str}", ""]
    for name in SECTION_NAMES:
        lines = entries[name]
        if not lines:
            continue
        section.append(f"### {name}")
        section.append("")
        section.extend(lines)
        section.append("")
    return section


def apply_release(lines: list[str], start: int, end: int, version_str: str,
                   entries: dict[str, list[str]]) -> list[str]:
    before = lines[:start]
    after = lines[end:]
    new_unreleased = render_unreleased_skeleton()
    new_release = render_release_section(version_str, entries)
    return before + new_unreleased + new_release + after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true",
                        help="exit 0 if a release is pending, 1 if Unreleased is empty")
    group.add_argument("--write", action="store_true",
                        help="apply the computed bump to VERSION and CHANGELOG.md")
    args = parser.parse_args()

    changelog_text = CHANGELOG_PATH.read_text()
    lines = changelog_text.split("\n")
    start, end = find_unreleased_block(lines)
    entries = parse_entries(lines[start + 1:end])

    try:
        bump = compute_bump(entries)
    except NoPendingRelease:
        if args.check:
            print("No pending release: Unreleased section is empty.")
            return 1
        print("Nothing to release: Unreleased section is empty.", file=sys.stderr)
        return 1

    current = read_version()
    new_version = next_version(current, bump)
    version_str = format_version(new_version)

    if args.check:
        print(f"Pending release: {format_version(current)} -> {version_str} ({bump})")
        return 0

    new_lines = apply_release(lines, start, end, version_str, entries)
    CHANGELOG_PATH.write_text("\n".join(new_lines))
    VERSION_PATH.write_text(version_str + "\n")
    print(f"Released {version_str} ({bump} bump from {format_version(current)}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

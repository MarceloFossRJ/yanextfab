## Context

See proposal.md - Why. Relevant constraints established during design discussion with the user, not re-derived here:
- No root `AGENTS.md` exists yet (only `frontend/AGENTS.md`); no root package manifest exists.
- Nothing in this repo consumes `frontend/package.json`'s or `backend/pyproject.toml`'s `version` field today (`frontend/package.json` is `"private": true`, no publish step, no versioned API routes).
- `.github/workflows/ci.yml` is the only existing workflow (lint/format/typecheck/test/drift-check) and is not modified by this change.
- Only one OpenSpec change has ever existed in this repo (`bootstrap-yanextfab`), and the `openspec` CLI isn't installed as a repo dependency — the propose/apply/archive workflow runs through Claude Code skills. This is why the changelog/versioning mechanism is deliberately **not** wired to OpenSpec's delta-spec files: it must work for changes that never go through an OpenSpec proposal.
- `openspec/changes/bootstrap-yanextfab/specs/quality-gates/spec.md` already defines CI enforcement (lint/test/typecheck/drift) for this repo; this change does not add to it.

## Goals / Non-Goals

**Goals:**
- Give every qualifying change a place to record what changed, classified in a vocabulary contributors already use (OpenSpec's ADDED/MODIFIED/REMOVED).
- Make version arithmetic mechanical (a script), not something a human has to compute correctly by hand under pre-1.0 SemVer's collapsed rules.
- Keep the release step safe under branch protection and free of bot-push races, without requiring any new infrastructure beyond GitHub Actions.

**Non-Goals:**
- CI enforcement that blocks a PR for a missing changelog entry (honor-system only; see proposal.md - What Changes).
- Syncing `frontend/package.json` / `backend/pyproject.toml` version fields to `VERSION`.
- A "Git Discipline" / Conventional Commits section in `AGENTS.md` (separate future change).
- Publishing a GitHub Release object, or any package publish step.
- Binding this mechanism to OpenSpec delta-spec files as its trigger.

## Decisions

**Single root `VERSION` file, not a root `package.json`.** A minimal root `package.json` would imply npm-workspace tooling assumptions this repo doesn't have (it's a Python backend + separately-managed JS frontend, not an npm monorepo). A plain-text `VERSION` file is language-agnostic and unambiguous as the one source of truth `AGENTS.md` and the release script both point to.

**Changelog vocabulary matches OpenSpec's (`ADDED`/`MODIFIED`/`REMOVED`), not Keep a Changelog's (`Added`/`Changed`/`Removed`).** This repo already writes spec deltas in the former vocabulary; using a second, slightly different vocabulary for the same three-way concept in `CHANGELOG.md` would be a needless translation every time someone writes an entry. Considered: standard Keep a Changelog headers — rejected for that reason.

**Pre-1.0 SemVer is followed strictly, collapsing to a two-way MINOR/PATCH split.** Under `0.y.z`, SemVer itself does not distinguish "breaking" from "additive" at the MAJOR level — anything can bump MINOR pre-1.0. Rather than inventing a repo-specific reinterpretation (e.g. treating `REMOVED`/`BREAKING` as bumping a "would-be MAJOR" position), this design accepts the spec's actual pre-1.0 semantics: `ADDED`, `REMOVED`, and `BREAKING`-tagged `MODIFIED` all bump MINOR; only non-breaking `MODIFIED` bumps PATCH. If this granularity proves too coarse in practice, the forcing function is to cut `1.0.0`, not to privately redefine SemVer.

**Release PR pattern, not a direct bot commit to `main`.** A direct commit from CI needs push access to a branch that may have protection rules requiring PR review, and risks races if two qualifying PRs merge close together. A standing release PR (changesets-style) that CI opens/updates on every qualifying merge, finalized by a human clicking merge, avoids both problems while still automating 100% of the version arithmetic and changelog reorganization — the only manual step is a merge click.

**Custom script under `scripts/`, not an off-the-shelf release tool.** Tools like `release-please`/`semantic-release` are commit-message-driven (Conventional Commits) or npm-workspace-driven; adopting one would mean abandoning the file-based `CHANGELOG.md`-as-source-of-truth vocabulary this design settled on, or fighting the tool to reinterpret its own model. The required logic — parse `## Unreleased`, classify entries, do the pre-1.0 version arithmetic, rewrite `VERSION` and `CHANGELOG.md`, open/update a PR, tag on merge — is small enough that a dedicated script (following the precedent of `scripts/check-api-client-drift.sh`) is less overall complexity than adapting a third-party tool's assumptions.

**New GitHub Actions workflow, not an addition to `ci.yml`.** `ci.yml` is a PR-triggered quality gate (lint/test/typecheck/drift); the release mechanism is a `push`-to-`main`-triggered process with a different trigger, permissions scope (needs to open/update PRs and push tags), and failure mode. Keeping them separate avoids conflating "is this PR mergeable" with "should a release PR be updated."

## Risks / Trade-offs

- **[Risk] Honor-system changelog entries can be forgotten** → Mitigation: none automated in this change by design (see Non-Goals); if this proves to be a recurring problem, a follow-up change can add a quality-gate check once a reliable exempt/non-exempt classifier exists.
- **[Risk] Release PR can go stale or accumulate many entries if nobody merges it** → Mitigation: this is an accepted trade-off of the Release PR pattern; a stale release PR is a visible, easy-to-notice signal (unlike a silent missed changelog entry), and it can always be merged whenever convenient.
- **[Risk] Two-way MINOR/PATCH granularity pre-1.0 may feel too coarse** → Mitigation: intentional, matches strict SemVer; the escape hatch is cutting `1.0.0`, not special-casing this repo's interpretation of the spec.
- **[Trade-off] `frontend/package.json`/`backend/pyproject.toml` version fields will visibly disagree with `VERSION` over time** → Accepted: those fields are already unconsumed dead weight (see Context); revisit only if either package is ever actually published.

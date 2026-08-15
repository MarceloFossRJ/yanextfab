## Why

The repo has no changelog and no versioning discipline: `frontend/package.json` and `backend/pyproject.toml` are both frozen at a placeholder `0.1.0`, there's no `CHANGELOG.md` anywhere, and no process ties a completed change to a recorded, classified entry. As the codebase grows past its bootstrap phase, there's no way to answer "what changed since last week" or "was that a breaking change" without reading git history line by line. This change establishes a lightweight, repo-wide convention — reusing OpenSpec's own ADDED/MODIFIED/REMOVED vocabulary — for recording and versioning changes, backed by CI automation that computes the version bump instead of requiring anyone to do SemVer arithmetic by hand.

## What Changes

- Add a new root `AGENTS.md` (the repo currently has none at root, only `frontend/AGENTS.md`) with a "Changelog & Versioning" section instructing any agent/human finishing a qualifying change to add an entry to `CHANGELOG.md`.
- Add a root `CHANGELOG.md` with a `## Unreleased` section, using `### ADDED` / `### MODIFIED` / `### REMOVED` subsections (OpenSpec's own vocabulary, not Keep a Changelog's `Added`/`Changed`/`Removed`). Breaking `MODIFIED` entries are marked `**BREAKING**`, reusing the bold-tag convention already used once in `openspec/changes/bootstrap-yanextfab/proposal.md`.
- Refactors, test-only changes, and CI-config-only changes are explicitly exempt from requiring an entry — enforcement is honor-system (no CI gate blocks a PR that skips it).
- Add a root `VERSION` file (plain text) as the single source of truth for one **unified** monorepo version number. `frontend/package.json` and `backend/pyproject.toml` version fields are explicitly left frozen and untouched — confirmed today they're unconsumed (`frontend/package.json` has `"private": true`, no publish step reads either field, no versioned API routes exist).
- Adopt strict pre-1.0 SemVer semantics (`0.y.z`): `ADDED`, `REMOVED`, and `BREAKING`-marked `MODIFIED` entries all bump **MINOR**; only non-breaking `MODIFIED` entries bump **PATCH**. No MAJOR bumps until a deliberate `1.0.0` cut.
- Add a custom script under `scripts/` (alongside the existing `scripts/check-api-client-drift.sh`) that parses `CHANGELOG.md`'s `## Unreleased` section, classifies entries, computes the version bump per the rules above, and rewrites `VERSION` and `CHANGELOG.md`.
- Add a new GitHub Actions workflow (separate from the existing `.github/workflows/ci.yml`, which is untouched) that runs on push to `main`: if `## Unreleased` has entries, it opens or updates a standing "Release: vX.Y.Z" pull request containing the computed bump and reorganized changelog. A human merges that PR to finalize — this is a Release-PR pattern (changesets-style), not a direct bot commit to `main`, since it doesn't require bypassing branch protection and avoids race conditions between concurrently merging PRs.
- On merge of the Release PR, a workflow step creates a git tag (e.g. `v0.2.0`). No GitHub Release object is created — out of scope, no audience consumes Releases yet.
- Explicitly out of scope: any CI check that blocks PRs missing a changelog entry (deferred — reliably auto-classifying "exempt" vs "non-exempt" changes is a harder problem than the version arithmetic itself); a "Git Discipline" / Conventional Commits section in `AGENTS.md` (separate, later change); syncing `frontend/package.json`/`backend/pyproject.toml` version fields to `VERSION`; adopting an off-the-shelf tool like `release-please`/`semantic-release`/`changesets` (those are commit-message-driven or npm-workspace-driven and don't fit this repo's file-based vocabulary or its two-runtime shape); binding this mechanism to OpenSpec's own delta-spec files (only one OpenSpec change has ever existed in this repo, and not every change goes through an OpenSpec proposal).

## Capabilities

### New Capabilities
- `release-versioning`: defines the changelog entry format and classification rules, the `VERSION` file as the unified version source of truth, the pre-1.0 SemVer bump rules, and the CI Release-PR automation (compute bump, open/update Release PR, tag on merge).

### Modified Capabilities
<!-- none: quality-gates' existing CI enforcement requirements are unchanged (enforcement of changelog entries stays honor-system, deliberately not added to quality-gates in this change) -->

## Impact

- **New files**: root `AGENTS.md`, root `CHANGELOG.md`, root `VERSION`, `scripts/<release-script>`, a new `.github/workflows/*.yml`.
- **Unchanged**: `.github/workflows/ci.yml`, `frontend/package.json` version field, `backend/pyproject.toml` version field, `openspec/changes/bootstrap-yanextfab/specs/quality-gates/spec.md`.
- **Process impact**: every future qualifying change (in this repo, by any contributor or agent) is expected to add a `CHANGELOG.md` entry as part of finishing the change, per the new root `AGENTS.md` instruction.

## Purpose

Defines how changes to this repo are recorded in a changelog and reflected in a single, unified SemVer version number, and how that version is advanced automatically via a CI-driven release process.

## ADDED Requirements

### Requirement: Changelog Entry Classification
Any non-exempt change SHALL be recorded as an entry under the `## Unreleased` section of the root `CHANGELOG.md`, classified under one of `### ADDED`, `### MODIFIED`, or `### REMOVED`. A `### MODIFIED` entry that breaks existing behavior SHALL be marked with a `**BREAKING**` tag.

#### Scenario: New capability recorded
- **WHEN** a change adds new user-facing or system-facing capability
- **THEN** an entry describing it is added under `## Unreleased` / `### ADDED`

#### Scenario: Breaking change marked
- **WHEN** a change modifies existing behavior in a way that breaks prior callers or consumers
- **THEN** the entry is added under `## Unreleased` / `### MODIFIED` and tagged `**BREAKING**`

### Requirement: Changelog Entry Exemption
Refactors, test-only changes, and CI-config-only changes SHALL NOT require a `CHANGELOG.md` entry.

#### Scenario: Exempt change has no entry
- **WHEN** a change only refactors internal code, adds/modifies tests, or edits CI configuration without altering observable behavior
- **THEN** the change is not required to add an entry to `CHANGELOG.md`

### Requirement: Unified Version Source of Truth
The repo SHALL maintain exactly one version number for the whole monorepo, stored in a root `VERSION` file, covering both the frontend and backend packages together. The `version` fields in `frontend/package.json` and `backend/pyproject.toml` SHALL NOT be updated by this process.

#### Scenario: Current version is read from VERSION
- **WHEN** any process needs the repo's current version
- **THEN** it reads the single value in the root `VERSION` file

### Requirement: Pre-1.0 SemVer Bump Rule
While the version's major component is `0`, the next version SHALL be computed as follows: if `## Unreleased` contains any `### ADDED` entry, any `### REMOVED` entry, or any `**BREAKING**`-tagged `### MODIFIED` entry, the version SHALL bump MINOR; otherwise, if `## Unreleased` contains only non-breaking `### MODIFIED` entries, the version SHALL bump PATCH. The MAJOR component SHALL NOT be bumped while it is `0`.

#### Scenario: Added capability bumps MINOR
- **WHEN** `## Unreleased` contains at least one `### ADDED` entry and the current version is `0.x.y`
- **THEN** the computed next version is `0.(x+1).0`

#### Scenario: Removal bumps MINOR
- **WHEN** `## Unreleased` contains at least one `### REMOVED` entry and no higher-precedence entries change the outcome, and the current version is `0.x.y`
- **THEN** the computed next version is `0.(x+1).0`

#### Scenario: Breaking modification bumps MINOR, not MAJOR
- **WHEN** `## Unreleased` contains a `**BREAKING**`-tagged `### MODIFIED` entry and the current version is `0.x.y`
- **THEN** the computed next version is `0.(x+1).0`, and the MAJOR component remains `0`

#### Scenario: Non-breaking modification bumps PATCH
- **WHEN** `## Unreleased` contains only non-breaking `### MODIFIED` entries and the current version is `0.x.y`
- **THEN** the computed next version is `0.x.(y+1)`

### Requirement: Release Pull Request Automation
On a push to `main` where `## Unreleased` contains at least one entry, CI SHALL open or update a standing release pull request that contains the computed next version and a reorganized `CHANGELOG.md` in which the `## Unreleased` entries are moved under a new `## [<version>] - <date>` heading, leaving `## Unreleased` empty. The release pull request SHALL NOT be merged automatically; a human merges it to finalize the release.

#### Scenario: Release PR created on first qualifying merge
- **WHEN** a merge to `main` adds the first `## Unreleased` entry since the last release
- **THEN** CI opens a release pull request proposing the computed version bump and reorganized changelog

#### Scenario: Release PR updated on subsequent qualifying merges
- **WHEN** a merge to `main` adds another `## Unreleased` entry while a release pull request is already open
- **THEN** CI updates that same release pull request's computed version and changelog content to reflect the new entry

### Requirement: Git Tag on Release
Merging the release pull request into `main` SHALL create a git tag matching the new version (e.g. `v0.2.0`).

#### Scenario: Tag created on release merge
- **WHEN** the release pull request is merged into `main`
- **THEN** a git tag matching the new `VERSION` value is created pointing at that merge commit

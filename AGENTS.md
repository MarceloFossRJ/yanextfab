# AGENTS.md

Repo-wide guidance for any agent or contributor working in this repository.

## Changelog & Versioning

This repo keeps one unified `CHANGELOG.md` and one unified version number
(in the root `VERSION` file) covering both `frontend` and `backend` together.
`frontend/package.json` and `backend/pyproject.toml` also carry a `version`
field each, but those are not touched by this process — nothing consumes
them today (see `openspec/changes/add-changelog-semver-versioning/design.md`
for why).

**When finishing a change that alters observable behavior**, add an entry
under `## Unreleased` in `CHANGELOG.md`, classified under one of:

- `### ADDED` — new capability.
- `### MODIFIED` — changed existing behavior. If it breaks prior callers or
  consumers, tag the entry `**BREAKING**`.
- `### REMOVED` — capability taken away.

This mirrors the vocabulary already used for OpenSpec spec deltas — use the
same three-way judgment call you'd use writing a delta spec, just applied to
a changelog line instead of a requirement block.

**Exempt — no entry required:** refactors, test-only changes, and
CI-config-only changes that don't alter observable behavior. This is
honor-system: nothing in CI blocks a PR that skips an entry it should have
had.

**Do not compute the version bump yourself.** A CI-driven Release PR
(`.github/workflows/release.yml`, via `scripts/compute-release.py`) reads
`## Unreleased` on every push to `main` and proposes the next version
automatically, following strict pre-1.0 SemVer rules: `ADDED`, `REMOVED`, and
`**BREAKING**`-tagged `MODIFIED` entries bump MINOR; non-breaking `MODIFIED`
entries alone bump PATCH; MAJOR stays `0` until a deliberate `1.0.0` cut.
Merging that Release PR finalizes the version and tags the commit.

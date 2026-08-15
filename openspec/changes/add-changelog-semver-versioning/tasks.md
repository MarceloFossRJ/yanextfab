## 1. Foundation files

- [x] 1.1 Create root `VERSION` file containing `0.1.0` as the initial unified version.
- [x] 1.2 Create root `CHANGELOG.md` with a `## Unreleased` section (empty `### ADDED` / `### MODIFIED` / `### REMOVED` subsections or a short usage comment) and no prior version history (first real entry will be `0.1.0`'s own eventual release).
- [x] 1.3 Create root `AGENTS.md` with a "Changelog & Versioning" section documenting: the classification rule (ADDED/MODIFIED/REMOVED, `**BREAKING**` tag), the exemption list (refactors, test-only, CI-config-only), that `VERSION` is the single unified source of truth, and that `frontend/package.json`/`backend/pyproject.toml` version fields are not touched by this process.

## 2. Release computation script

- [x] 2.1 Add `scripts/compute-release.<ext>` that parses `CHANGELOG.md`'s `## Unreleased` section and detects presence of `### ADDED`, `### REMOVED`, and `**BREAKING**`-tagged `### MODIFIED` entries.
- [x] 2.2 Implement the pre-1.0 bump rule: MINOR if any ADDED/REMOVED/BREAKING-MODIFIED entry is present, otherwise PATCH if only non-breaking MODIFIED entries are present; no-op (exit without proposing a release) if `## Unreleased` is empty.
- [x] 2.3 Implement the rewrite: bump `VERSION`, and reorganize `CHANGELOG.md` by moving the current `## Unreleased` entries under a new `## [<version>] - <date>` heading, leaving `## Unreleased` empty again.
- [x] 2.4 Add a way to run the script locally/in CI in "dry run" mode (print the computed next version and diff without writing files), for use in step 3's PR-update logic and for manual sanity checks.

## 3. Release PR automation (CI)

- [x] 3.1 Add a new GitHub Actions workflow (e.g. `.github/workflows/release.yml`), triggered on `push` to `main`, that does not modify `ci.yml`.
- [x] 3.2 In the workflow, run the script from Task 2 in dry-run mode against `CHANGELOG.md` on `main`; if `## Unreleased` is empty, the job exits without further action.
- [x] 3.3 If `## Unreleased` has entries, have the workflow run the script for real (writing `VERSION` and reorganizing `CHANGELOG.md`) on a dedicated release branch (e.g. `release/next`), and open a pull request from that branch into `main` titled `Release: v<version>` if one doesn't already exist for the current pending release.
- [x] 3.4 If a release PR already exists and is still open, update its branch with the newly recomputed `VERSION`/`CHANGELOG.md` content instead of opening a second PR.
- [x] 3.5 Grant the workflow only the GitHub Actions permissions it needs (`contents: write`, `pull-requests: write`) and scope it to run only on the repo's own `main` branch pushes (not forks/external PRs).

## 4. Tag on release merge

- [x] 4.1 Extend the workflow (or add a second job triggered on the same `push` event, gated on detecting a merged release PR) to create and push a git tag matching the new `VERSION` value once the release PR is merged into `main`.
- [x] 4.2 Confirm no GitHub Release object is created as part of this — tagging only.

## 5. Verification

- [x] 5.1 Manually add a sample `### ADDED` entry under `## Unreleased`, run the script locally in dry-run mode, and confirm it proposes a MINOR bump from `0.1.0` to `0.2.0`. (Verified in a sandbox copy: `--check` and `--write` both produced `0.1.0 -> 0.2.0 (minor)`, and the changelog rewrite moved the entry under `## [0.2.0] - 2026-08-15` correctly.)
- [x] 5.2 Manually add a sample non-breaking `### MODIFIED` entry (no other entries present), run the script locally in dry-run mode, and confirm it proposes a PATCH bump from `0.1.0` to `0.1.1`. (Verified: `--check` produced `0.1.0 -> 0.1.1 (patch)`.)
- [x] 5.3 Manually add a `**BREAKING**`-tagged `### MODIFIED` entry alongside a plain `### ADDED` entry, and confirm the script still proposes MINOR (not MAJOR) given the current `0.y.z` version. (Verified: `--check` produced `0.1.0 -> 0.2.0 (minor)`, confirming the collapse rule. Also spot-checked the empty-`Unreleased` no-op path: `--check` exits 1 with no pending release.)
- [ ] 5.4 Push a test commit with an `## Unreleased` entry to a throwaway branch merged into `main` (or exercise the workflow via `workflow_dispatch`/a fork) and confirm the release PR opens with the expected `VERSION` and `CHANGELOG.md` diff. **Not run** — this requires pushing to the real GitHub remote (branches/PRs/workflow runs on the actual repo), which wasn't authorized as part of this session. Do this once the change is committed and pushed.
- [x] 5.5 Confirm `frontend/package.json` and `backend/pyproject.toml` are untouched by the whole flow, and that `ci.yml` still runs unmodified on the release PR itself (it's a normal PR to `main`). (Verified via `git diff --stat` on those three files: no changes.)

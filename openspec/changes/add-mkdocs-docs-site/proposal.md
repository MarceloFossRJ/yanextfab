## Why

The repo's only documentation is the root `README.md` — 323 lines mixing a project pitch, prerequisites, template-setup steps, a full getting-started walkthrough, troubleshooting, tech stack notes, testing, deployment, and API client codegen into a single scrolling page. That's already hard to navigate for the repo's own primary audience (the user, re-running "Use this template" for future projects) and for outside GitHub users evaluating the template, and it won't get easier as more sections get added. There's no search, no real navigation, and no separation between "read this once to get started" and "reference material to come back to."

## What Changes

- Add a `docs/` folder of Markdown pages built with mkdocs + the Material for MkDocs theme, covering: Getting Started (prerequisites + template setup + quickstart), Tech Stack, Testing, Deployment, API Client Codegen, Configuration, and Troubleshooting — mirroring the current README's sections minus the parts that stay in the README.
- Add a new root-level `pyproject.toml` + `uv.lock` dedicated to docs tooling (mkdocs, mkdocs-material), separate from `backend/pyproject.toml`, since the docs describe both `frontend/` and `backend/`, not just the backend.
- Add `mkdocs.yml` at the repo root configuring the Material theme, nav structure, and site metadata.
- Add a new, independent GitHub Actions workflow (`.github/workflows/docs.yml`) that builds the docs site and deploys it to GitHub Pages on every push to `main`. It does not read or modify `release.yml`'s version-bump/tagging logic, and runs as its own job alongside (not gated by) `ci.yml`.
- Trim `README.md` down to: project pitch, prerequisites, "Use this template" steps, and a quickstart — with a link to the published docs site for everything else. **BREAKING** for anyone currently deep-linking to a specific README section/anchor that moves to the docs site.
- Remove the untouched `create-next-app` boilerplate content from `frontend/README.md` and the empty `backend/README.md` (neither carries real custom content today) rather than migrating it.
- Explicitly out of scope: docs versioning/multi-version support (no `mike` plugin, no version switcher — the site tracks `main` as "latest" only), folding `AGENTS.md` or `openspec/` content into the docs site (different audience: agents/contributors, not template users), and any change to `release.yml`'s existing CHANGELOG/SemVer release-PR process.

## Capabilities

### New Capabilities
- `project-documentation`: defines the docs site's structure (pages, nav), tooling (mkdocs + Material, its own root-level `uv` environment), hosting (GitHub Pages, deployed on every push to `main`), versioning stance (unversioned, tracks `main`), and README's reduced scope as the entry point into it.

### Modified Capabilities
<!-- none: this change doesn't alter any existing capability's requirements. quality-gates (CI enforcement) is untouched — the new docs workflow is independent of ci.yml and release.yml. -->

## Impact

- **New files**: `docs/**/*.md`, `mkdocs.yml`, root `pyproject.toml` + `uv.lock` (docs-only), `.github/workflows/docs.yml`.
- **Modified files**: `README.md` (trimmed), `frontend/README.md` and `backend/README.md` (stripped of stale boilerplate).
- **Unchanged**: `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `backend/pyproject.toml`, `frontend/package.json`, `AGENTS.md`, `openspec/`.
- **One-time manual step** (not automatable from this change): enabling GitHub Pages in the repo's Settings (source: GitHub Actions) so the new workflow's deploy step has somewhere to publish to.

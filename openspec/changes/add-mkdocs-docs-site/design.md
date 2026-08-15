## Context

See `proposal.md` - Why for motivation. Current state: the repo's only documentation is the root `README.md`; there is no `docs/` folder, no `mkdocs.yml`, and no GitHub Pages workflow. `.github/workflows/` has exactly `ci.yml` and `release.yml`. The backend is Python, managed with `uv` via `backend/pyproject.toml`/`backend/uv.lock`; the frontend is Next.js, managed with `pnpm`. `release.yml` drives an existing CHANGELOG + pre-1.0 SemVer release-PR process (see `openspec/changes/add-changelog-semver-versioning/`) that this change must not touch.

## Goals / Non-Goals

**Goals:**
- Publish a searchable, navigable documentation site sourced from Markdown in `docs/`, deployed to GitHub Pages on every push to `main`.
- Keep docs tooling isolated in its own root-level `uv` environment, independent of the backend's.
- Trim `README.md` down to entry-point content only, with the docs site as the single source of truth for everything else.

**Non-Goals:**
- Docs versioning (no `mike` plugin, no version switcher) — the site always tracks `main`.
- Any change to `release.yml`'s version-bump/tagging behavior or cadence.
- Folding `AGENTS.md` or `openspec/` content into the site (different audience).
- Fixing "keep README and docs in sync going forward" as a process — this change achieves it structurally (one source of truth per topic) but doesn't add tooling to enforce it long-term.

## Decisions

**1. mkdocs + Material for MkDocs, over Docusaurus / VitePress / a plain `docs/` folder with no generator.**
Weighed explicitly against the alternatives: Docusaurus (React) fits the frontend's JS stack but adds a second, heavier JS toolchain; VitePress (Vue) is light but is an odd tooling fit for a Next.js+FastAPI project; a plain unbuilt `docs/` folder is the objectively lightest option (GitHub renders Markdown natively, zero pipeline) but gives up search/nav polish and the deliberate learning goal behind this choice. mkdocs is Python-native, sits naturally next to the backend's `uv` toolchain conceptually, has a low-friction GitHub Pages deploy story, and Material adds search/nav/dark-mode with modest config. Chosen deliberately for the Python-ecosystem fit and hands-on value, not because it's the minimal-footprint option.

**2. Docs tooling gets its own root-level `pyproject.toml` + `uv.lock`, not `backend/pyproject.toml`.**
Alternatives considered: (a) add mkdocs/mkdocs-material as an optional dependency group inside `backend/pyproject.toml` — rejected, since the docs describe both `frontend/` and `backend/`, and bundling the dependency there would misrepresent scope and couple docs builds to backend dependency changes; (b) run mkdocs ad hoc via `uvx` with nothing pinned in the repo — rejected, since it risks silent version drift between a contributor's machine and CI, and CI needs a reproducible lockfile to build from deterministically.

**3. No docs versioning.**
This is a fork-and-diverge template, not a library consumers pin an exact version of for API compatibility — every user immediately owns their own copy and diverges from `main`. A version switcher would be pure overhead with no one to serve it to.

**4. Deploy workflow is independent of `release.yml`, triggered on every push to `main`.**
Alternative considered: gate docs deploys on the release-PR merge (i.e., only redeploy when `VERSION` bumps) — rejected, since "latest tracks `main`" (Decision 3) implies the docs should reflect `main` continuously, and coupling to the release cadence would leave the published site stale between releases for no benefit. Keeping the workflow independent also means it can't interact with or break `release.yml`'s tagging logic.

**5. GitHub Pages via the native Actions deployment flow (`actions/configure-pages` + `actions/deploy-pages`), not the classic `mkdocs gh-deploy` branch-push approach.**
No `gh-pages` branch to keep in sync with `main`, and it's GitHub's currently recommended approach. Trade-off: requires a one-time manual repo Settings change (Pages → Source: GitHub Actions) that cannot be automated from within this change — called out explicitly in `tasks.md`.

**6. Docs page structure mirrors the current README's sections 1:1** (Getting Started, Tech Stack, Testing, Deployment, API Client Codegen, Configuration, Troubleshooting), rather than a reorganized information architecture. Minimizes content-mapping risk during migration — every existing paragraph has an obvious destination page — and can be reorganized later once the site exists, which is a much lower-risk change than the initial migration.

**7. Stale sub-package READMEs are stripped, not migrated.** `frontend/README.md` is untouched `create-next-app` boilerplate and `backend/README.md` is empty; neither has custom content worth carrying forward, so treating them as "content to migrate" would just add migration noise.

## Risks / Trade-offs

- [Repo now has two independent Python environments (backend's, docs') that could be confused for one another] → Mitigation: keep the docs `pyproject.toml` minimal (mkdocs + mkdocs-material only), and not wired into any backend workspace/lockfile.
- [GitHub Pages requires a manual, one-time repo Settings change that this change can't perform itself] → Mitigation: called out as an explicit manual task in `tasks.md`; the deploy workflow will fail visibly (not silently) until Pages is enabled, rather than degrading quietly.
- [Manually moving README content into `docs/` pages risks losing or misplacing content] → Mitigation: page structure mirrors existing README headings 1:1 (Decision 6), and `tasks.md` checks off each README section as it's relocated.
- [Two sources of truth could reappear over time if someone edits README instead of docs/, or vice versa] → Mitigation: this change makes README's scope narrow enough (pitch + prerequisites + template steps + quickstart) that there's little temptation to add reference content there instead of to `docs/`.

## Migration Plan

This is a content/tooling migration, not a data migration. Order: scaffold `docs/` + `mkdocs.yml` + root `pyproject.toml`/`uv.lock` → move README content section-by-section into the corresponding docs page → trim `README.md` to its new scope → add `.github/workflows/docs.yml` → manually enable GitHub Pages (Settings → Pages → Source: GitHub Actions) → verify the first deploy renders correctly → strip stale `frontend/README.md`/`backend/README.md` boilerplate.

Rollback: a plain `git revert` of the change's commit(s) — no runtime state or data is involved. The published GitHub Pages site would simply stop receiving new deploys; it can optionally be disabled manually in repo Settings if needed.

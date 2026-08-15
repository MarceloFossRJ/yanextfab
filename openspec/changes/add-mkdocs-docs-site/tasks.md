## 1. Docs Tooling Scaffold

- [x] 1.1 Add a new root-level `pyproject.toml` for docs tooling (`mkdocs`, `mkdocs-material`), kept separate from `backend/pyproject.toml`
- [x] 1.2 Generate the corresponding root-level `uv.lock`
- [x] 1.3 Add `mkdocs.yml` at the repo root: Material theme, site name/description, search enabled

## 2. Docs Site Structure & Content Migration

- [x] 2.1 Create the `docs/` folder with page files: `getting-started.md`, `project-structure.md`, `adding-features.md`, `testing.md`, `tech-stack.md`, `configuration.md`, `deployment.md`, `api-client-codegen.md`, `troubleshooting.md` (plus `index.md` as the site's required landing page, not separately enumerated in the original task list)
- [x] 2.2 Move "Prerequisites", "Creating your own project from this template", "Getting started", "Try it out", and "Other commands" content from `README.md` into `docs/getting-started.md`
- [x] 2.3 Move "What's in the box" content from `README.md` into `docs/project-structure.md`
- [x] 2.4 Move "Adding your own features" content from `README.md` into `docs/adding-features.md`
- [x] 2.5 Move "Testing" and "Enable pre-commit hooks" content from `README.md` into `docs/testing.md`
- [x] 2.6 Move "Tech stack, briefly" content from `README.md` into `docs/tech-stack.md`
- [x] 2.7 Move "Configuration" content from `README.md` into `docs/configuration.md`
- [x] 2.8 Move "Deployment" content from `README.md` into `docs/deployment.md`
- [x] 2.9 Move "API client codegen" content from `README.md` into `docs/api-client-codegen.md`
- [x] 2.10 Move "Troubleshooting" content from `README.md` into `docs/troubleshooting.md`
- [x] 2.11 Set `mkdocs.yml`'s `nav` to match the page order above
- [x] 2.12 Run `mkdocs build --strict` locally and confirm it succeeds with no broken links or warnings

## 3. README Trim

- [x] 3.1 Rewrite root `README.md` to contain only: project pitch, prerequisites, "Use this template" steps, and a quickstart
- [x] 3.2 Add a prominent link from `README.md` to the published documentation site for everything else
- [x] 3.3 Spot-check that every section removed from `README.md` has a corresponding home in `docs/` — nothing silently dropped

## 4. CI Deploy Workflow

- [x] 4.1 Add `.github/workflows/docs.yml` that builds the docs site with the root-level `uv` environment on push to `main`
- [x] 4.2 Deploy the built site to GitHub Pages using `actions/configure-pages` + `actions/upload-pages-artifact` + `actions/deploy-pages`
- [x] 4.3 Confirm the new workflow is independent of, and makes no changes to, `ci.yml` or `release.yml`

## 5. Housekeeping & Verification

- [x] 5.1 Strip `frontend/README.md` of its untouched `create-next-app` boilerplate; replace with a short pointer to the docs site
- [x] 5.2 Replace the empty `backend/README.md` with a short pointer to the docs site, consistent with 5.1
- [ ] 5.3 Manually enable GitHub Pages in repo Settings → Pages → Source: GitHub Actions (cannot be automated from within this change)
- [ ] 5.4 Push to `main` (or merge this change) and confirm `docs.yml` runs and the site deploys successfully
- [ ] 5.5 Browse the deployed site and confirm search, navigation, and every migrated page render correctly
- [x] 5.6 Add a `CHANGELOG.md` entry under `## Unreleased` per `AGENTS.md` (README's public content/location changes are externally observable)

## Why

New projects created from this template must manually hunt down and replace every hardcoded "Yanextfab" occurrence across ~15 files (branding text, DB/SMTP placeholders, a CI release gate), and the current docs checklist for this is already incomplete — it omits `docker-compose.yml`, both GitHub Actions workflows, `mkdocs.yml`, and several config defaults. Separately, the docs' step 1 assumes the "Use this template" button is already visible, but the repo currently has GitHub's "Template repository" setting off (`isTemplate: false`), so the button doesn't exist yet — the instructions never say to enable it.

## What Changes

- Add `scripts/init.py`: an interactive setup script that prompts for project display name, short description, and author name; auto-derives slug/casing variants, the GitHub owner/repo (via `git remote get-url origin`), and the copyright year; shows a summary and asks for one y/n confirmation; then rewrites every hardcoded template-name and placeholder-credential occurrence across the repo (see spec for the full file list).
- Add a `make init` Makefile target that runs the script, matching the existing `make <verb>` workflow convention.
- The script self-deletes (removes itself and the `make init` target) after a successful run, so a renamed project doesn't carry template-bootstrap tooling forward.
- Rewrite `docs/getting-started.md`'s "Creating Your Own Project From This Template" section: step 1 gains a note that the repo owner must enable Settings → General → Template repository before the button appears; step 2's manual checklist is replaced with instructions to run `make init`.

## Capabilities

### New Capabilities
- `template-init`: the interactive script that turns a freshly cloned copy of this template into a new, correctly-named project (prompts, derived values, confirmation, file rewrites, self-cleanup).

### Modified Capabilities
(none — no existing specs in this repo yet)

## Impact

- New file: `scripts/init.py`.
- Modified: `Makefile` (new `init` target, later removed by the script itself post-run).
- Modified: `docs/getting-started.md` (rewritten template-setup instructions).
- Rewritten at runtime by the script (not by this change itself): `LICENSE`, `README.md`, `frontend/README.md`, `backend/README.md`, `mkdocs.yml`, root `pyproject.toml`, `backend/pyproject.toml` (description only), `frontend/src/app/layout.tsx`, `frontend/src/app/register/page.tsx`, `frontend/src/components/dashboard/app-sidebar.tsx`, `backend/src/app/main.py`, `backend/src/app/core/mail.py`, `docker-compose.yml`, `backend/.env.example`, `backend/src/app/core/config.py`, `backend/tests/conftest.py`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`.
- Explicitly untouched by the script: `.github/CODEOWNERS`, `docs/index.md`/`tech-stack.md`/`testing.md` prose, `openspec/` directory, `frontend/package.json` `name` field, `backend/pyproject.toml` `name` field.
- No production runtime impact — this only affects the one-time template-to-project bootstrap flow.

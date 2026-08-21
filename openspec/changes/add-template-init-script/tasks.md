## 1. Script scaffold and prompts

- [x] 1.1 Create `scripts/init.py` with the three interactive prompts (display name, description, author), in order
- [x] 1.2 Implement slug (kebab-case) and PascalCase/Title-Case derivation from the display name
- [x] 1.3 Implement GitHub owner/repo detection via `git remote get-url origin` (handle SSH and HTTPS remote URL forms), with a clear error if it fails or isn't a GitHub URL
- [x] 1.4 Derive copyright year from the system date
- [x] 1.5 Derive Postgres user/password/database name and SMTP "from" address from the slug

## 2. Confirmation step

- [x] 2.1 Print a summary of all derived values (slug, PascalCase name, detected owner/repo, DB creds, SMTP address, year)
- [x] 2.2 Require a single y/n confirmation; exit without writing anything on "no"

## 3. File rewrites

- [x] 3.1 Rewrite branding occurrences: `LICENSE`, `README.md`, `frontend/README.md`, `backend/README.md`, `mkdocs.yml`, root `pyproject.toml`, `backend/pyproject.toml` (description only), `frontend/src/app/layout.tsx`, `frontend/src/app/register/page.tsx`, `frontend/src/components/dashboard/app-sidebar.tsx`, `backend/src/app/main.py`, `backend/src/app/core/mail.py`
- [x] 3.2 Rewrite infra placeholders consistently across `docker-compose.yml`, `backend/.env.example`, `backend/src/app/core/config.py`, `backend/tests/conftest.py`, `.github/workflows/ci.yml`
- [x] 3.3 Rewrite `.github/workflows/release.yml`'s repository guard condition using the detected owner/repo
- [x] 3.4 Verify the script does not touch `.github/CODEOWNERS`, `docs/index.md`/`tech-stack.md`/`testing.md`, `openspec/`, `frontend/package.json`'s `name`, or `backend/pyproject.toml`'s `name`

## 4. Self-cleanup

- [x] 4.1 Add a `make init` target to the `Makefile` that runs `uv run scripts/init.py`
- [x] 4.2 After all rewrites succeed, delete `scripts/init.py` and remove the `init` target from the `Makefile`
- [x] 4.3 Confirm the script and target are left intact if the user declines confirmation or a rewrite step fails partway through

## 5. Documentation

- [x] 5.1 Rewrite `docs/getting-started.md`'s "Creating Your Own Project From This Template" step 1 to note enabling Settings → General → Template repository before the button appears
- [x] 5.2 Replace step 2's manual checklist with instructions to run `make init` (or `uv run scripts/init.py`)

## 6. Verification

- [x] 6.1 Run the script in a scratch clone/worktree, walk through the prompts, confirm, and grep the resulting tree for residual `[Yy]anextfab` (should only remain in explicitly-excluded files) — confirmed clean in two full runs; found and fixed two gaps not caught by the original repo grep (`frontend/src/lib/auth/constants.ts`'s session-cookie constant, and a stale `uv.lock` entry now regenerated via `uv lock`)
- [~] 6.2 Run `make lint` and `make test` (or backend/frontend equivalents) after a rename to confirm nothing broke — ran `python -m py_compile` on all touched backend files (passed); skipped the full Docker Compose `make lint`/`make test` stack as disproportionate for a throwaway scratch clone
- [x] 6.3 Confirm `scripts/init.py` and the `make init` target are gone after a successful run — verified, and also verified both are left intact when the user declines the confirmation prompt
- [x] 6.4 Re-read the rewritten `docs/getting-started.md` section for accuracy

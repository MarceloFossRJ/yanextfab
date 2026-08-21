## Purpose

Turns a freshly cloned copy of this template repo into a correctly-named, self-consistent project by replacing every hardcoded template-branding string and placeholder credential in one interactive run, then removing itself.

## ADDED Requirements

### Requirement: Interactive project details prompt
The script SHALL prompt the user interactively for exactly three values: project display name, short description, and author name. The script SHALL NOT accept these values via command-line flags or non-interactive input.

#### Scenario: Running the script
- **WHEN** the user runs `make init` or `uv run scripts/init.py` in a freshly cloned copy of the template
- **THEN** the script prompts for project display name, then short description, then author name, in that order

### Requirement: Derived values computed without prompting
From the display name, the script SHALL derive a slug (lowercase, hyphenated) and a PascalCase/Title-Case variant without prompting the user separately for either. The script SHALL detect the GitHub owner and repository name from `git remote get-url origin` and SHALL determine the copyright year from the system date, without prompting for either.

#### Scenario: Deriving casing variants
- **WHEN** the user enters a display name such as "Acme Corp"
- **THEN** the script derives a slug such as `acme-corp` and a PascalCase/Title-Case form such as "Acme Corp" for use across renamed files, without asking a follow-up question

#### Scenario: Detecting the GitHub remote
- **WHEN** the script runs inside a git working tree whose `origin` remote points at `github.com/<owner>/<repo>`
- **THEN** the script uses that owner and repo name for every file that hardcodes `MarceloFossRJ/yanextfab`, without prompting the user for them

### Requirement: Confirmation before writing
Before making any file changes, the script SHALL print a summary of all derived values (slug, PascalCase name, detected GitHub owner/repo, derived database credentials, derived SMTP address, copyright year) and SHALL require a single yes/no confirmation. If the user declines, the script SHALL exit without modifying any file.

#### Scenario: User confirms
- **WHEN** the script has printed the derived-values summary and the user answers yes
- **THEN** the script proceeds to rewrite files

#### Scenario: User declines
- **WHEN** the script has printed the derived-values summary and the user answers no
- **THEN** the script exits immediately and no file in the repository is modified

### Requirement: Template-branding rewrite
On confirmation, the script SHALL replace every hardcoded "Yanextfab"/"yanextfab" occurrence in: `LICENSE` (copyright holder and year), `README.md` (title and description), `frontend/README.md`, `backend/README.md`, `mkdocs.yml` (`site_name`, `repo_url`, `repo_name`), the root `pyproject.toml` (`name` and description), `backend/pyproject.toml` (description only), `frontend/src/app/layout.tsx` (metadata title), `frontend/src/app/register/page.tsx`, `frontend/src/components/dashboard/app-sidebar.tsx`, `frontend/src/lib/auth/constants.ts` (session cookie name), `backend/src/app/main.py` (FastAPI `title=`), and `backend/src/app/core/mail.py` (email subject). The script SHALL also regenerate the root `uv.lock` after editing the root `pyproject.toml`'s `name` field, so the lockfile's derived name stays consistent.

#### Scenario: Branding replaced across the repo
- **WHEN** the script completes a confirmed run with display name "Acme Corp"
- **THEN** none of the listed files contain the strings "Yanextfab" or "yanextfab" anymore, and each now reflects the derived project name

### Requirement: Infrastructure placeholder rewrite
On confirmation, the script SHALL derive Postgres user, password, and database name, and an SMTP "from" address, from the project slug, and SHALL apply these consistently across `docker-compose.yml`, `backend/.env.example`, `backend/src/app/core/config.py`, `backend/tests/conftest.py`, and `.github/workflows/ci.yml`.

#### Scenario: Consistent derived credentials
- **WHEN** the script completes a confirmed run
- **THEN** the Postgres user/password/database name and SMTP "from" address are identical across all five listed files and are derived from the same project slug

### Requirement: Release workflow gate rewrite
On confirmation, the script SHALL rewrite `.github/workflows/release.yml`'s repository guard condition to reference the GitHub owner/repo detected from the git remote, replacing the template's hardcoded `MarceloFossRJ/yanextfab` value.

#### Scenario: Release gate updated
- **WHEN** the script completes a confirmed run in a repo whose `origin` remote points at `github.com/someorg/somerepo`
- **THEN** `.github/workflows/release.yml`'s repository guard condition references `someorg/somerepo` instead of `MarceloFossRJ/yanextfab`

### Requirement: Excluded files left untouched
The script SHALL NOT modify `.github/CODEOWNERS`, the prose content of `docs/index.md`, `docs/tech-stack.md`, or `docs/testing.md`, the `openspec/` directory, the `name` field in `frontend/package.json`, or the `name` field in `backend/pyproject.toml`.

#### Scenario: Exclusions preserved
- **WHEN** the script completes a confirmed run
- **THEN** `.github/CODEOWNERS`, `docs/index.md`, `docs/tech-stack.md`, `docs/testing.md`, the `openspec/` directory, `frontend/package.json`'s `name` field, and `backend/pyproject.toml`'s `name` field are byte-for-byte unchanged

### Requirement: Self-cleanup after success
After successfully completing all file rewrites, the script SHALL delete itself (`scripts/init.py`) and SHALL remove the `init` target from the `Makefile`.

#### Scenario: Script removes itself
- **WHEN** the script finishes rewriting files successfully
- **THEN** `scripts/init.py` no longer exists and the `Makefile` no longer contains an `init` target

#### Scenario: Script does not remove itself on decline or failure
- **WHEN** the user declines the confirmation prompt, or the script fails before completing all rewrites
- **THEN** `scripts/init.py` and the `Makefile`'s `init` target still exist, so the user can re-run it

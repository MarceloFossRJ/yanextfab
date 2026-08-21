## Context

See proposal.md - Why. The repo root already has Python/uv tooling (for the mkdocs docs site), while the frontend is a separate pnpm workspace — running the setup script before any `pnpm install` has happened is a hard constraint.

## Goals / Non-Goals

**Goals:**
- Single, safe, one-shot script a new template owner runs right after cloning.
- No new runtime dependency beyond what the repo already requires (Python 3.12+, already a documented prerequisite).

**Non-Goals:**
- Non-interactive/CI invocation (flags) — see proposal; this is a manual one-time step, not something re-run in automation.
- A full dry-run diff preview — see Decisions below.
- Enabling the GitHub "Template repository" setting or touching anything on github.com — that stays a manual step for the repo owner, documented in `docs/getting-started.md`.

## Decisions

- **Language: Python**, not Node or bash. Alternatives considered: a Node script (rejected — would require `pnpm install` to succeed in `frontend/` first, and the repo root has no Node tooling of its own); a bash/sed script (rejected — cross-platform text substitution across ~18 files with multiple casing variants is fragile in bash/sed compared to Python's `pathlib`/`re`, and bash isn't guaranteed on native Windows per the docs' own Windows/WSL2 caveat). Python's stdlib covers every need here (file I/O, regex substitution, `subprocess` for `git remote`), so no new dependency is added.
- **Confirmation model: derived-values summary + single y/n, no full diff preview.** The script only ever runs on a freshly cloned, pre-first-commit working tree, so the safety net is git itself (`git checkout -- .` and re-run) rather than an in-script preview. A full diff of ~18 files would be noisy without adding real safety over that git-native rollback.
- **Casing derivation is mechanical, not a second prompt.** One display-name input drives both the slug and the PascalCase/Title-Case variant, so the two forms can never drift out of sync the way two independent prompts could.
- **Self-delete is unconditional on success, not flag-gated.** Earlier considered a `--keep` flag (see grilling session); dropped once the confirmation-prompt model was settled — the y/n gate before writing is the safety checkpoint, and self-delete only fires after every rewrite succeeds, so there's no scenario where a user is surprised by the script disappearing without having just confirmed the run.
- **Infra placeholders (DB creds, SMTP) are derived from the slug, not separately prompted.** Consistent with treating them as template boilerplate rather than real secrets — `docker-compose.yml`/`.env.example` are dev-only defaults; a real deployment configures its own `.env`, which the script does not touch (no `.env` file should exist yet in a fresh clone).
- **Scope boundary excludes `docs/*.md` prose, `openspec/`, and the two generic `name` fields** (`frontend/package.json`, `backend/pyproject.toml`) — see spec's "Excluded files" requirement. These were deliberately kept out during the grilling session because they're either fork-specific content the owner will rewrite anyway, or already-generic values the original docs already called optional.

## Risks / Trade-offs

- [Unusual display-name input (emoji, ampersands, non-ASCII) could produce a malformed slug] → Mitigation: the confirmation summary shows the derived slug before any file is written, so a bad derivation is caught before it propagates to 18 files.
- [`git remote get-url origin` fails or returns a non-GitHub URL if run before `git remote add origin` or in a non-GitHub clone] → Mitigation: this is a hard prerequisite (documented in the getting-started rewrite) — the script should fail fast with a clear error rather than silently writing a wrong owner/repo into `release.yml`.
- [Running the script a second time after self-deletion is impossible by design] → Mitigation: this is intentional (proposal's self-cleanup goal); a user who wants to re-derive names again can `git clone` the template fresh.

## Migration Plan

Not applicable — this adds new tooling and doc text; it does not change any existing runtime behavior or require migrating existing data.

# Getting Started

## Prerequisites

You have two options. Pick one — you don't need both.

**Option A — Docker only (recommended, least setup):**

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- `git`

Everything — including `make lint`, `make format`, and `make test` — runs *inside* the
containers, so Option A alone is enough for the entire day-to-day workflow described here. The
one exception is [pre-commit hooks](testing.md#enable-pre-commit-hooks-optional-recommended),
which run on your machine at `git commit` time and so need native tooling regardless.

**Option B — running the apps natively (faster iteration, more setup, needed for pre-commit
hooks):** everything in Option A, plus:

- [Node.js 24+](https://nodejs.org/) and [pnpm](https://pnpm.io/installation) (frontend)
- [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) (backend)
- A local Postgres instance, *or* just the `postgres` service from Docker Compose on its own:
  `docker compose up postgres -d` starts only that container (see `docker-compose.yml` for its
  connection details).

`make` is used throughout these docs as a shorthand, but it's optional — every `make <target>`
command is a one-liner defined in the root `Makefile`; if you don't have `make` installed, open
the `Makefile` and run the underlying command directly (e.g. `make up` is just
`docker compose up --build`).

**Windows**: use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) with Docker
Desktop's WSL2 backend. The repo's shell scripts (`docker-entrypoint.sh`,
`scripts/check-api-client-drift.sh`) and Makefile targets assume a Unix-like shell and aren't
tested on native Windows (PowerShell/cmd).

## Creating Your Own Project From This Template

1. On GitHub, click **"Use this template"** on the Yanextfab repo (or `git clone` it if you're
   not using GitHub) to get your own copy under a new name.
2. Rename the project. Nothing does this automatically — it's a handful of places where
   "Yanextfab"/"yanextfab" is hardcoded as boilerplate branding:
   - `frontend/package.json` — the `"name"` field (currently `"frontend"`, fine to leave as-is
     or rename)
   - `backend/pyproject.toml` — the `[project]` `name` field (currently `"backend"`)
   - `frontend/src/components/dashboard/app-sidebar.tsx` — the "Yanextfab" text shown in the
     dashboard sidebar
   - `frontend/src/app/layout.tsx` — the page `<title>`/description (`metadata`) shown in the
     browser tab
   - `frontend/src/app/register/page.tsx` — "Get started with Yanextfab." copy
   - `backend/src/app/main.py` — the FastAPI `title="Yanextfab API"`
   - `backend/src/app/core/mail.py` — the password-reset email subject line
   - `LICENSE` — the copyright holder name
   - The root `README.md` — the title and description
3. Continue with **Quickstart** below.

The `openspec/` directory is this template's own internal planning history (the proposal,
design doc, and task breakdown used to build Yanextfab itself) — it's not part of the running
app. Keep it if you want a written record of *why* things are built the way they are, or delete
the whole folder for your own project; nothing in `frontend/` or `backend/` depends on it.

## Quickstart

```bash
cp .env.example .env
```

Open `.env` in a text editor and fill in:

- `JWT_SECRET` — a random secret used to sign session tokens. Generate one with
  `openssl rand -hex 32` (available by default on macOS/Linux; on Windows use WSL, or generate
  one at <https://generate-secret.vercel.app/32>) and paste it in. **Don't skip this** — the
  committed default is a well-known placeholder, not a real secret.
- `ANTHROPIC_API_KEY` — *optional.* Needed only to make the AI chat example actually respond.
  Get one at <https://console.anthropic.com/> (requires an account; Anthropic's API is
  pay-as-you-go, not free, but new accounts typically get a small trial credit). If you leave
  this blank, everything else in the app still works — the chat page will show an error message
  instead of a reply, rather than crashing.

Then bring the whole stack up:

```bash
make up   # or: docker compose up --build
```

This starts four containers together: Postgres, the backend (database migrations run
automatically on startup), the frontend, and Mailpit (a fake email inbox for testing the
password-reset flow — see below). The first run downloads base images and installs
dependencies, so it can take a few minutes; subsequent runs are much faster.

**This command keeps running in your terminal** (it's streaming live logs from all four
containers) rather than returning you to the prompt — that's expected, not a hang. Leave it
running and open a *new* terminal tab/window for everything else, or add `-d` to run detached
instead (`docker compose up --build -d`) and use `make logs` whenever you want to see the live
logs.

**How to tell it worked:** once the logs settle, open <http://localhost:3000> — you should land
on a login page. That confirms the frontend is up and can reach the backend.

- App: <http://localhost:3000>
- API docs (interactive, from FastAPI): <http://localhost:8000/docs>
- Mailpit (dev email inbox): <http://localhost:8025>

### Try It Out

1. Go to <http://localhost:3000/register> and create an account with any email and an 8+
   character password — there's no email verification step, so any address works.
2. You'll land on the dashboard. Try the **Items** page (a small create/edit/delete example —
   proves the typed API path works end-to-end) and the **Chat** page (the AI agent example — it
   needs `ANTHROPIC_API_KEY` to actually reply, see above).
3. Log out — click your email at the bottom of the sidebar, then **Log out**. This takes you
   back to the login page.
4. From the login page, click **"Forgot password?"**, enter the email you registered with, then
   check <http://localhost:8025> — the reset email actually arrives there in dev, with a working
   reset link, instead of going to a real inbox.

### Other Commands

All defined in the root `Makefile`. Everything except `up`/`down`/`build` requires the stack to
already be running (`make up`) — they run *inside* the containers, not on your machine.

| Command | What it does |
| --- | --- |
| `make down` | Stop and remove the containers |
| `make logs` | Tail logs from all services (useful for debugging a container that won't start) |
| `make restart` | Restart the containers without rebuilding |
| `make migrate` | Run database migrations manually (normally automatic on `make up`) |
| `make backend-shell` / `make frontend-shell` | Open a shell inside the running backend/frontend container |
| `make lint` / `make format` | Run linters / auto-format both apps |
| `make test` | Run both test suites (backend: pytest, frontend: vitest) |

Running into trouble? See [Troubleshooting](troubleshooting.md).

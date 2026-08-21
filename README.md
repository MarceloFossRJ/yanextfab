# Yanextfab

Yet another Next.js and FastAPI boilerplate — a personal-first starter for projects that need a
TypeScript frontend, a Python backend, and heavy AI/agent tooling out of the box.

- **Frontend**: [Next.js](https://nextjs.org/) + React, [Zod](https://zod.dev/) for schema
  validation, [Shadcn/ui](https://ui.shadcn.com/) for components, [Tailwind CSS](https://tailwindcss.com/) for styling
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/) (async) for the database, [Pydantic](https://docs.pydantic.dev/) for data validation, [LangGraph](https://langchain-ai.github.io/langgraph/) for AI agents
- **Auth**: [`fastapi-users`](https://fastapi-users.github.io/fastapi-users/) on the backend, with Next.js owning the session cookie
- **AI**: an example LangGraph agent streamed over SSE, backed by Anthropic via `init_chat_model`

📖 **Full documentation:** <https://marcelofossrj.github.io/yanextfab/> — tech stack details,
testing, deployment, configuration, API client codegen, and troubleshooting all live there. This
README only covers prerequisites and the quickstart.

## Prerequisites

You have two options. Pick one — you don't need both.

**Option A — Docker only (recommended, least setup):**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- `git`

Everything — including `make lint`, `make format`, and `make test` — runs *inside* the
containers, so Option A alone is enough for the entire day-to-day workflow. The one exception is
pre-commit hooks, which run on your machine at `git commit` time and so need native tooling
regardless — see the [full docs](https://marcelofossrj.github.io/yanextfab/testing/#enable-pre-commit-hooks-optional-recommended).

**Option B — running the apps natively (faster iteration, more setup, needed for pre-commit
hooks):** everything in Option A, plus:
- [Node.js 24+](https://nodejs.org/) and [pnpm](https://pnpm.io/installation) (frontend)
- [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) (backend)
- A local Postgres instance, *or* just the `postgres` service from Docker Compose on its own:
  `docker compose up postgres -d` starts only that container (see `docker-compose.yml` for its
  connection details).

`make` is used throughout as a shorthand, but it's optional — every `make <target>` command is a
one-liner defined in the root `Makefile`; if you don't have `make` installed, open the
`Makefile` and run the underlying command directly (e.g. `make up` is just
`docker compose up --build`).

**Windows**: use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) with Docker
Desktop's WSL2 backend.

## Use this template

1. Make sure the repo has GitHub's **Template repository** setting enabled (Settings → General →
   check "Template repository") — the button below only appears once that's on. Then, on GitHub,
   click **"Use this template"** on the Yanextfab repo (or `git clone` it if you're not using
   GitHub) to get your own copy under a new name.
2. Rename the project — run `make init` (or `uv run scripts/init.py`) right after cloning. It
   prompts for a project name, description, and author, then automatically rewrites every
   hardcoded template-branding string across the repo — see
   [Creating Your Own Project From This Template](https://marcelofossrj.github.io/yanextfab/getting-started/#creating-your-own-project-from-this-template)
   in the docs for exactly what it changes.
3. Continue with **Quickstart** below.

## Quickstart

```bash
cp .env.example .env
```

Open `.env` and fill in `JWT_SECRET` (generate with `openssl rand -hex 32` — don't skip this)
and, optionally, `ANTHROPIC_API_KEY` to make the AI chat example respond.

```bash
make up   # or: docker compose up --build
```

This starts Postgres, the backend, the frontend, and Mailpit (a dev email inbox), and keeps
running in your terminal streaming logs. Once it settles, open <http://localhost:3000> — you
should land on a login page.

- App: <http://localhost:3000>
- API docs (interactive, from FastAPI): <http://localhost:8000/docs>
- Mailpit (dev email inbox): <http://localhost:8025>

See the [full docs](https://marcelofossrj.github.io/yanextfab/) for a guided walkthrough,
every `make` command, troubleshooting, and everything else about the stack.

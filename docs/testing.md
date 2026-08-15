# Testing

`make test` (with the stack running via `make up`) runs both suites inside the containers,
with zero extra setup:

- **Backend**: [pytest](https://docs.pytest.org/). Tests live in `backend/tests/`; a real
  (disposable) Postgres database is required — see `backend/tests/conftest.py`, which creates
  and tears down its own test database automatically against whatever `DATABASE_URL` it's given.
- **Frontend**: [Vitest](https://vitest.dev/). Tests live next to the code they test as
  `*.test.ts` files (e.g. `frontend/src/lib/schemas/auth.test.ts`).

Running natively instead (Option B): `cd backend && uv run pytest` / `cd frontend && pnpm test`
— for the backend, make sure `DATABASE_URL` in `backend/.env` points at a Postgres you can
actually reach (e.g. `postgresql+asyncpg://yanextfab:yanextfab@localhost:5433/yanextfab` for the
Compose Postgres — note **5433**, not Postgres's default 5432, see
[Troubleshooting](troubleshooting.md)).

Both suites run automatically in CI on every pull request — see `.github/workflows/ci.yml`.

## Enable pre-commit hooks (optional, recommended)

```bash
uv tool install pre-commit   # or: pipx install pre-commit
pre-commit install
```

Requires `uv` (backend) and `pnpm` (frontend) to already be installed — see
[Prerequisites](getting-started.md#prerequisites) if you're only using Docker and don't have
them yet.

This is optional — skipping it doesn't break anything locally. What it buys you: Ruff (lint +
format) on the backend and ESLint + Prettier on the frontend run automatically before every
`git commit`, catching the same issues CI would catch on the PR, just earlier and locally
instead of waiting for a CI run.

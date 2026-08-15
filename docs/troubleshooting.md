# Troubleshooting

- **"Port already in use"**: something else on your machine is already using port 3000, 8000,
  8025, or 5433. Stop that process, or edit the port mappings in `docker-compose.yml`. (Postgres
  is deliberately exposed on host port **5433**, not the default 5432, specifically to avoid
  clashing with a Postgres install you might already have running locally — if you connect a
  database GUI tool, point it at 5433, not 5432.)
- **A container keeps restarting or exits immediately**: run `make logs` and look for the
  first error — it's almost always a missing/invalid `.env` value or Docker not having enough
  resources.
- **Docker isn't running at all**: make sure Docker Desktop is open and its whale icon shows
  "running" before `make up`.
- Still stuck: try `make down` then `make up` again for a clean restart.

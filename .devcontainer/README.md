# Devcontainer Draft

This devcontainer is intended for a fuller Codespaces workshop setup:

- Python workspace container
- PostgreSQL sidecar with seeded `trips` data
- `uv` for running inline Python scripts
- learners install `dbc` and ADBC drivers themselves during the workshop

## What it gives learners

- a reproducible environment
- PostgreSQL already available
- a known `ADBC_POSTGRES_URI`
- no local PostgreSQL setup required
- room for learners to do the `dbc` install flow live

## Exact manual test

If you want to validate whether Codespaces is the right teaching environment, the test path is:

```bash
python --version
uv --version
echo "$ADBC_POSTGRES_URI"
psql "$ADBC_POSTGRES_URI" -c "select count(*) from trips;"
uv tool install dbc
dbc --version
dbc install duckdb
dbc install postgresql
uv run "Code Draft/exercise_1.py"
uv run "Code Draft/exercise_2.py"
```

Things to judge while testing:

- how long the codespace build takes
- whether `uv tool install dbc` is painless
- whether driver installation is fast enough for a workshop
- whether Postgres is reliably ready when you need it
- whether the whole flow is simpler than local setup

## Main files

- `devcontainer.json`
- `docker-compose.yml`
- `Dockerfile`
- `post-create.sh`
- `postgres/init/01-trips.sql`

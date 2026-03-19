# ADBC Lab

Minimal workshop test repo for validating a Codespaces-based ADBC teaching environment.

This repo assumes:

- Python code uses `adbc-driver-manager`
- learners install `dbc` themselves
- learners install the `duckdb` and `postgresql` drivers with `dbc`
- Python scripts run with `uv run`

## Exercises

- `exercise_1.py`
  Self-contained DuckDB exercise. Create a small table, run a query, and inspect the Arrow result.

- `completed_exercise_1.py`
  Minimal completed version of Exercise 1.

- `exercise_2.py`
  PostgreSQL to DuckDB exercise. Read a small result from PostgreSQL and land it in DuckDB.

- `completed_exercise_2.py`
  Minimal completed version of Exercise 2.

## Intended Codespaces Test Flow

```bash
python --version
uv --version
uv tool install dbc
dbc install duckdb
dbc install postgresql
uv run exercise_1.py
uv run exercise_2.py
```

If both scripts run cleanly in Codespaces, the environment is at least plausible for teaching.

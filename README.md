# ADBC Lab

Minimal workshop test repo for validating a Codespaces-based ADBC teaching environment.

The code/exercises contained here do not represent final versions of exercises for the workshop, but do contain a basic version of code generated with matching expected dependencies, to test the following assumptions:

- Python code uses `adbc-driver-manager`
- learners install `dbc` themselves
- learners install the `duckdb` and `postgresql` drivers with `dbc`
- Python scripts run with `uv run`

## Setup

Go to https://github.com/codespaces/new and select this repo.

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

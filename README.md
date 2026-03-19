# ADBC Lab

Minimal workshop test repo for validating a Codespaces-based ADBC teaching environment.

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
python exercise_1.py
python exercise_2.py
```

If both scripts run cleanly in Codespaces, the environment is at least plausible for teaching.

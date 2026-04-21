# ADBC Lab

Hands-on exercises for the ADBC workshop. Uses NYC Citi Bike trip data (~1M rows) loaded into a Postgres database.

## Setup

### Option 1: GitHub Codespaces (recommended)

Go to https://github.com/thisisnic/adbc-lab and click **Use this template** → **Open in a codespace**.

The environment will set up automatically: Python, uv, and a Postgres database with the trip data pre-loaded.

### Option 2: Local

You'll need:
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- A running PostgreSQL instance with the trip data loaded (download from [releases](https://github.com/thisisnic/adbc-lab/releases/tag/data-v1))
- Set `ADBC_POSTGRES_URI` if your connection string differs from the default

## Exercises

Follow the instructions in the exercise files:

1. **Exercise 1** (`exercise_1.txt`): Install ADBC and run your first query
2. **Exercise 2** (`exercise_2.txt`): Move data to a local DuckDB and query both backends

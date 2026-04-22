#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["adbc-driver-manager", "pyarrow"]
# ///

"""Exercise 2: Move data from Postgres to a local DuckDB and query both."""

import os

from adbc_driver_manager import dbapi

POSTGRES_URI = os.getenv("ADBC_POSTGRES_URI")

QUERY = """
SELECT
    start_station_name,
    COUNT(*) AS trips,
    ROUND(AVG(tripduration / 60.0), 2) AS avg_duration_minutes
FROM trips
GROUP BY start_station_name
ORDER BY trips DESC
LIMIT 10
"""

# Pull data from Postgres
with dbapi.connect(driver="postgresql", db_kwargs={"uri": POSTGRES_URI}) as pg_conn:
    with pg_conn.cursor() as cur:
        cur.execute("SELECT * FROM trips")
        trips = cur.fetch_arrow_table()

print(f"Pulled {len(trips)} rows from Postgres")
print()

# Load into local DuckDB
with dbapi.connect(driver="duckdb", db_kwargs={"path": "local_analysis.duckdb"}) as duck_conn:
    with duck_conn.cursor() as cur:
        cur.adbc_ingest("trips", trips, mode="replace")
    duck_conn.commit()

print("Loaded into local DuckDB")
print()

# Run the same query against both backends
print("=== Postgres ===")
with dbapi.connect(driver="postgresql", db_kwargs={"uri": POSTGRES_URI}) as conn:
    with conn.cursor() as cur:
        cur.execute(QUERY)
        print(cur.fetch_arrow_table())

print()
print("=== DuckDB ===")
with dbapi.connect(driver="duckdb", db_kwargs={"path": "local_analysis.duckdb"}) as conn:
    with conn.cursor() as cur:
        cur.execute(QUERY)
        print(cur.fetch_arrow_table())

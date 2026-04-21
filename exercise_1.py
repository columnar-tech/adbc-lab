#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["adbc-driver-manager", "pyarrow"]
# ///

"""Exercise 1: Pull data from Postgres with ADBC."""

import os

from adbc_driver_manager import dbapi

POSTGRES_URI = os.getenv(
    "ADBC_POSTGRES_URI", "postgresql://postgres:postgres@postgres:5432/postgres"
)

with dbapi.connect(driver="postgresql", db_kwargs={"uri": POSTGRES_URI}) as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                start_station_name,
                end_station_name,
                tripduration,
                starttime,
                usertype
            FROM trips
            LIMIT 100000
            """
        )
        result = cur.fetch_arrow_table()

print(result)
print()
print("Schema:")
print(result.schema)

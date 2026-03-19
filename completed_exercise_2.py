import os

from adbc_driver_duckdb import dbapi as duckdb_dbapi
from adbc_driver_postgresql import dbapi as postgresql_dbapi


POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@postgres:5432/postgres")


with postgresql_dbapi.connect(POSTGRES_URI) as pg_conn:
    with pg_conn.cursor() as pg_cursor:
        pg_cursor.execute(
            """
            SELECT
              trip_id,
              user_type,
              start_station,
              end_station,
              duration_minutes
            FROM trips
            ORDER BY trip_id
            LIMIT 10
            """
        )
        trips = pg_cursor.fetch_arrow_table()


with duckdb_dbapi.connect("portable_analysis.duckdb") as duck_conn:
    with duck_conn.cursor() as duck_cursor:
        duck_cursor.adbc_ingest("trips_from_postgres", trips, mode="replace")
        duck_cursor.execute(
            """
            SELECT
              start_station,
              COUNT(*) AS trips,
              AVG(duration_minutes) AS avg_duration_minutes
            FROM trips_from_postgres
            GROUP BY start_station
            ORDER BY trips DESC, start_station
            """
        )
        print(duck_cursor.fetch_arrow_table().to_pylist())

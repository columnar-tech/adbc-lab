import os

from adbc_driver_manager import dbapi


POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@postgres:5432/postgres")
DUCKDB_PATH = "portable_analysis.duckdb"


def main() -> None:
    print("Connecting to PostgreSQL...")
    with dbapi.connect(driver="postgresql", db_kwargs={"uri": POSTGRES_URI}) as pg_conn:
        with pg_conn.cursor() as pg_cursor:
            print("Reading a small result set from PostgreSQL...")
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

    print(f"Fetched {trips.num_rows} rows from PostgreSQL.")

    print(f"Connecting to DuckDB at {DUCKDB_PATH}...")
    with dbapi.connect(driver="duckdb", db_kwargs={"path": DUCKDB_PATH}) as duck_conn:
        with duck_conn.cursor() as duck_cursor:
            print("Writing the result into DuckDB...")
            duck_cursor.adbc_ingest("trips_from_postgres", trips, mode="replace")

            print("Running the same style of analytical query locally...")
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
            summary = duck_cursor.fetch_arrow_table()

    print("\nArrow result:")
    print(summary)

    print("\nAs Python values:")
    for row in summary.to_pylist():
        print(row)


if __name__ == "__main__":
    main()

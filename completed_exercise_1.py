from adbc_driver_manager import dbapi


with dbapi.connect(driver="duckdb", db_kwargs={"path": "workshop.duckdb"}) as conn:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE OR REPLACE TABLE bike_trips AS
            SELECT *
            FROM (
              VALUES
                (1, 'member', 'Waterloo', 'Bank', 14),
                (2, 'casual', 'Bank', 'London Bridge', 22),
                (3, 'member', 'Waterloo', 'Soho', 11),
                (4, 'member', 'Soho', 'Bank', 9),
                (5, 'casual', 'Waterloo', 'Bank', 18)
            ) AS t(trip_id, user_type, start_station, end_station, duration_minutes)
            """
        )
        cursor.execute(
            """
            SELECT
              start_station,
              COUNT(*) AS trips,
              AVG(duration_minutes) AS avg_duration_minutes
            FROM bike_trips
            GROUP BY start_station
            ORDER BY trips DESC, start_station
            """
        )
        print(cursor.fetch_arrow_table().to_pylist())

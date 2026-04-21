CREATE TABLE IF NOT EXISTS trips (
    tripduration INTEGER,
    starttime TIMESTAMP,
    stoptime TIMESTAMP,
    start_station_id BIGINT,
    start_station_name TEXT,
    start_station_latitude DOUBLE PRECISION,
    start_station_longitude DOUBLE PRECISION,
    end_station_id BIGINT,
    end_station_name TEXT,
    end_station_latitude DOUBLE PRECISION,
    end_station_longitude DOUBLE PRECISION,
    bikeid BIGINT,
    usertype TEXT,
    birth_year BIGINT,
    gender TEXT
);

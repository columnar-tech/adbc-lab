#!/usr/bin/env bash

set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

# Download Citi Bike trip data
DATA_URL="https://github.com/thisisnic/adbc-lab/releases/download/data-v1/citibike_trips.parquet"
DATA_FILE="citibike_trips.parquet"

if [ ! -f "$DATA_FILE" ]; then
  echo "Downloading trip data..."
  curl -L "$DATA_URL" -o "$DATA_FILE"
fi

# Load parquet into Postgres
echo "Loading data into Postgres..."
uv run --with pyarrow --with psycopg2-binary python <<'PYTHON'
import pyarrow.parquet as pq
import pyarrow.csv as csv
import psycopg2
import io

table = pq.read_table("citibike_trips.parquet")

conn = psycopg2.connect("postgresql://postgres:postgres@postgres:5432/postgres")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM trips")
if cur.fetchone()[0] > 0:
    print("Data already loaded, skipping.")
else:
    buf = io.BytesIO()
    csv.write_csv(table, buf)
    buf.seek(0)
    cur.copy_expert("COPY trips FROM STDIN WITH (FORMAT csv, HEADER true)", buf)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM trips")
    print(f"Loaded {cur.fetchone()[0]:,} rows into Postgres")

cur.close()
conn.close()
PYTHON

cat <<'EOF'

Workshop environment ready.

Try:
  uv tool install dbc
  dbc install postgresql
  dbc install duckdb
  uv run exercise_1.py
  uv run exercise_2.py

EOF

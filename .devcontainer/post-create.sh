#!/usr/bin/env bash

set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

cat <<'EOF'

Workshop environment ready.

Try:
  uv tool install dbc
  dbc install duckdb
  dbc install postgresql
  uv run exercise_1.py
  uv run exercise_2.py

EOF

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
  uv run "Code Draft/exercise_1.py"
  uv run "Code Draft/exercise_2.py"

Learners still need to install:
  - dbc
  - the duckdb driver
  - the postgresql driver

PostgreSQL URI inside the codespace, once drivers are installed:
  $ADBC_POSTGRES_URI

EOF

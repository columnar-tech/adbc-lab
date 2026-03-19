#!/usr/bin/env bash

set -euo pipefail

export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

uv pip install --system -r requirements.txt

cat <<'EOF'

Workshop environment ready.

Try:
  python exercise_1.py
  python exercise_2.py

EOF

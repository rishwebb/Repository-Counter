#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.github_repo_summary.env"
PY_FILE="$SCRIPT_DIR/github_repo_summary.py"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE" >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

if [[ -z "${GITHUB_USERNAME:-}" ]]; then
  echo "GITHUB_USERNAME is missing in $ENV_FILE" >&2
  exit 1
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN is missing in $ENV_FILE" >&2
  exit 1
fi

python3 "$PY_FILE" "$GITHUB_USERNAME" --token "$GITHUB_TOKEN"

# If running in an interactive terminal, wait for a keypress before exiting
# This prevents terminal windows from closing immediately when double-clicked.
if [ -t 1 ]; then
  printf "\nPress any key to exit..."
  # read one character silently
  read -r -n 1 -s
  printf "\n"
fi

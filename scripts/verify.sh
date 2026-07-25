#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

if [[ ! -x ".venv/bin/python" ]]; then
    printf 'The virtual environment is missing. Run ./scripts/setup.sh first.\n' >&2
    exit 1
fi

.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python -m coverage erase
.venv/bin/python -m coverage run manage.py test
.venv/bin/python -m coverage report --fail-under=95 -m

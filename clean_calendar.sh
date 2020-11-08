#!/usr/bin/env bash

set -euo pipefail
# set -x

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
source "$DIR/env/bin/activate"

python3 "$DIR/clean_calendar.py"

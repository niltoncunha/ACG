#!/usr/bin/env sh
set -eu
CONFIG="${ACG_CONFIG:-acg.yaml}"
MODE="${1:-all}"
python3 "$(dirname "$0")/acg-enforce.py" --config "$CONFIG" --mode "$MODE"

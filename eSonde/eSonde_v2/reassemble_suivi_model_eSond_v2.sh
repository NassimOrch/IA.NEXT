#!/bin/sh
set -eu
# Extract the two independent ZIP archives into the same destination.
# Usage: sh reassemble_suivi_model_eSond_v2.sh [part1.zip] [part2.zip] [destination]
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PART1=${1:-"$(pwd)/suivi_model_eSond_v2.zip"}
PART2=${2:-"$(pwd)/suivi_model_eSond_v2_part2.zip"}
DEST=${3:-"$(pwd)/suivi_model_eSond_v2_extracted"}
command -v unzip >/dev/null 2>&1 || { echo 'unzip is required' >&2; exit 2; }
command -v python3 >/dev/null 2>&1 || { echo 'python3 is required' >&2; exit 2; }
[ -f "$PART1" ] || { echo "Missing ZIP part 1: $PART1" >&2; exit 2; }
[ -f "$PART2" ] || { echo "Missing ZIP part 2: $PART2" >&2; exit 2; }
mkdir -p "$DEST"
unzip -oq "$PART1" -d "$DEST"
unzip -oq "$PART2" -d "$DEST"
ROOT="$DEST/suivi_model_eSond_v2"
python3 "$ROOT/scripts/verify_suivi_package.py" "$ROOT"
echo "Verified package extracted at: $ROOT"

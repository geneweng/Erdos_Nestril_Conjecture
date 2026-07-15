#!/bin/zsh
# Parallel sound exhaustive sweep for one vertex count.
# Usage: ./run_sweep.sh <n> <maxedges> <workers>
set -e
cd "$(dirname "$0")"
N=$1
MAXM=$2
W=${3:-10}
for ((i=0; i<W; i++)); do
  geng -c -q -D4 "$N" "21:$MAXM" "$i/$W" 2>/dev/null \
    | python3 hunt_sweep.py "n${N}_p${i}" >> "results/log_n${N}.txt" 2>&1 &
done
wait
echo "n=$N sweep complete" >> "results/log_n${N}.txt"

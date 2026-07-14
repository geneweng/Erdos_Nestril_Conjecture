"""Exhaustive sweep: read graph6 on stdin, flag any graph with chi'_s >= 21.

Usage: geng -c -d1 -D4 <n> 21:<maxm> | python hunt_sweep.py <tag>

For each graph:
  - DSATUR-color the conflict graph L(G)^2; if <= 20 colors, it is not a
    counterexample (skip).  If exactly 20, log as a near-miss candidate.
  - If DSATUR needs >= 21 colors, decide 20-colorability by SAT.
    UNSAT => counterexample to Erdos-Nesetril for Delta=4.
"""

import sys
import networkx as nx
from sec import conflict_graph, greedy_clique, sat_colorable

tag = sys.argv[1] if len(sys.argv) > 1 else "sweep"
near_path = f"results/near_{tag}.g6"
hit_path = f"results/HIT_{tag}.g6"

count = 0
near = 0
hits = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    count += 1
    G = nx.from_graph6_bytes(line.encode())
    # Fast pre-prune: an edge uv with deg(u)+deg(v) <= 6 has <= 16 conflicts,
    # impossible in an edge-critical chi'_s=21 graph (needs >= 20).
    deg = dict(G.degree())
    if any(deg[u] + deg[v] <= 6 for u, v in G.edges()):
        continue
    C = conflict_graph(G)
    # Criticality prune: in an edge-critical graph with chi'_s = 21, every
    # edge conflicts with >= 20 others (else color G-e with 20 colors and
    # extend greedily).  Any counterexample contains such a critical graph,
    # which is itself enumerated, so skipping non-critical graphs is sound.
    if min(dict(C.degree()).values()) < 20:
        continue
    col = nx.coloring.greedy_color(C, strategy="DSATUR")
    used = max(col.values()) + 1
    if used <= 19:
        continue
    if used == 20:
        # Possible chi'_s = 20 graph; record for structural analysis.
        with open(near_path, "a") as f:
            f.write(line + "\n")
        near += 1
        continue
    # DSATUR needed >= 21 colors: decide exactly.
    ok, _ = sat_colorable(C, 20, clique=greedy_clique(C))
    if ok:
        with open(near_path, "a") as f:
            f.write(line + " sat20\n")
        near += 1
    else:
        hits += 1
        with open(hit_path, "a") as f:
            f.write(line + "\n")
        print(f"*** COUNTEREXAMPLE: {line}", flush=True)

print(f"[{tag}] done: {count} graphs, {near} near-misses, {hits} hits", flush=True)

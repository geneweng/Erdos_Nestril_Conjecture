"""Cross-validate the SAT-based exact chi'_s against plain backtracking."""

import random
import networkx as nx
from sec import conflict_graph, strong_chromatic_index, verify_strong_coloring


def chromatic_backtrack(C):
    """Exact chromatic number by branch-and-bound backtracking."""
    nodes = sorted(C.nodes(), key=lambda v: -C.degree(v))
    n = len(nodes)
    best = [n + 1]

    def bt(i, colors, used):
        if used >= best[0]:
            return
        if i == n:
            best[0] = used
            return
        v = nodes[i]
        forbidden = {colors[u] for u in C.neighbors(v) if u in colors}
        for c in range(used):
            if c not in forbidden:
                colors[v] = c
                bt(i + 1, colors, used)
                del colors[v]
        colors[v] = used
        bt(i + 1, colors, used + 1)
        del colors[v]

    bt(0, {}, 0)
    return best[0]


rng = random.Random(42)
trials = 0
for _ in range(60):
    n = rng.randint(6, 10)
    p = rng.uniform(0.2, 0.6)
    G = nx.gnp_random_graph(n, p, seed=rng.randint(0, 10**9))
    if max(dict(G.degree()).values() or [0]) > 4:
        # trim edges at high-degree vertices to keep Delta <= 4
        for v in list(G.nodes()):
            while G.degree(v) > 4:
                G.remove_edge(v, next(iter(G.neighbors(v))))
    if G.number_of_edges() < 3:
        continue
    C = conflict_graph(G)
    exact_sat, col = strong_chromatic_index(G)
    exact_bt = chromatic_backtrack(C)
    assert exact_sat == exact_bt, (exact_sat, exact_bt, nx.to_graph6_bytes(G))
    assert verify_strong_coloring(G, col)
    trials += 1

print(f"cross-check passed on {trials} random graphs (SAT == backtracking, colorings valid)")

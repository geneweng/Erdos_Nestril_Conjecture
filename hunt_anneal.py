"""Simulated annealing over Delta<=4 graphs, maximizing exact chi'_s.

Usage: python hunt_anneal.py <n> <seed> <steps>

Moves: add / remove / rewire an edge keeping Delta <= 4.
Energy: -(chi'_s) with clique lower bound of the conflict graph as tiebreak.
Any state with chi'_s >= 21 is a counterexample -> dumped and celebrated.
"""

import random
import sys
import math
import networkx as nx
from sec import conflict_graph, strong_chromatic_index, blowup

n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
steps = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
rng = random.Random(seed)


def score(G):
    if G.number_of_edges() < 15:
        return 0.0, 0
    v, _ = strong_chromatic_index(G, ub_hint=21, exact_clique=False)
    C = conflict_graph(G)
    # clique lower bound as gradient signal
    from sec import greedy_clique
    q = len(greedy_clique(C))
    return v + 0.01 * q, v


def random_start():
    if seed % 3 == 0 and n >= 10:
        # perturbed C5 blowup plus extra vertices
        G = blowup(nx.cycle_graph(5), {i: 2 for i in range(5)})
        G.add_nodes_from(range(10, n))
        for _ in range(n - 10):
            pass
        return G
    else:
        while True:
            try:
                G = nx.random_regular_graph(4, n, seed=rng.randint(0, 10**9))
                return nx.Graph(G.edges())
            except nx.NetworkXError:
                continue


def mutate(G):
    H = G.copy()
    deg = dict(H.degree())
    op = rng.random()
    edges = list(H.edges())
    if op < 0.4 and edges:
        # rewire: remove an edge, add another
        u, v = rng.choice(edges)
        H.remove_edge(u, v)
        cand = [(a, b) for a in H.nodes() for b in H.nodes()
                if a < b and not H.has_edge(a, b)
                and H.degree(a) < 4 and H.degree(b) < 4]
        if cand:
            H.add_edge(*rng.choice(cand))
    elif op < 0.7:
        cand = [(a, b) for a in H.nodes() for b in H.nodes()
                if a < b and not H.has_edge(a, b)
                and deg[a] < 4 and deg[b] < 4]
        if cand:
            H.add_edge(*rng.choice(cand))
    elif edges:
        u, v = rng.choice(edges)
        H.remove_edge(u, v)
    return H


G = random_start()
cur, cur_chi = score(G)
best, best_chi = cur, cur_chi
bestG = G.copy()
T0, T1 = 0.8, 0.02
for t in range(steps):
    T = T0 * (T1 / T0) ** (t / steps)
    H = mutate(G)
    s, chi = score(H)
    if chi >= 21:
        g6 = nx.to_graph6_bytes(H, header=False).decode().strip()
        print(f"*** COUNTEREXAMPLE chi'_s={chi}: {g6}", flush=True)
        with open("results/HIT_anneal.g6", "a") as f:
            f.write(g6 + "\n")
        break
    if s >= cur or rng.random() < math.exp((s - cur) / T):
        G, cur, cur_chi = H, s, chi
        if s > best:
            best, best_chi, bestG = s, chi, H.copy()
    if t % 500 == 0:
        print(f"[n={n} seed={seed}] step {t}: cur chi'_s={cur_chi}, best={best_chi}", flush=True)

g6 = nx.to_graph6_bytes(bestG, header=False).decode().strip()
print(f"[n={n} seed={seed}] FINAL best chi'_s={best_chi}  {g6}", flush=True)

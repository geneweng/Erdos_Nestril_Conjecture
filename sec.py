"""Strong edge coloring toolkit for the Erdos-Nesetril conjecture hunt.

A strong edge coloring of G is a partition of E(G) into induced matchings.
Equivalently, a proper vertex coloring of the conflict graph L(G)^2, whose
vertices are the edges of G, with two edges adjacent iff they share an
endpoint or some edge of G joins their endpoints (distance <= 1 in L(G)).

The strong chromatic index chi'_s(G) is the minimum number of colors.

Erdos-Nesetril: chi'_s(G) <= 1.25 * Delta(G)^2.
For Delta = 4 the conjectured bound is 20; the proven bound is 21
(Huang-Santana-Yu).  A counterexample is a Delta=4 graph with chi'_s = 21.
"""

import itertools
import networkx as nx
from pysat.solvers import Cadical195


def conflict_graph(G):
    """Return L(G)^2 as a networkx graph whose nodes are edges of G."""
    edges = [tuple(sorted(e)) for e in G.edges()]
    C = nx.Graph()
    C.add_nodes_from(edges)
    # Two edges conflict iff they share an endpoint or an edge of G joins them.
    adj = {v: set(G.neighbors(v)) for v in G.nodes()}
    for e, f in itertools.combinations(edges, 2):
        a, b = e
        c, d = f
        if a in f or b in f:
            C.add_edge(e, f)
            continue
        if c in adj[a] or d in adj[a] or c in adj[b] or d in adj[b]:
            C.add_edge(e, f)
    return C


def greedy_clique(C):
    """A large (not necessarily maximum) clique in C, greedily by degree."""
    best = []
    nodes = sorted(C.nodes(), key=lambda v: C.degree(v), reverse=True)
    for start in nodes[:40]:
        clique = [start]
        cand = set(C.neighbors(start))
        while cand:
            v = max(cand, key=lambda u: len(cand & set(C.neighbors(u))))
            clique.append(v)
            cand &= set(C.neighbors(v))
        if len(clique) > len(best):
            best = clique
    return best


def max_clique_exact(C, limit_nodes=200):
    """Exact maximum clique via networkx (fine at these sizes)."""
    best = []
    for q in nx.find_cliques(C):
        if len(q) > len(best):
            best = q
    return best


def sat_colorable(C, k, clique=None, solver_cls=Cadical195):
    """Decide whether conflict graph C is properly k-colorable.

    Returns (True, coloring dict) or (False, None).
    Symmetry breaking: nodes of `clique` are pre-assigned distinct colors.
    """
    nodes = list(C.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    if clique is None:
        clique = greedy_clique(C)
    if len(clique) > k:
        return False, None

    def var(v, c):
        return idx[v] * k + c + 1

    cnf = []
    for v in nodes:
        cnf.append([var(v, c) for c in range(k)])
    for u, v in C.edges():
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c)])
    for c, v in enumerate(clique):
        cnf.append([var(v, c)])

    with solver_cls(bootstrap_with=cnf) as s:
        if not s.solve():
            return False, None
        model = set(l for l in s.get_model() if l > 0)
        coloring = {}
        for v in nodes:
            for c in range(k):
                if var(v, c) in model:
                    coloring[v] = c
                    break
        return True, coloring


def strong_chromatic_index(G, ub_hint=None, lb_hint=None, exact_clique=True):
    """Compute chi'_s(G) exactly.  Returns (value, coloring)."""
    C = conflict_graph(G)
    if C.number_of_nodes() == 0:
        return 0, {}
    clique = max_clique_exact(C) if exact_clique else greedy_clique(C)
    lb = max(len(clique), lb_hint or 0)
    greedy = nx.coloring.greedy_color(C, strategy="DSATUR")
    ub = max(greedy.values()) + 1
    if ub_hint:
        ub = min(ub, ub_hint)
    coloring = greedy
    while ub > lb:
        ok, col = sat_colorable(C, ub - 1, clique=clique)
        if not ok:
            break
        coloring = col
        ub = max(col.values()) + 1
    return ub, coloring


def verify_strong_coloring(G, coloring):
    """Check that `coloring` (edge -> color) is a valid strong edge coloring."""
    C = conflict_graph(G)
    assert set(coloring) == set(C.nodes()), "coloring must cover all edges"
    for u, v in C.edges():
        if coloring[u] == coloring[v]:
            return False
    return True


def blowup(G, sizes):
    """Blow up each vertex v of G into an independent set of size sizes[v]."""
    H = nx.Graph()
    parts = {}
    ctr = 0
    for v in G.nodes():
        parts[v] = list(range(ctr, ctr + sizes[v]))
        H.add_nodes_from(parts[v])
        ctr += sizes[v]
    for u, v in G.edges():
        for a in parts[u]:
            for b in parts[v]:
                H.add_edge(a, b)
    return H


if __name__ == "__main__":
    # Sanity checks.
    C5 = nx.cycle_graph(5)
    v, col = strong_chromatic_index(C5)
    print(f"C5: Delta=2, chi'_s = {v} (conjecture bound 5)")
    assert v == 5 and verify_strong_coloring(C5, col)

    # The extremal example for Delta=4: blow up C5 by independent sets of size 2.
    B = blowup(C5, {i: 2 for i in range(5)})
    assert max(dict(B.degree()).values()) == 4
    v, col = strong_chromatic_index(B)
    print(f"C5 blowup x2: Delta=4, m={B.number_of_edges()}, chi'_s = {v} (conjecture bound 20)")
    assert verify_strong_coloring(B, col)

    P = nx.petersen_graph()
    v, col = strong_chromatic_index(P)
    print(f"Petersen: Delta=3, chi'_s = {v} (conjecture bound 10)")
    assert verify_strong_coloring(P, col)

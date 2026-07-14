"""Structured Delta=4 families: exact chi'_s for each, flag anything >= 21."""

import itertools
import subprocess
import networkx as nx
from sec import strong_chromatic_index, blowup

results = []


def check(name, G, bound=21):
    d = max(dict(G.degree()).values())
    assert d <= 4, f"{name}: Delta={d}"
    v, _ = strong_chromatic_index(G, ub_hint=21, exact_clique=G.number_of_edges() <= 40)
    results.append((v, name, G.number_of_nodes(), G.number_of_edges()))
    flag = " ***" if v >= bound else ""
    print(f"chi'_s={v:3d}  {name}  (n={G.number_of_nodes()}, m={G.number_of_edges()}){flag}", flush=True)


# --- 4-regular circulants C_n(a, b) ---
for n in range(11, 11):
    seen = set()
    for a in range(1, n // 2 + 1):
        for b in range(a + 1, n // 2 + 1):
            if a == n - a or b == n - b:  # would give degree 2 connection
                continue
            G = nx.circulant_graph(n, [a, b])
            if max(dict(G.degree()).values()) != 4 or not nx.is_connected(G):
                continue
            key = nx.weisfeiler_lehman_graph_hash(G)
            if key in seen:
                continue
            seen.add(key)
            check(f"C_{n}({a},{b})", G)

# --- torus grids C_m x C_n (cartesian product, 4-regular) ---
for m in range(3, 3):
    for n in range(m, 9):
        G = nx.cartesian_product(nx.cycle_graph(m), nx.cycle_graph(n))
        G = nx.convert_node_labels_to_integers(G)
        check(f"C_{m} x C_{n}", G)

# --- line graphs of connected cubic graphs (4-regular) ---
for nn in (4, 6, 8, 10, 12, 14):
    out = subprocess.run(["geng", "-c", "-q", "-d3", "-D3", str(nn)],
                         capture_output=True, text=True)
    for i, line in enumerate(out.stdout.split()):
        H = nx.from_graph6_bytes(line.encode())
        G = nx.convert_node_labels_to_integers(nx.line_graph(H))
        check(f"L(cubic {nn}v #{i})", G)

# --- blowups of odd cycles with degree <= 4 ---
for n in (5, 7, 9, 11):
    base = nx.cycle_graph(n)
    for sizes in itertools.product((1, 2, 3), repeat=n):
        if all(sizes[(i - 1) % n] + sizes[(i + 1) % n] <= 4 for i in range(n)):
            if len(set(sizes)) == 1 and sizes[0] == 1:
                continue
            G = blowup(base, dict(enumerate(sizes)))
            if not nx.is_connected(G):
                continue
            # canonical: skip rotations/reflections duplicates
            rots = {tuple(sizes[(i + k) % n] for i in range(n)) for k in range(n)}
            rots |= {tuple(r[::-1]) for r in rots}
            if sizes != min(rots):
                continue
            check(f"C_{n} blowup {sizes}", G)

# --- named graphs ---
check("Chvatal", nx.chvatal_graph())
check("K5", nx.complete_graph(5))
check("K_{4,4}", nx.complete_bipartite_graph(4, 4))
check("Q4 hypercube", nx.convert_node_labels_to_integers(nx.hypercube_graph(4)))
check("Robertson(19,girth5)-like: cage(4,5)", nx.LCF_graph(19, [0], 1) if False else nx.circulant_graph(19, [1, 2]))  # placeholder

results.sort(reverse=True)
print("\nTop 12 by chi'_s:")
for v, name, n, m in results[:12]:
    print(f"  {v:3d}  {name} (n={n}, m={m})")

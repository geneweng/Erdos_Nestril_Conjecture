"""Bounded-effort hunt over the remaining structured families.

For the counterexample hunt only DSATUR >= 21 matters (then we decide
exactly).  Otherwise we report chi'_s as an exact value when a budgeted SAT
walk-down converges, else as a bracket [lb, ub].
"""

import itertools
import subprocess
import networkx as nx
from sec import conflict_graph, greedy_clique, sat_colorable, blowup

BUDGET = 300_000  # cadical conflicts per decision


def bounded_chi(G):
    """Return (lb, ub) with lb == ub when exact."""
    C = conflict_graph(G)
    clique = greedy_clique(C)
    lb = len(clique)
    col = nx.coloring.greedy_color(C, strategy="DSATUR")
    ub = max(col.values()) + 1
    while ub > lb:
        ok, col2 = sat_colorable(C, ub - 1, clique=clique, conf_budget=BUDGET)
        if ok is None:
            break  # undecided: leave bracket
        if not ok:
            lb = ub
            break
        ub = max(col2.values()) + 1
    return lb, ub


def check(name, G):
    assert max(dict(G.degree()).values()) <= 4
    lb, ub = bounded_chi(G)
    val = str(ub) if lb == ub else f"[{lb},{ub}]"
    flag = " ***" if ub >= 21 else ""
    print(f"chi'_s={val:>8}  {name}  (n={G.number_of_nodes()}, m={G.number_of_edges()}){flag}",
          flush=True)


# --- circulants n=15..40 ---
for n in range(15, 41):
    for a in range(1, n // 2 + 1):
        for b in range(a + 1, n // 2 + 1):
            if 2 * a == n or 2 * b == n:
                continue
            G = nx.circulant_graph(n, [a, b])
            if max(dict(G.degree()).values()) != 4 or not nx.is_connected(G):
                continue
            check(f"C_{n}({a},{b})", G)
    print(f"-- circulants n={n} done", flush=True)

# --- line graphs of connected cubic graphs on 14 vertices ---
out = subprocess.run(["geng", "-c", "-q", "-d3", "-D3", "14"],
                     capture_output=True, text=True)
for i, line in enumerate(out.stdout.split()):
    H = nx.from_graph6_bytes(line.encode())
    check(f"L(cubic 14v #{i})", nx.convert_node_labels_to_integers(nx.line_graph(H)))
print("-- line graphs done", flush=True)

# --- blowups of odd cycles ---
for n in (5, 7, 9, 11):
    base = nx.cycle_graph(n)
    for sizes in itertools.product((1, 2, 3), repeat=n):
        if not all(sizes[(i - 1) % n] + sizes[(i + 1) % n] <= 4 for i in range(n)):
            continue
        rots = {tuple(sizes[(i + k) % n] for i in range(n)) for k in range(n)}
        rots |= {tuple(r[::-1]) for r in rots}
        if tuple(sizes) != min(rots):
            continue
        G = blowup(base, dict(enumerate(sizes)))
        if G.number_of_edges() < 10 or not nx.is_connected(G):
            continue
        check(f"C_{n} blowup {sizes}", G)
print("-- blowups done", flush=True)

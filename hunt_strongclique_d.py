"""Generalized strong-clique SAT: does any graph with Delta <= D contain
`target` edges that pairwise conflict?

Usage: python hunt_strongclique_d.py <D> <target> [N]

Rigorous vertex bound: fix a clique edge (0,1); every clique edge has an
endpoint in S = N[0] u N[1], |S| <= 2D.  Every relevant vertex is an
endpoint of a clique edge; at most target-1 clique edges have an endpoint
outside S, so N <= 2D + (target - 1) suffices.
"""

import sys
import itertools
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical195

D = int(sys.argv[1])
target = int(sys.argv[2])
N = int(sys.argv[3]) if len(sys.argv) > 3 else 2 * D + target - 1

pool = IDPool()
pairs = list(itertools.combinations(range(N), 2))
E = lambda a, b: pool.id(("e", min(a, b), max(a, b)))
K = lambda a, b: pool.id(("k", min(a, b), max(a, b)))

# labels: 0,1 = base edge; 2..D = N(0)\{1}; D+1..2D-1 = fresh N(1)\{0}
n0_hi = D          # N(0) subset {1, 2..D}
n1_hi = 2 * D - 1  # N(1) subset {0, 2..2D-1}

cnf = [[K(0, 1)]]
for a, b in pairs:
    cnf.append([-K(a, b), E(a, b)])
for j in range(n0_hi + 1, N):
    cnf.append([-E(0, j)])
for j in range(n1_hi + 1, N):
    cnf.append([-E(1, j)])
# prefix form for N(0)\{1} and fresh N(1)
for j in range(3, n0_hi + 1):
    cnf.append([-E(0, j), E(0, j - 1)])
for j in range(D + 2, n1_hi + 1):
    cnf.append([-E(1, j), E(1, j - 1)])
# every selected edge touches S
for a, b in pairs:
    if a >= 2:
        clause = [-K(a, b)]
        for x in (a, b):
            if x <= n0_hi:
                clause.append(E(0, x))
            if x <= n1_hi:
                clause.append(E(1, x))
        cnf.append(clause)
# pairwise conflicts
for (a, b), (c, d) in itertools.combinations(pairs, 2):
    if len({a, b, c, d}) == 4:
        cnf.append([-K(a, b), -K(c, d), E(a, c), E(a, d), E(b, c), E(b, d)])
for v in range(N):
    lits = [E(v, u) for u in range(N) if u != v]
    cnf.extend(CardEnc.atmost(lits=lits, bound=D, vpool=pool,
                              encoding=EncType.seqcounter).clauses)
klits = [K(a, b) for a, b in pairs]
cnf.extend(CardEnc.atleast(lits=klits, bound=target, vpool=pool,
                           encoding=EncType.seqcounter).clauses)

print(f"D={D} target={target} N={N}: {pool.top} vars, {len(cnf)} clauses", flush=True)
with Cadical195(bootstrap_with=cnf) as s:
    if s.solve():
        model = set(l for l in s.get_model() if l > 0)
        sel = [(a, b) for a, b in pairs if K(a, b) in model]
        host = [(a, b) for a, b in pairs if E(a, b) in model]
        print(f"SAT: {target}-edge strong clique exists for Delta<={D}")
        print("clique:", sel)
        print("host:", host)
    else:
        print(f"UNSAT: no Delta<={D} graph has a {target}-edge strong clique")
